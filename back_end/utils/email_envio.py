import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from back_end.models.login_models import Login
from datetime import datetime, timedelta

#Função para configuração para e enviar e-mail de recuperação de senha
def enviar_email_recuperacao(db: Session, usuario_id: int, assunto: str, corpo: str):
    login = db.query(Login).filter(Login.id_login == usuario_id).first()

    if login:
        token = atualizar_token_recuperacao(db, usuario_id)
        link = f'http://localhost:8000/recuperar-senha?token={token}'
        corpo_completo = f'{corpo}\n\nClique no link para recuperar sua senha: {link}'

        # Enviar o e-mail
        msg = MIMEMultipart()
        msg['From'] = 'NafUnifeso@unifeso.com'  
        msg['To'] = login.email  
        msg['Subject'] = assunto  
        msg.attach(MIMEText(corpo_completo, 'plain'))

        try:
            servidor = smtplib.SMTP('localhost', 1025)  # MailHog rodando na porta 1025
            servidor.sendmail(msg['From'], msg['To'], msg.as_string())
            servidor.quit()
            print("E-mail de recuperação enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
    else:
        print("Usuário não encontrado!")


#função para gerar token seguro
def gerar_token_recuperacao():
    token = secrets.token_urlsafe(16) 
    return token

#Função para atualizar o token de recuperação de senha
def atualizar_token_recuperacao(db: Session, usuario_id: int):
    token = gerar_token_recuperacao()
    expiracao = datetime.utcnow() + timedelta(minutes=5)
    login = db.query(Login).filter(Login.id_login == usuario_id).first()
    
    if login:
        login.token_recuperacao = token
        login.expiracao_token_recuperacao = expiracao
        db.commit()  # Salvar no banco de dados
        return token
    else:
        raise Exception("Usuário não encontrado!")




