from twilio.rest import Client
from src.utils.config import Settings

settings = Settings()


class TwilioClient:

    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID,
                             settings.TWILIO_AUTH_TOKEN)

    def send_message(self, to: str, **kwargs: str | dict) -> None:
        """
        Envía un mensaje de WhatsApp usando Twilio.

        Parámetros:
        - to (str): Número de teléfono del destinatario (formato internacional).
        - kwargs:
            - body (str, opcional): Mensaje de texto a enviar.
            - contentId (str, opcional): ID de contenido para usar una plantilla de Twilio.
            - variables (dict, opcional): Variables dinámicas para la plantilla (si se usa `contentId`).
        """
        message_data = {
            "from_": f'whatsapp:{settings.TWILIO_SENDER_NUMBER}',
            "to": f'whatsapp:{to}',
        }

        if 'body' in kwargs:
            message_data["body"] = kwargs["body"]
        elif 'contentId' in kwargs:
            message_data["content_sid"] = kwargs["contentId"]
            if 'variables' in kwargs:
                message_data["content_variables"] = kwargs["variables"]

        self.client.messages.create(**message_data)

    def verify_user(self) -> bool:
        """
        Envía un mensaje de WhatsApp con un código de verificación.

        Parámetros:
        - to (str): Número de teléfono del destinatario (formato internacional).
        - code (str): Código de verificación.
        """
        account = self.client.api.v2010.accounts(
            settings.TWILIO_ACCOUNT_SID).fetch()

        return account.status == 'active'
