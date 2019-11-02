from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=100)

    # should this actually be classmethod?
    @staticmethod
    def get_all_roles_with_privs():
        roles = Role.objects.all()
        data_list = []
        for role in roles:
            data = {}
            data['id'] = role.id
            data['role_name'] = role.role_name
            data['privs'] = []
            for priv in role.privilege_set.all():
                data['privs'].append(priv.priv.priv_name)
            data_list.append(data)
        return data_list

    def __str__(self):
        return self.role_name


class PossiblePrivilege(models.Model):
    priv_name = models.CharField(max_length=100)

    def __str__(self):
        return self.priv_name


class Privilege(models.Model):
    class Meta:
        ordering = ['priv']

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    priv = models.ForeignKey(PossiblePrivilege, on_delete=models.CASCADE)

