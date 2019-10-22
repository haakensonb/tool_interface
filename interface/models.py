from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return self.role_name


class PossiblePrivilege(models.Model):
    priv_name = models.CharField(max_length=100)

    def __str__(self):
        return self.priv_name


class Privilege(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    priv = models.ForeignKey(PossiblePrivilege, on_delete=models.CASCADE)

