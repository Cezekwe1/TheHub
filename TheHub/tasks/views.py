from django.shortcuts import render
from utilities.decorators import valid_func_method
from django.http import JsonResponse
from .models import Task
from django.core.serializers import serialize
from django.contrib.auth.models import User
# Create your views here.

@valid_func_method(method="GET")
def get_tasks(request):
    if request.user.is_authenticated:
        users_tasks = []
        organization_tasks = []
        tasks = Task.objects.filter(owners__id=request.user.id)
        current_org = request.user.profile.current_organization
        for task in tasks:
            obj = {"id":task.id, "description": task.description , "title":task.title, "organization":task.organization.id}
            users_tasks.append(obj)
            if current_org is not None and current_org == task.organization:
                organization_tasks.append(obj)

        return JsonResponse({"my_tasks": users_tasks, "org_tasks": organization_tasks}) 
    else:
        return JsonResponse({"Error": "Not Authenticated"}) 


@valid_func_method(method="POST")
def make_task(request):
    if request.user.is_authenticated:
        title = request.POST["title"]
        description = request.POST["description"]
        organization = request.POST["organization"]
        owners = request.POST["owners"]
        task = Task(title=title, description=description, organization=organization)
        owner_objs = []

        for owner in owners:
            try: 
                u = User.objects.get(pk=owner)
                owner_objs.append(u)
            except User.DoesNotExist:
                JsonResponse({'Error': 'One or more of these user dont exist'}, status=500)

        for obj in owner_objs:
            task.add(obj)
        
        task_obj = {"title":task.title, "description":task.description, "organization":task.organization.id, "owners": owners}
        return JsonResponse(task_obj)
    else:
        JsonResponse({"Error": "User is not authenticated"}, status=500)


@valid_func_method(method="GET")
def get_task(request,task_id):
    task = Task.objects.filter(id=task_id)
    if task:
        task = task[0]
        task_obj = {"title":task.title, "description":task.description, "organization":task.organization.id}
        return JsonResponse(task_obj)
    else: 
        return JsonResponse({"Error": "Task doesnt exist"}, status=500)

@valid_func_method(method="PATCH")
def update_task(request,task_id):
    task = Task.objects.filter(id=task_id)
    if task:
        task = task[0]
        task.title = request.PATCH["title"]
        task.description = request.PATCH["description"]
        task_obj = {"title":task.title, "description":task.description, "organization":task.organization.id}
        return JsonResponse(task_obj)
    else: 
        return JsonResponse({"Error": "Task doesnt exist"}, status=500)


        
