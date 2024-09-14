from rest_framework import serializers
from .models import *

# ---------- Create ConditionSerializer --------


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = "__all__"


# ---------- Create TestObjectSerializer --------


class TestObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestObject
        fields = "__all__"


# ---------- Create TestSerializer --------


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class AlloySerializer(serializers.ModelSerializer):
    class Meta:
        model = Alloy
        fields = "__all__"


from rest_framework import serializers
from .models import *

# ---------- Create TestCategorySerializer --------


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = "__all__"
