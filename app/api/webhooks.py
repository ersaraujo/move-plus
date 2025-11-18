# app/api/webhooks.py

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import Response

from .. import crud # Necessário para o handle_user
from ..database import get_db

# NOTA: O prefixo é '/webhooks' e será usado no ngrok
router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks (Chatbot & Pagamento)"],
)

# ===============================================
# WEBHOOK 1: ENTRADA DE MENSAGEM DO WHATSAPP (TWILIO)
# ===============================================

@router.post("/whatsapp/inbound")
async def handle_whatsapp_message(
    From: str = Form(...), 
    Body: str = Form(...), 
    db: Session = Depends(get_db)
):
    """
    Recebe o Webhook de mensagens do Twilio e testa o fluxo de resposta.
    """
    # 1. Lógica de Busca/Criação de Usuário
    phone_number = From.replace("whatsapp:", "")
    
    user = crud.handle_user_on_inbound(db, phone_number, default_class_id=1) 
    
    # 2. Resposta via Twilio (usando o Twiml)
    response = MessagingResponse() 
    
    if user.status == "INITIAL":
        crud.update_user_status(db, user, new_status="AWAITING_NAME")
        
        msg = (f"🎉 Olá, bem-vindo(a) ao Move+! 🎉\n\n"
               f"Seu número ({phone_number}) foi registrado.\n"
               f"Status inicial: {user.status} -> (Atualizado para AWAITING_NAME)\n\n"
               f"Responda com seu nome para continuarmos o cadastro de teste.")
        response.message(msg)
        
    elif user.status == "AWAITING_NAME":
        user_name = Body.strip()
        crud.update_user_status(db, user, new_status="AWAITING_PAYMENT")
        
        msg = (f"Obrigado, {user_name}! Seu nome foi salvo.\n"
               f"Próxima etapa: Geração de Link de Pagamento.\n"
               f"Esta etapa será implementada em seguida!")
        response.message(msg)
    
    else:
        # Resposta genérica para outros estados
        response.message(f"Seu status atual é: {user.status}. Responda 'INICIAR' para recomeçar o teste.")
    
    print(f"Resposta TwiML gerada: {response}")
    return Response(content=str(response), media_type="text/xml")

# Rotas de Pagamento e Outros Webhooks permanecem comentadas/removidas por enquanto
# ...