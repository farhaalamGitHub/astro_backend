from django.db import models


class Requestor(models.Model):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Organization(models.Model):
    requestor = models.OneToOneField(
        Requestor, null=True, on_delete=models.DO_NOTHING, related_name="organization"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    established_date = models.DateField()

    def __str__(self):
        return self.email


class Quotation(models.Model):
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    status = models.ForeignKey(
        "utility.QuotationStatus",
        on_delete=models.SET_NULL,
        null=True,
        related_name="quotations",
    )
    base_metal_alloy = models.CharField(max_length=250)
    alloy = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id} - {self.requestor} - {self.date_created}"


class QuotationDetail(models.Model):
    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name="details"
    )
    test = models.ForeignKey("director.Test", on_delete=models.CASCADE)
    test_condition = models.ForeignKey("director.Condition", on_delete=models.CASCADE)
    test_condition_value = models.CharField(max_length=250)
    test_object = models.ForeignKey("director.TestObject", on_delete=models.CASCADE)
    test_object_quantity = models.IntegerField()
    unit_dimension = models.ForeignKey(
        "utility.UnitDimension", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.test_object} - {self.quotation}"


class QuotationTestParameter(models.Model):
    quotation_detail = models.ForeignKey(
        QuotationDetail, on_delete=models.CASCADE, related_name="test_parameters"
    )
    test_parameter = models.ForeignKey(
        "director.TestParameter", on_delete=models.CASCADE
    )
    test_parameter_value = models.CharField(max_length=250)
    unit_dimension = models.ForeignKey(
        "utility.UnitDimension", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.test_parameter} - {self.quotation_detail}"


class QuotationObjectDimension(models.Model):
    quotation_detail = models.ForeignKey(
        QuotationDetail, on_delete=models.CASCADE, related_name="object_dimensions"
    )
    unit_dimension = models.ForeignKey(
        "utility.UnitDimension", on_delete=models.CASCADE
    )
    dimension_value = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.unit_dimension} - {self.quotation_detail}"


class Geometry(models.Model):
    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name="geometry"
    )
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.description


class File(models.Model):
    geometry = models.ForeignKey(
        Geometry, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField()

    def __str__(self):
        return f"File {self.id}"
