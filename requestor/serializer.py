from rest_framework import serializers
from authentication.models import *
from .models import *
from director.models import *
from utility.models import *


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

    def orginizationupdate(self, instance, validated_data):
        organization_data = validated_data.pop("organization", None)
        if organization_data:
            if instance.organization:
                # Update existing organization
                organization_instance = instance.organization
                organization_instance.name = organization_data.get(
                    "name", organization_instance.name
                )
                organization_instance.email = organization_data.get(
                    "email", organization_instance.email
                )
                organization_instance.address = organization_data.get(
                    "address", organization_instance.address
                )
                organization_instance.established_date = organization_data.get(
                    "established_date", organization_instance.established_date
                )

                organization_instance.save()
                print(f"Updated organization: {organization_instance}")

        return instance


class RequestorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=100, required=False, allow_null=True, write_only=True
    )
    last_name = serializers.CharField(
        max_length=100, required=False, allow_null=True, write_only=True
    )
    password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)

    organization = OrganizationSerializer(required=False, allow_null=True)

    class Meta:
        model = Requestor
        fields = ["id", "first_name", "last_name", "email", "password", "organization"]

    def create(self, validated_data):
        organization_data = validated_data.pop("organization", None)
        # organization_data.pop("requestor", None)

        if organization_data:
            organization_data.pop("requestor", None)

        # Extract user data including email
        user_data = {
            "first_name": validated_data.pop("first_name", None),
            "last_name": validated_data.pop("last_name", None),
            "password": validated_data.pop("password"),
            "email": validated_data.pop("email"),
        }

        role, _ = Role.objects.get_or_create(name="REQUESTOR")

        # Create or retrieve the User
        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "password": user_data["password"],
                "role": role,  # Assign the role directly
            },
        )

        # Create the Requestor instance
        requestor = Requestor.objects.create(user=user, **validated_data)

        # Create Organization if organization_data is provided
        if organization_data:
            organization_instance = Organization.objects.create(
                requestor=requestor, **organization_data
            )

        return requestor

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.organization)
        representation.update(
            {
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
                "email": instance.user.email,
                # "role": instance.user.role.name,
            }
        )
        return representation

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", None)

        print(user_data)

        if user_data:
            email = user_data.get("email")
            if email:
                try:
                    user_instance = User.objects.get(email=email)
                    instance.user = user_instance
                    user_instance.first_name = user_data.get(
                        "first_name", user_instance.first_name
                    )
                    user_instance.last_name = user_data.get(
                        "last_name", user_instance.last_name
                    )
                    user_instance.email = email
                    if "password" in user_data:
                        user_instance.set_password(user_data["password"])

                    user_instance.save()
                    print(f"Updated user: {user_instance}")

                except User.DoesNotExist:
                    print(f"User with email {email} does not exist.")

        instance.user.first_name = validated_data.get(
            "first_name", instance.user.first_name
        )
        instance.user.last_name = validated_data.get(
            "last_name", instance.user.last_name
        )
        instance.user.email = validated_data.get("email", instance.user.email)
        instance.save()
        print(f"Updated requestor: {instance}")
        return instance


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ["geometry"]


class GeometrySerializer(serializers.ModelSerializer):
    files = FileSerializer(
        required=False,
        allow_null=True,
        many=True,
        allow_empty=True,
    )

    class Meta:
        model = Geometry
        fields = "__all__"
        read_only_fields = ["quotation"]


class QuotationObjectDimensionSerializer(serializers.Serializer):
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    dimension = serializers.PrimaryKeyRelatedField(queryset=Dimension.objects.all())
    value = serializers.IntegerField()


class QuotationTestParameterSerializer(serializers.Serializer):
    test_parameter = serializers.PrimaryKeyRelatedField(
        queryset=TestParameter.objects.all()
    )
    test_parameter_value = serializers.IntegerField()
    unit_dimension = serializers.PrimaryKeyRelatedField(
        queryset=UnitDimension.objects.all()
    )


class QuotationObjectDetailSerializer(serializers.Serializer):
    test_object = serializers.PrimaryKeyRelatedField(
        queryset=TestObject.objects.all(),
    )
    test_object_quantity = serializers.IntegerField()
    test_condition = serializers.PrimaryKeyRelatedField(
        queryset=Condition.objects.all(),
    )
    test_condition_value = serializers.IntegerField()
    unit_dimension = serializers.PrimaryKeyRelatedField(
        queryset=UnitDimension.objects.all(),
    )
    object_dimension = QuotationObjectDimensionSerializer(many=True)
    test_parameters = QuotationTestParameterSerializer(many=True)


class QuotationDetailSerializer(serializers.ModelSerializer):

    test_objects = QuotationObjectDetailSerializer(many=True, write_only=True)

    class Meta:
        model = QuotationDetail
        fields = [
            "test",
            "test_objects",
        ]


class QuotationSerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(
        required=False,
        allow_null=True,
        many=True,
        allow_empty=True,
    )
    details = QuotationDetailSerializer(required=False, many=True)

    class Meta:
        model = Quotation
        fields = "__all__"
        read_only_fields = ["status"]

    def create(self, validated_data):
        print("\n\n", validated_data, "\n\n")

        details = validated_data.pop("details", None)
        geometry = validated_data.pop("geometry", None)

        status = QuotationStatus.objects.get(name="Pending")
        quotation = Quotation.objects.create(status=status, **validated_data)
        print("\n\n", details, "\n\n")

        if details:
            for detail in details:
                print("\n\n", detail, "\n\n")

                for test_object in detail["test_objects"]:
                    print("\n\n", test_object, "\n\n")
                    test_parameters = test_object.pop("test_parameters", [])
                    object_dimensions = test_object.pop("object_dimension", [])

                    quotation_detail = QuotationDetail.objects.create(
                        quotation=quotation, test=detail["test"], **test_object
                    )
                    quotation_detail.save()

                    for test_parameter in test_parameters:
                        QuotationTestParameter.objects.create(
                            quotation_detail=quotation_detail,
                            **test_parameter,
                        ).save()

                    for object_dimension in object_dimensions:

                        unit_dimension = UnitDimension.objects.filter(
                            unit=object_dimension["unit"]
                        ) & UnitDimension.objects.filter(
                            dimension=object_dimension["dimension"]
                        )

                        if unit_dimension:
                            print(unit_dimension)

                            QuotationObjectDimension.objects.create(
                                quotation_detail=quotation_detail,
                                unit_dimension=unit_dimension[0],
                                dimension_value=object_dimension["value"],
                            ).save()

        quotation.save()
        return quotation

    def to_representation(self, instance):

        representation = {}
        representation["id"] = instance.id
        representation["requestor"] = instance.requestor.user.email
        representation["status"] = instance.status.name
        representation["date_created"] = instance.date_created
        representation["base_metal_alloy"] = instance.base_metal_alloy
        representation["alloy"] = instance.alloy

        if instance.geometry:
            representation["geometry"] = []

            for geometry in instance.geometry.all():
                representation["geometry"].append(geometry.__dict__)

        if instance.details:
            representation["details"] = []

            unique_tests = instance.details.all().values("test").distinct()

            for test in unique_tests:
                obj = {
                    "test": Test.objects.get(pk=test["test"]).name,
                    "test_objects": [],
                }

                test_details = instance.details.filter(test=test["test"])

                representation["details"].append(obj)
                for test_detail in test_details:
                    test_detail_obj = {
                        "test_object": test_detail.test_object.name,
                        "test_object_quantity": test_detail.test_object_quantity,
                        "test_condition": test_detail.test_condition.name,
                        "test_condition_value": test_detail.test_condition_value,
                        "unit_dimension": test_detail.unit_dimension.unit.name
                        + " - "
                        + test_detail.unit_dimension.dimension.name,
                        "quotation_object_dimension": [
                            {
                                "unit": object_dimension.unit_dimension.unit.name,
                                "dimension": object_dimension.unit_dimension.dimension.name,
                                "value": object_dimension.dimension_value,
                            }
                            for object_dimension in test_detail.object_dimensions.all()
                        ],
                        "quotation_test_parameter": [
                            {
                                "test_parameter": test_parameter.test_parameter.name,
                                "test_parameter_value": test_parameter.test_parameter_value,
                                "unit": test_parameter.unit_dimension.unit.name,
                                "dimension": test_parameter.unit_dimension.dimension.name,
                            }
                            for test_parameter in test_detail.test_parameters.all()
                        ],
                    }

                    obj["test_objects"].append(test_detail_obj)

        return representation
