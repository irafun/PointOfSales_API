from rest_framework.serializers import *

class ErrorSerializer(Serializer):
    error = CharField(max_length=1024)

class SuccessSerializer(Serializer):
    detail = CharField(max_length=1024)