from django.shortcuts import render, redirect
from interface.models import Role, PossiblePrivilege, Privilege
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    possible_privs = PossiblePrivilege.objects.all()
    roles = Role.objects.all()
    return render(request, 'interface/index.html', context={'possible_privs': possible_privs, 'roles': roles})


def roles_and_privs(request):
    # get_all_roles_with_privs is a static method on Role model
    data_list = Role.get_all_roles_with_privs()
    return JsonResponse({'context': data_list})


def all_possible_privs(request):
    possible_privs = list(PossiblePrivilege.objects.all().values())
    return JsonResponse({'context': possible_privs})


def add_possible_priv(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))
        priv = json_data['add_priv']
        obj, created = PossiblePrivilege.objects.get_or_create(
            priv_name=priv
        )
        outgoing_data = {}
        if created:
            outgoing_data['message'] = 'Created possible privilege'
            # send back the priv that was added so the frontend knows what to add
            outgoing_data['added_priv'] = priv
        elif obj:
            outgoing_data['message'] = f"possible privilege {obj.priv_name} already exists"
        return JsonResponse({'context': outgoing_data})
    return JsonResponse({'error': 'Request method was not POST'})

def delete_possible_priv(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        delete_privs = json_data['delete_privs']
        data = {'message': "Deleted privilege(s): ", 'error': "Error privileges do not exist: "}
        for priv in delete_privs:
            try:
                p = PossiblePrivilege.objects.get(priv_name=priv)
                p.delete()
                data['message'] += priv
            except PossiblePrivilege.DoesNotExist:
                data['error'] += priv
        return JsonResponse({'context': data})
    return JsonResponse({'error': 'Request method was not POST'})

def add_role(request):
    role = request.POST.get('role')
    obj, created = Role.objects.get_or_create(
        role_name=role
    )
    if created:
        print(f"created role {role}")
    elif obj:
        print(f"role {role} already exists")
    return redirect('index')

def delete_role(request):
    role = request.POST.get('role')
    try:
        r = Role.objects.get(role_name=role)
        r.delete()
        print(f"deleted role {role}")
    except Role.DoesNotExist:
        print(f"role {role} doesn't exist")
    return redirect('index')

def assign_priv_to_role(request):
    role = request.POST.get('role')
    priv = request.POST.get('priv')
    r, p = None, None
    try:
        r = Role.objects.get(role_name=role)
    except Role.DoesNotExist:
        print("role does not exist")

    try:
        p = PossiblePrivilege.objects.get(priv_name=priv)
    except PossiblePrivilege.DoesNotExist:
        print("privilege does not exist")

    if r and p:
        obj, created = Privilege.objects.get_or_create(
            role=r,
            priv=p
        )
        if created:
            print(f"assigned privilege {priv} to {role}")
        elif obj:
            print(f"role {role} already has privilege {priv}")

    return redirect('index')

def remove_priv_from_role(request):
    role = request.POST.get('role')
    priv = request.POST.get('priv')
    r, p = None, None
    try:
        r = Role.objects.get(role_name=role)
    except Role.DoesNotExist:
        print("role does not exist")

    try:
        p = PossiblePrivilege.objects.get(priv_name=priv)
    except PossiblePrivilege.DoesNotExist:
        print("privilege does not exist")
    
    if r and p:
        try:
            privilege = Privilege.objects.get(role=r, priv=p)
            privilege.delete()
            print(f"removed privilege {priv} for role {role}")
        except:
            print("could not remove privilege")
    
    return redirect('index')