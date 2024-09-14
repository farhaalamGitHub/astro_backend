from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class UnitDimension(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    dimension = models.ForeignKey("Dimension", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dimension} - {self.unit}"


class Dimension(models.Model):
    name = models.CharField(max_length=250)
    units = models.ManyToManyField(
        Unit, through=UnitDimension, related_name="dimension"
    )

    def __str__(self):
        return self.name


class QuotationStatus(models.Model):
    name = models.CharField(max_length=250)
    step = models.IntegerField()

    def __str__(self):
        return self.name
