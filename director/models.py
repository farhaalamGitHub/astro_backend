from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Admin(models.Model):
    user = models.OneToOneField("authentication.User", on_delete=models.DO_NOTHING)
    phone_no = models.CharField(max_length=250)
    
    def __str__(self):
        return self.user.email


class Alloy(MPTTModel):
    name = models.CharField(max_length=250, blank=False, null=False)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    @classmethod
    def get_parent_level_alloys(cls):
        top_level_alloys = cls.objects.filter(parent__isnull=True)
        return top_level_alloys

    @classmethod
    def get_children_alloys(cls, parent_alloy_id):
        try:
            parent_alloy = cls.objects.get(id=parent_alloy_id)
            children_alloys = parent_alloy.get_descendants(include_self=False)
            return children_alloys
        except cls.DoesNotExist:
            return None


class TestCategory(MPTTModel):
    name = models.CharField(max_length=250, blank=False, null=False)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Test Category"
        verbose_name_plural = "Test Categories"


class Test(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE)
    conditions = models.ManyToManyField("Condition", related_name="tests")

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=250)
    upper_limit = models.CharField(max_length=250)
    lower_limit = models.CharField(max_length=250)
    unit_dimension = models.ForeignKey(
        "utility.UnitDimension", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class TestParameter(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    upper_limit = models.CharField(max_length=250)
    lower_limit = models.CharField(max_length=250)
    unit_dimension = models.ForeignKey(
        "utility.UnitDimension", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class TestObject(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class StanderdTestObjectDimension(models.Model):
    test_object = models.ForeignKey(TestObject, on_delete=models.CASCADE)
    size_name = models.CharField(max_length=250)
    dimension_value = models.FloatField()
    unit_dimension = models.ForeignKey(
        "utility.UnitDimension", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.size_name
