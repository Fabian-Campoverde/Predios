from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView,DeleteView
from django.template.loader import render_to_string
from erp.userauths.models import Construccion
from erp.dashboard.forms import ConstruccionForm
from erp.dashboard.models import *
from app.settings import *



class ConstruccionList(PermissionRequiredMixin,ListView):
    permission_required = 'view_contribuyente'
    model = Construccion
    template_name = 'construcciones.html'

    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Construcciones'
        context['create_url'] = reverse_lazy('newconstruccion')
        context['entity'] = 'Construcciones'
        context['action'] = 'add'
        return context
    
class NewConstruccion(PermissionRequiredMixin, CreateView):
    permission_required = 'view_contribuyente'
    model = Construccion
    template_name = 'new.html'
    form_class = ConstruccionForm
    success_url = reverse_lazy('construcciones')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva construccion en construccion'
        context['list_url'] = reverse_lazy('construcciones')
        context['entity'] = 'Construcciones'
        context['action'] = 'add'
        return context
    
    def send_email(self, construccion):
        try:
            mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Construir el mensaje
            email_to=construccion.predio.propietario.user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = email_to 
            mensaje['Subject'] = "Tienes una nueva construccion registrada en tu predio"
            mensaje['X-Custom-Header'] = 'Construccion en el Sistema de Predios'

            content= render_to_string("email.html", {"user": construccion.predio.propietario.user,"contrib": construccion.predio.propietario ,
                                                     "img":"https://ai-previews.123rf.com/ai-variation/preview/wm/solerf/solerf1505/solerf150500005_1.jpg", 
                                                     "title":"su nueva construccion",
                                                     "message": "Nueva construccion registrada en el predio de ubicacion: "+ construccion.predio.ubicacion})

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
        construccion = form.save()

        # Enviar correo electrónico al deudor
        self.send_email(construccion)

        return super().form_valid(form)
    
class EditConstruccion(PermissionRequiredMixin, UpdateView):
    permission_required = 'view_contribuyente'
    model = Construccion
    template_name = 'edit.html'
    form_class = ConstruccionForm
    success_url = reverse_lazy('construcciones')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una construccion'
        context['list_url'] = reverse_lazy('construcciones')
        context['entity'] = 'Construcciones'
        context['action'] = 'edit'
        return context
    
    def send_email(self, construccion):
        try:
            mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Construir el mensaje
            email_to=construccion.predio.propietario.user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = email_to 
            mensaje['Subject'] = "Actualización de datos de construccion registrada en tu predio"
            mensaje['X-Custom-Header'] = 'Construccion en el Sistema de Predios'

            content= render_to_string("email.html", {"user": construccion.predio.propietario.user,"contrib": construccion.predio.propietario ,
                                                     "img":"https://ai-previews.123rf.com/ai-variation/preview/wm/solerf/solerf1505/solerf150500005_1.jpg", 
                                                     "title":"su construccion actualizada",
                                                     "message": "Su construccion registrada en el predio de ubicacion: "+ construccion.predio.ubicacion+ " ha registrado algunos cambios en el sistema"})

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
        construccion = form.save()

        # Enviar correo electrónico al deudor
        self.send_email(construccion)

        return super().form_valid(form)

class DeleteConstruccion(DeleteView):
    model = Construccion
    template_name = 'delete.html'
    success_url = reverse_lazy('construcciones')  # Redirección exitosa después de la eliminación

    def form_valid(self, form):
        # Obtenemos la construccion a eliminar
        const = self.get_object()  
        # construccion = form.save()
        # Enviar correo electrónico al deudor
        # self.send_email(const)            
        # const.delete()
        try:
            const.delete()
            self.send_email(const)
        except Exception as e:
            print (e)
    
        # Redireccionamos a la URL de éxito
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Construccion'
        context['list_url'] = reverse_lazy('construcciones')
        context['entity'] = 'Construcciones'
        context['action'] = 'del'
        return context
    
    def send_email(self, construccion):
        try:
            mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            
            # Construir el mensaje
            email_to=construccion.predio.propietario.user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = email_to 
            mensaje['Subject'] = "Eliminacion de su construccion registrada en tu predio"
            mensaje['X-Custom-Header'] = 'Construccion en el Sistema de Predios'

            content= render_to_string("email.html", {"user": construccion.predio.propietario.user,"contrib": construccion.predio.propietario ,
                                                     "img":"https://ai-previews.123rf.com/ai-variation/preview/wm/solerf/solerf1505/solerf150500005_1.jpg", 
                                                     "title":"su construccion eliminada",
                                                     "message": "Su construccion registrada en el predio de ubicacion: "+ construccion.predio.ubicacion+ " ha sido eliminada del sistema"})

            # Adjuntamos el texto
            mensaje.attach(MIMEText(content,'html'))
            # Enviar el correo electrónico
            mailServer.sendmail(EMAIL_HOST_USER, email_to, mensaje.as_string())
            
            # Cerrar la conexión con el servidor SMTP
            mailServer.quit()
            
            print("Correo enviado correctamente")
            
        except Exception as e:
            print("Error al enviar el correo:", e)



