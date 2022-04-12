from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=200)
    password = models.CharField(max_length=256)
    token = models.CharField(max_length=256)


class LDSportInfo(models.Model):
    UserID = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    weekLdrunTime = models.CharField(max_length=256)
    weekLdrunNum = models.CharField(max_length=256)
    weekLdrunDistance = models.CharField(max_length=256)
    weekLdrunPace = models.CharField(max_length=256)
    termLdrunDistance = models.CharField(max_length=256)
    reachLdrunTargetNum = models.CharField(max_length=256)
    reachLdrunScore = models.CharField(max_length=256)


class MrSportInfo(models.Model):
    UserID = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    weekMrunTime = models.CharField(max_length=256)
    weekMrunNum = models.CharField(max_length=256)
    weekMrunDistance = models.CharField(max_length=256)
    weekMrunPace = models.CharField(max_length=256)
    termMrunDistance = models.CharField(max_length=256)
    reachMrunTargetNum = models.CharField(max_length=256)
    reachMrunScore = models.CharField(max_length=256)



