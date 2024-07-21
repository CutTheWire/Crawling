import os
import smtplib
from dotenv import load_dotenv
from datetime import datetime
from threading import local

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional

import mysql.connector
from mysql.connector import Error

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path)
local_conn = local()

# 데이터베이스 연결 설정
db_config = {
    'host': 'mysql',  # MySQL 서비스 이름
    'user': os.getenv('MYSQL_ROOT_USER', 'root'),  # 기본 사용자 'root'
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE', 'email_db'),  # 기본 데이터베이스 이름
    'port': '3306'  # 기본 포트
}



# SMTP 설정 (Outlook)
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')

# Pydantic 모델
class EmailSend(BaseModel):
    subject: str
    body: str
    recipient_email: str

class Queries:
    def __init__(self):
        self._local_conn = None

    @property
    def local_conn(self):
        if self._local_conn is None or not self._local_conn.is_connected():
            self._local_conn = mysql.connector.connect(**db_config)
        return self._local_conn

    def save_email(self, subject, body, recipient_email, sender_email, file_name):
        now = datetime.now()
        cursor = self.local_conn.cursor()
        cursor.execute("INSERT INTO emails (subject, body, recipient_email, sender_email, file_name, sent_at) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (subject, body, recipient_email, sender_email, file_name, now))
        self.local_conn.commit()
        cursor.close()

db_queries = Queries()

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), "cut.ico"))

@app.get("/robots.txt")
async def get_robots():
    return FileResponse(os.path.join(script_dir, "robots.txt"))

@app.get("/")
def main():
    try:
        with open(os.path.join(script_dir, "index.html"), "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return {"message": "This server is an Email"}

@app.post("/send_email")
async def send_email(
    subject: str = Form(...),
    body: str = Form(...),
    recipient_email: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    email = EmailSend(
        subject=subject,
        body=body,
        recipient_email=recipient_email,
    )

    try:
        msg = MIMEMultipart()
        msg['Subject'] = email.subject
        msg['From'] = smtp_username  # 발신자 이메일을 SMTP 사용자명으로 설정
        msg['To'] = email.recipient_email

        msg.attach(MIMEText(email.body, 'plain'))

        if file:
            part = MIMEApplication(await file.read(), Name=file.filename)
            part['Content-Disposition'] = f'attachment; filename="{file.filename}"'
            msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()  # TLS 시작
            smtp.login(smtp_username, smtp_password)  # 로그인
            smtp.send_message(msg)  # 메시지 전송

        file_name = file.filename if file else None
        db_queries.save_email(email.subject, email.body, email.recipient_email, smtp_username, file_name)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Email sent successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
