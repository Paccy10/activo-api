from rest_framework import serializers
from django.core.mail import EmailMessage
from django.utils.html import strip_tags


def check_unique_value(model, field, value, errors):
    kwargs = {field: value}
    if model.objects.filter(**kwargs).exists():
        raise serializers.ValidationError(errors[field]["unique"])


def send_email(subject, message, to):
    email_message = EmailMessage(subject, message, to=to)
    email_message.content_subtype = "html"
    email_message.send()
