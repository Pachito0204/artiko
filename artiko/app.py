import os
from flask import Flask, send_from_directory, request, jsonify, render_template_string
from pathlib import Path
import csv, datetime, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # load variables from .env in dev

app = Flask(__name__, static_folder='static', template_folder='.')


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    name = data.get('name','').strip()
    email = data.get('email','').strip()
    message = data.get('message','').strip()

    if not name or not email or not message:
        return jsonify({'error':'Nombre, email y mensaje son obligatorios.'}), 400

    out_dir = Path('data')
    out_dir.mkdir(exist_ok=True)
    csv_file = out_dir / 'contacts.csv'
    header = ['timestamp','name','email','phone','company','message']
    row = [datetime.datetime.utcnow().isoformat(),
           name,
           email,
           data.get('phone','').strip(),
           data.get('company','').strip(),
           message]
    write_header = not csv_file.exists()
    with csv_file.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)

    # Try to send email via SMTP (if configured)
    mail_server = os.getenv('MAIL_SERVER')
    mail_port = int(os.getenv('MAIL_PORT') or 0)
    mail_user = os.getenv('MAIL_USER')
    mail_pass = os.getenv('MAIL_PASS')
    mail_to = os.getenv('MAIL_TO') or mail_user

    if mail_server and mail_port and mail_user and mail_pass and mail_to:
        try:
            msg = EmailMessage()
            msg['Subject'] = f"[Artiko] Nuevo contacto: {name}"
            msg['From'] = mail_user
            msg['To'] = mail_to
            body = f"Nombre: {name}\nEmail: {email}\nTelefono: {data.get('phone','')}\nEmpresa: {data.get('company','')}\n\nMensaje:\n{message}"
            msg.set_content(body)

            with smtplib.SMTP(mail_server, mail_port, timeout=10) as smtp:
                smtp.starttls()
                smtp.login(mail_user, mail_pass)
                smtp.send_message(msg)
        except Exception as e:
            # Log error to file
            errlog = out_dir / 'mail_errors.log'
            with errlog.open('a', encoding='utf-8') as ef:
                ef.write(f"{datetime.datetime.utcnow().isoformat()} - mail send failed: {e}\n")
            # still return ok because contact saved
    return jsonify({'ok':True}), 200


if __name__ == '__main__':
    # For local development: set FLASK_ENV=development and create a .env file
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=True)
