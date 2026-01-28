from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from datetime import datetime
import uuid

api = Namespace(
    "qa-emails",
    description="Sistema de QA para revisão e classificação de e-mails por IA",
    path="/qa/emails"
)
# ========= MODELOS ========= #

email_thread_model = api.model("EmailThread", {
    "thread_id": fields.String(
        required=False,
        description="ID da thread (opcional, gerado se não enviado)"
    ),
    "subject": fields.String(required=True, description="Assunto do e-mail"),
    "messages": fields.List(
        fields.String,
        required=True,
        description="Lista de mensagens do thread (ordem cronológica)"
    )
})

qa_result_model = api.model("QAResult", {
    "thread_id": fields.String,
    "labels": fields.List(fields.String),
    "confidence": fields.Float,
    "issues": fields.List(fields.String),
    "reviewed_at": fields.String
})

# ========= MOCK DA IA ========= #
def run_ai_review(thread_data):
    """
    Aqui entra sua IA real (OpenAI, Azure, local, etc).
    Por enquanto, é um mock estruturado.
    """

    text = " ".join(thread_data["messages"]).lower()

    labels = []
    issues = []

    if "erro" in text or "problema" in text:
        labels.append("problema_tecnico")
        issues.append("Cliente relata erro ou falha")

    if "urgente" in text:
        labels.append("urgente")

    if "reclamação" in text or "insatisfeito" in text:
        labels.append("reclamacao")
        issues.append("Tom negativo detectado")

    if not labels:
        labels.append("neutro")

    return {
        "labels": labels,
        "confidence": round(0.75 + (0.05 * len(labels)), 2),
        "issues": issues
    }

# ========= ENDPOINTS ========= #

@api.route("/review")
class ReviewEmail(Resource):
    @api.expect(email_thread_model)
    @api.marshal_with(qa_result_model)
    def post(self):
        """
        Executa a revisão QA de um thread de e-mail usando IA
        """
        data = request.json

        thread_id = data.get("thread_id", str(uuid.uuid4()))

        ai_result = run_ai_review(data)

        return {
            "thread_id": thread_id,
            "labels": ai_result["labels"],
            "confidence": ai_result["confidence"],
            "issues": ai_result["issues"],
            "reviewed_at": datetime.utcnow().isoformat()
        }, 200


@api.route("/checklist")
class QAChecklist(Resource):
    def get(self):
        """
        Checklist padrão do Analista QA
        """
        return {
            "checks": [
                "Tom adequado",
                "Resposta completa",
                "Ausência de informações sensíveis",
                "Classificação correta",
                "Encaminhamento apropriado"
            ]
        }, 200
