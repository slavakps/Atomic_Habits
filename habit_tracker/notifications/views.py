import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ConnectTelegramView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"

        response = requests.get(url).json()

        if not response.get("result"):
            return Response({"error": "Отправьте любое сообщение боту в Telegram и попробуйте снова"}, status=400)

        last_message = response["result"][-1]
        chat_id = last_message["message"]["chat"]["id"]

        request.user.tg_chat_id = chat_id
        request.user.save()

        return Response({"chat_id": chat_id})
