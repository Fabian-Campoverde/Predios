from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.template.loader import render_to_string

from erp.userauths.models import Deuda
from erp.dashboard.forms import DeudaForm
from app.settings import *
# from background_task import background
# from django.contrib.auth.models import User

# @background(schedule=60)
# def notify_user(user_id):
#     # lookup user by id and send them a message
#     user = User.objects.get(pk=user_id)
#     user.email_user('Here is a notification', 'You have been notified')


class DeudasView(PermissionRequiredMixin, ListView):
    permission_required = 'view_contribuyente'
    model = Deuda
    template_name = 'deudas.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Deudas'
        context['create_url'] = reverse_lazy('new')
        context['entity'] = 'Deudas'
        return context
    
    

class NewDeuda(PermissionRequiredMixin, CreateView):
    permission_required = 'view_contribuyente'
    model = Deuda
    template_name = 'new.html'
    form_class = DeudaForm
    success_url = reverse_lazy('deudas')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Deuda'
        context['entity'] = 'Deudas'
        context['create_url'] = reverse_lazy('newpredio')
        context['list_url'] = reverse_lazy('deudas')
        context['action'] = 'add'
        return context
    
    def send_email(self, deuda):
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
            mensaje['Subject'] = "Tienes una nueva deuda registrada"
            mensaje['X-Custom-Header'] = 'Deuda en el Sistema de Predios'

            content= render_to_string("email.html", {"user": deuda.contribuyente.user,"contrib": deuda.contribuyente ,
                                                     "img":"https://elnuevoempresario.com/wp-content/uploads/2023/02/deuda.jpg", 
                                                     "title":"nueva deuda",
                                                     "message": "Nueva deuda registrada por un monto de S/ "+ str(deuda.monto_deuda)})

            # Adjuntamos el texto
            mensaje.attach(MIMEText(content,'html'))
            # Enviar el correo electrónico
            mailServer.sendmail(EMAIL_HOST_USER, email_to, mensaje.as_string())
            
            # Cerrar la conexión con el servidor SMTP
            mailServer.quit()
            
            print("Correo enviado correctamente")
            
        except Exception as e:
            print("Error al enviar el correo:", e)

    def form_valid(self, form):
        # Guardar la deuda
        deuda = form.save()

        # Enviar correo electrónico al deudor
        self.send_email(deuda)

        return super().form_valid(form)

class EditDeuda(PermissionRequiredMixin, UpdateView):
    permission_required = 'view_contribuyente'
    model = Deuda
    template_name = 'edit.html'
    form_class = DeudaForm
    success_url = reverse_lazy('deudas')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una deuda'
        context['list_url'] = reverse_lazy('deudas')
        context['entity'] = 'Deuda'
        context['action'] = 'edit'
        return context
