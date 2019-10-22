from django.shortcuts import render, redirect
from interface.models import Role, PossiblePrivilege, Privilege

# Create your views here.
def index(request):
    possible_privs = PossiblePrivilege.objects.all()
    roles = Role.objects.all()
    return render(request, 'interface/index.html', context={'possible_privs': possible_privs, 'roles': roles})

def add_possible_priv(request):
    priv = request.POST.get('add_priv')
    obj, created = PossiblePrivilege.objects.get_or_create(
        priv_name=priv
    )
    if created:
        print(f"created possible privilege {priv}")
    elif obj:
        print(f"possible privilege {obj.priv_name} already exists")
    return redirect('index')

def delete_possible_priv(request):
    priv = request.POST.get('delete_priv')
    try:
        p = PossiblePrivilege.objects.get(priv_name=priv)
        p.delete()
        print(f"deleted possible privilege {p.priv_name}")
    except PossiblePrivilege.DoesNotExist:
        print(f"possible privilege {priv} does not exist")
    return redirect('index')

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