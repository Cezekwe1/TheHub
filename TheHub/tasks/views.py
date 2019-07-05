from django.shortcuts import render
from utilities.decorators import valid_func_method
from django.http import JsonResponse, QueryDict
from .models import Task
from django.core.serializers import serialize
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from organizations.models import Organization, OrgInvite
import json
# Create your views here.
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_tasks(request):
    users_tasks = []
    organization_tasks = []
    tasks = Task.objects.filter(owners__id=request.user.id, organization=None)
    current_org = request.user.profile.get_current_org()
    if current_org:
        org_task_set = Task.objects.filter(organization= current_org.id)
        
        for task in org_task_set:
            org_id = task.organization.id if task.organization else None
            task_owners = []
            for owner in task.owners.all():
                obj = {"id": owner.id, "username": owner.username, "email": owner.email }
                task_owners.append(obj)
            
            obj = {"id":task.id, "description": task.description , "title":task.title, "organization":org_id, "owners": task_owners, "completed":task.completed}
            organization_tasks.append(obj)
    
    for task in tasks:
        org_id = task.organization.id if task.organization else None
        task_owners = []
        for owner in task.owners.all():
            obj = {"id": owner.id, "username": owner.username, "email": owner.email }
            task_owners.append(obj)
        obj = {"id":task.id, "description": task.description , "title":task.title, "organization":org_id, "owners": task_owners}
        users_tasks.append(obj)

    organization_tasks.extend(users_tasks)
    return JsonResponse({"my_tasks": users_tasks, "org_tasks": organization_tasks}) 


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def make_task(request):
    if request.user.is_authenticated:
        body = json.loads(request.body)
        title = body["title"] if "title" in body else None
        description = body["description"] if "description" in body else None
        organization = body["organization"] if "organization" in body and  not body["noOrg"] else None
        owners = body["owners"]
        if organization:
            organization = Organization(id=organization)
        task = Task(title=title, description=description, organization=organization)
        task.save()
        print(task, body)
        owner_objs = []
        result = []
        if owners:
            for owner in owners:
                try: 
                    u = User.objects.get(pk=owner)
                    result.append({"id":u.id, "username": u.username, "email": u.email})
                    owner_objs.append(u)
                except User.DoesNotExist:
                    JsonResponse({'Error': 'One or more of these user dont exist'}, status=500)

            for obj in owner_objs:
                task.owners.add(obj)
        org_id = task.organization.id if task.organization else None
        task_obj = {"id": task.id, "title":task.title, "description":task.description, "organization":org_id, "owners": result}
        return JsonResponse(task_obj)
    else:
        JsonResponse({"Error": "User is not authenticated"}, status=500)


@valid_func_method(method="GET")
def get_task(request,task_id):
    if request.user.is_authenticated:
        task = Task.objects.filter(id=task_id)
        if task:
            task = task[0]
            org_id = task.organization.id if task.organization else None
            task_owners = []
            for owner in task.owners.all():
                obj = {"id": owner.id, "username": owner.username, "email": owner.email }
                task_owners.append(obj)
            task_obj = {"title":task.title, "description":task.description, "organization":org_id, "owners":task_owners}
            return JsonResponse(task_obj)
        else: 
            return JsonResponse({"Error": "Task doesnt exist"}, status=500)
    else:
         JsonResponse({"Error": "User is not authenticated"}, status=500)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_task(request,task_id):
    task = Task.objects.filter(id=task_id)
    if task:
        task = task[0]
        body = json.loads(request.body)
        print(body)
        task.title = body["title"] if "title" in body else task.title
        task.description = body["description"] if "description" in body else task.description
        owners = body["new_owners"] if "new_owners" in body else []
        del_owners = body["del_owners"] if "del_owners" in body else []
        org_id = task.organization.id if task.organization else None
        task.completed = body["completed"] if "completed" in body else task.completed
        print(body)
        result = []
        dels = []
        task.save()
        for owner in owners:
            try:
                u = User.objects.get(pk=owner)
                task.owners.add(u)
                result.append(owner)
            except User.DoesNotExist:
                JsonResponse({'Error': 'One or more of these user dont exist'}, status=500)

        for delo in del_owners:
            try:
                u = User.objects.get(pk=delo)
                task.owners.remove(u)
                dels.append(delo)
            except User.DoesNotExist:
                JsonResponse({'Error': 'One or more of these user dont exist'}, status=500)


        task_obj = {"title":task.title, "description":task.description, "organization":org_id, "added": result, "removed": dels}
        return JsonResponse(task_obj)
    else: 
        return JsonResponse({"Error": "Task doesnt exist"}, status=500)
    

@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_task(request, task_id):
    
    task = Task.objects.filter(id=task_id)
    if task:
        task = task[0]
        org_id = task.organization.id if task.organization else None
        task_obj = {"title":task.title, "description":task.description, "organization":org_id}
        task.delete()
        return Response(task_obj)
    else: 
        return Response({"Error": "Task doesnt exist"}, status=500)



        
