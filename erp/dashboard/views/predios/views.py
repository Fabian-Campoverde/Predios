from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.template.loader import render_to_string
from erp.userauths.models import Predio
from erp.dashboard.forms import PredioForm
from erp.dashboard.models import *
from app.settings import *

class PredioList(PermissionRequiredMixin, ListView):
    permission_required = 'view_contribuyente'
    model = Predio
    template_name = 'predios.html'

    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de predios'
        context['create_url'] = reverse_lazy('newpredio')
        context['entity'] = 'Predios'
        context['action'] = 'add'
        return context


class NewPredio(PermissionRequiredMixin, CreateView):
    permission_required = 'view_contribuyente'
    model = Predio
    template_name = 'new.html'
    form_class = PredioForm
    success_url = reverse_lazy('predio')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de predios'
        context['list_url'] = reverse_lazy('predio')
        context['entity'] = 'Predios'
        context['action'] = 'add'
        return context
    
    def send_email(self, predio):
        try:
            mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Construir el mensaje
            email_to=predio.propietario.user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = email_to 
            mensaje['Subject'] = "Tienes un nuevo predio registrado"
            mensaje['X-Custom-Header'] = 'Predio en el Sistema de Predios'

            content= render_to_string("email.html", {"user": predio.propietario.user,"contrib": predio.propietario ,
                                                     "img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJK4f75gQcYIgjZ1R6LCVS7l47kcdlTJvn3DbysulRJA&s", 
                                                     "title":"su nuevo predio",
                                                     "message": "Nuevo predio registrado en "+ predio.ubicacion})

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
        predio = form.save()

        # Enviar correo electrónico al deudor
        self.send_email(predio)

        return super().form_valid(form)


class EditPredio(PermissionRequiredMixin, UpdateView):
    permission_required = 'view_contribuyente'
    model = Predio
    template_name = 'edit.html'
    form_class = PredioForm
    success_url = reverse_lazy('predio')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un nuevo predio'
        context['list_url'] = reverse_lazy('userhome')
        context['entity'] = 'Usuarios'
        context['action'] = 'edit'
        return context
