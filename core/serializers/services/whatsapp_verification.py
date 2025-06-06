from rest_framework import serializers

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()