
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime, timedelta
import os

app = Flask(__name__)
sessions = {}

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    from_number = request.form.get("From")
    body = request.form.get("Body").strip().lower()
    now = datetime.utcnow()

    last_seen = sessions.get(from_number)
    sessions[from_number] = now

    response = MessagingResponse()
    msg = response.message()

    if last_seen is None or (now - last_seen).total_seconds() > 1200:  # 20 minutos
        bienvenida = (
            "Hola! Bienvenido a La Casa de la Suerte. Gracias por tu mensaje.\n"
            "Estas con ganas de ganar hoy?🤑\n"
            "Para jugar selecciona la opción que desees a continuación:\n"
            "1 Quiniela\n"
            "2 Quiniela Plus\n"
            "3 Instantánea\n"
            "4 Bailarina\n"
            "5 Tele Kino\n"
            "6 Tarasca\n"
            "7 Quini 6\n"
            "8 Brinco\n"
            "9 Loto Plus\n"
            "10 Money\n\n"
            "Para dudas/consultas escribí 11"
        )
        msg.body(bienvenida)
    else:
        if body in [str(i) for i in range(1, 12)]:
            msg.body(f"Recibimos tu selección: opción {body}. Pronto recibirás más detalles.")
        else:
            msg.body("⚠️ Opción inválida. Por favor escribí un número del 1 al 10, o 11 para consultas.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
