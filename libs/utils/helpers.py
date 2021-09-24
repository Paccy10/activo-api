from rest_framework import serializers


def check_unique_value(model, field, value, errors):
    kwargs = {field: value}
    if model.objects.filter(**kwargs).exists():
        raise serializers.ValidationError(errors[field]["unique"])
