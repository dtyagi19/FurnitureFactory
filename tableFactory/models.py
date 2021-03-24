from django.db import models


class Feet(models.Model):
    name = models.CharField(max_length=200)
    width = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    radius = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Leg(models.Model):
    name = models.CharField(max_length=200)
    """
    Creating many to many mapping with Legs here, 
    as one feet can be assigned to many legs
    """
    feet = models.ForeignKey(Feet, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=200,
                            unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    """
    Creating one to one mapping with Legs here, 
    as one leg can be assigned to only one table
    """
    leg = models.OneToOneField(
        Leg, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
