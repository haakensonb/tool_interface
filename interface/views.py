from django.shortcuts import render, redirect
from interface.models import Role, PossiblePrivilege, Privilege

# Create your views here.
def index(request):
    possible_privs = PossiblePrivilege.objects.all()
    return render(request, 'interface/index.html', context={'possible_privs': possible_privs})

def add_possible_priv(request, priv):
    obj, created = PossiblePrivilege.objects.get_or_create(
        priv_name=priv
    )
    if created:
        print(f"created possible privilege {priv}")
    elif obj:
        print(f"possible privilege {obj.priv_name} already exists")
    return redirect('index')

def delete_possible_priv(request, priv):
    try:
        p = PossiblePrivilege.objects.get(priv_name=priv)
        p.delete()
        print(f"deleted possible privilege {p.priv_name}")
    except PossiblePrivilege.DoesNotExist:
        print(f"possible privilege {priv} does not exist")
    return redirect('index')
