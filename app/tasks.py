import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pytz
import schedule
import time
from django.template.loader import render_to_string
from app.settings import *
from erp.userauths.models import Deuda
from django.utils import timezone
from datetime import date, timedelta


def enviar_correos():
        # Obtener las nuevas deudas
        # deudas_hoy = Deuda.objects.all()
        
        # # Enviar correo a cada usuario con nuevas deudas
        # for deuda in deudas_hoy:
        #     send_email(deuda)

         # Obtener la fecha actual
     # Obtener la fecha actual
    # Obtener la zona horaria de Perú
    zona_horaria_peru = pytz.timezone('America/Lima')

    # Obtener la fecha actual en la zona horaria de Perú
    fecha_actual = timezone.now().astimezone(zona_horaria_peru).date()

    print(fecha_actual)
    
    # Obtener todas las deudas
    todas_deudas = Deuda.objects.all()

    # Iterar sobre todas las deudas y enviar correos basados en la fecha de vencimiento
    for deuda in todas_deudas:
        if deuda.fecha_vencimiento is not None:  # Verificar si la fecha de vencimiento no es None
            dias_hasta_vencimiento = (deuda.fecha_vencimiento - fecha_actual).days
            print(dias_hasta_vencimiento)

            if deuda.estado == 'pendiente':  
                if dias_hasta_vencimiento == 7:
                    message1 = 'Su deuda vencerá en 7 días'
                    message2 = 'vencerá en 7 días '
                    send_email(deuda, message1, message2)
                elif dias_hasta_vencimiento == 1:
                    message1 = 'Su deuda vencerá en 1 día'
                    message2 = 'vencerá en 1 día'
                    send_email(deuda, message1, message2)
                elif dias_hasta_vencimiento <= 0:  
                    message1 = 'Su deuda venció'
                    message2 = 'ha vencido '
                    send_email(deuda, message1, message2)
                    deuda.estado = 'vencido'  
                    deuda.save()  


def send_email(deuda, message1, message2):
        try:
            mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Construir el mensaje
            email_to=deuda.contribuyente.user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = email_to 
            mensaje['Subject'] = message1
            mensaje['X-Custom-Header'] = 'Deuda en el Sistema de Predios'

            content= render_to_string("email.html", {"user": deuda.contribuyente.user,"contrib": deuda.contribuyente ,
                                                     "img":"https://elnuevoempresario.com/wp-content/uploads/2023/02/deuda.jpg", 
                                                     "title":" Deuda",
                                                     "message": "Su deuda registrada por "+str(deuda.tipo_deuda)+" con un monto de S/ "+ str(deuda.monto_deuda) +" "+ str(message2)
                                                      + ". Fecha de vencimiento : "+ str(deuda.fecha_vencimiento) })

            # Adjuntamos el texto
            mensaje.attach(MIMEText(content,'html', 'utf-8'))
            # Enviar el correo electrónico
            mailServer.sendmail(EMAIL_HOST_USER, email_to, mensaje.as_string())
            
            # Cerrar la conexión con el servidor SMTP
            mailServer.quit()
            
            print("Correo enviado correctamente " + str(deuda.id))
            
        except Exception as e:
            print("Error al enviar el correo:", e)

schedule.every().day.at("20:17").do(enviar_correos)
#schedule.every(1).minutes.do(enviar_correos)

# Ejecutar el planificador en un bucle infinito
while True:
    schedule.run_pending()
    time.sleep(1) 