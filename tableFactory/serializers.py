from rest_framework import serializers

from tableFactory.models import Feet, Leg, Table


class FeetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    width = serializers.IntegerField(required=False, allow_null=True)
    length = serializers.IntegerField(required=False, allow_null=True)
    radius = serializers.IntegerField(required=False, allow_null=True)
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)

    """
    1. A foot with a radius must not have length or width
    2. A foot with a length must also have a width
    3. A foot with a width must also have a length 
    """
    def validate(self, data):
        if 'radius' in data and data['radius'] is not None:
            if (('length' in data and data['length'] is not None) or
                    ('width' in data and data['width'] is not None)):
                raise serializers.ValidationError(
                    "A foot with a radius must not have length or width")
        elif 'length' in data and data['length'] is not None:
            if 'width' not in data or data['width'] is None:
                raise serializers.ValidationError(
                    "A foot with a length must also have a width")
        elif 'width' in data and data['width'] is not None:
            if 'length' not in data or data['length'] is None:
                raise serializers.ValidationError(
                    "A foot with a width must also have a length")
        return data

    # DRF serializer.save() calls self.create(self.validated_data)
    def create(self, validated_data):
        return Feet.objects.create(**validated_data)

    # Add update() implementation on FeetSerializer
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LegSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Leg.objects.create(**validated_data)

    # Add update() implementation on LegSerializer
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LegRetrieveSerializer(serializers.ModelSerializer):
    feet = FeetSerializer

    class Meta:
        model = Leg
        fields = ('name', 'created_date', 'updated_date', 'feet')
        read_only = ('name', 'created_date', 'updated_date', 'feet')


class TableSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Table.objects.create(**validated_data)

    # Add update() implementation on TableSerializer
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class TableRetrieveSerializer(serializers.ModelSerializer):
    leg = LegSerializer

    class Meta:
        model = Table
        fields = ('name', 'created_date', 'updated_date', 'leg')
        read_only = ('name', 'created_date', 'updated_date', 'leg')
