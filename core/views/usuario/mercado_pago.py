# views.py
import mercadopago
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings

class CreatePreferenceView(APIView):
    permission_classes = [AllowAny]  # Ajuste conforme necessário

    def post(self, request):
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        items = request.data.get("items", [])
        preference_data = {
            "items": items,
            "back_urls": {
                "success": "https://seusite.com/success",
                "failure": "https://seusite.com/failure",
                "pending": "https://seusite.com/pending"
            },
            "auto_return": "approved",
        }

        preference_response = sdk.preference().create(preference_data)
        return Response(preference_response["response"])
