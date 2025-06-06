import random
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .core.models.services.whatsapp_verification import WhatsAppVerification
from .core.serializers.services.whatsapp_verification import SendCodeSerializer, VerifyCodeSerializer

WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/<YOUR_PHONE_NUMBER_ID>/messages"
ACCESS_TOKEN = "<YOUR_PERMANENT_ACCESS_TOKEN>"
TEMPLATE_NAME = "codigo_verificacao"
LANGUAGE = "pt_BR"

class SendCodeView(APIView):
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        code = str(random.randint(10000, 99999))
        WhatsAppVerification.objects.create(phone_number=phone, code=code)

        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "template",
            "template": {
                "name": TEMPLATE_NAME,
                "language": {"code": LANGUAGE},
                "components": [{
                    "type": "body",
                    "parameters": [{"type": "text", "text": code}]
                }]
            }
        }

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        r = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

        if r.status_code == 200:
            return Response({"message": "Código enviado"})
        return Response({"error": "Erro ao enviar WhatsApp", "detail": r.json()}, status=500)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        try:
            record = WhatsAppVerification.objects.filter(phone_number=phone, code=code).latest('created_at')
        except WhatsAppVerification.DoesNotExist:
            return Response({"error": "Código inválido"}, status=400)

        if not record.is_valid():
            return Response({"error": "Código expirado"}, status=400)

        return Response({"message": "Código verificado com sucesso!"})
