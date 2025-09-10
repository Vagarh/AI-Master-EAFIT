import os
import smtplib
from email.message import EmailMessage

def send_email(to_addr, subject, body, attachment_data=None, attachment_filename=None, attachment_mimetype=None):
    # 1. Validar variables de entorno
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    pwd  = os.getenv("SMTP_PASS")
    port_str = os.getenv("SMTP_PORT", "587")

    missing_vars = []
    if not host: missing_vars.append("SMTP_HOST")
    if not user: missing_vars.append("SMTP_USER")
    if not pwd: missing_vars.append("SMTP_PASS")
    
    if missing_vars:
        return False, f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}"

    if not to_addr:
        return False, "No se ha proporcionado una dirección de correo de destino."

    try:
        port = int(port_str)
    except ValueError:
        return False, f"El valor de SMTP_PORT ('{port_str}') no es un número válido."

    # 2. Construir y enviar el correo
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_data and attachment_filename and attachment_mimetype:
        maintype, subtype = attachment_mimetype.split('/', 1)
        msg.add_attachment(attachment_data,
                           maintype=maintype,
                           subtype=subtype,
                           filename=attachment_filename)
    try:
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
        return True, "Correo enviado con éxito."
    except smtplib.SMTPAuthenticationError:
        return False, "Fallo de autenticación. Revisa SMTP_USER y SMTP_PASS."
    except smtplib.SMTPConnectError:
        return False, f"No se pudo conectar al servidor SMTP en {host}:{port}. Revisa SMTP_HOST y SMTP_PORT."
    except Exception as e:
        return False, f"Ocurrió un error inesperado al enviar el correo: {e}"
