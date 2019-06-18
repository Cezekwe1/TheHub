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
import json
# Create your views here.
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_tasks(request):
    users_tasks = []
    organization_tasks = []
    tasks = Task.objects.filter(owners__id=request.user.id)
    current_org = request.user.profile.get_current_org()
    if current_org:
        org_task_set = Task.objects.filter(organization= current_org.id)
        
        for task in org_task_set:
            org_id = task.organization.id if task.organization else None
            task_owners = []
            for owner in task.owners.all():
                obj = {"id": owner.id, "username": owner.username, "email": owner.email }
                task_owners.append(obj)
            
            obj = {"id":task.id, "description": task.description , "title":task.title, "organization":org_id, "owners": task_owners}
            organization_tasks.append(obj)
    
    for task in tasks:
        org_id = task.organization.id if task.organization else None
        task_owners = []
        for owner in task.owners.all():
            obj = {"id": owner.id, "username": owner.username, "email": owner.email }
            task_owners.append(obj)
        obj = {"id":task.id, "description": task.description , "title":task.title, "organization":org_id, "owners": task_owners}
        users_tasks.append(obj)
    
    return JsonResponse({"my_tasks": users_tasks, "org_tasks": organization_tasks}) 


@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@valid_func_method(method="POST")
def make_task(request):
    if request.user.is_authenticated:
        title = request.POST["title"] if "title" in request.POST else None
        description = request.POST["description"] if "description" in request.POST else None
        organization = request.POST["organization"] if "organization" in request.POST else None
        owners = request.POST.getlist("owners")
        task = Task(title=title, description=description, organization=organization)
        task.save()
        owner_objs = []
        result = []
        if owners:
            for owner in owners:
                try: 
                    u = User.objects.get(pk=owner)
                    result.append(u.id)
                    owner_objs.append(u)
                except User.DoesNotExist:
                    JsonResponse({'Error': 'One or more of these user dont exist'}, status=500)

            for obj in owner_objs:
                task.owners.add(obj)
        org_id = task.organization.id if task.organization else None
        task_obj = {"title":task.title, "description":task.description, "organization":org_id, "owners": result}
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
        task.title = body["title"]
        task.description = body["description"]
        owners = body["new_owners"]
        del_owners = body["del_owners"]
        org_id = task.organization.id if task.organization else None
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



        
