from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

from erp.userauths.forms import ProfileForm, UserForm,UserRegisterForm
from erp.userauths.models import Deuda, Profile, User
from erp.dashboard.models import *


class UserView(PermissionRequiredMixin, ListView):
    permission_required = 'view_contribuyente'
    model = Profile
    template_name = 'users.html'

    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de contribuyentes'
        context['list_url'] = reverse_lazy('userhome')
        context['create_url'] = reverse_lazy('create')
        context['users'] = User.objects.all()

        context['entity'] = 'Usuarios'
        return context


class NewContribuyente(PermissionRequiredMixin, CreateView):
    permission_required = 'view_contribuyente'
    template_name = 'user_form.html'
    success_url = reverse_lazy('userhome')
    model=Profile
    form=ProfileForm


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('userhome')
        
        return context 
    
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
       
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(self.success_url)
        else:
            # Volver a renderizar la plantilla con los formularios y los errores
            return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
        
    
        
    # permission_required = 'view_contribuyente'
    # model = Profile
    # form_class = ProfileForm
    # template_name = 'new.html'
    # success_url = reverse_lazy('userhome')


    # def post(self, request, *args, **kwargs):
    #     form = ProfileForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(self.success_url)
    #     else:
    #         self.object = None
    #         context = self.get_context_data(**kwargs)
    #         context['form'] = form
    #         return render(request, self.template_name, context)


    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Creacion de un nuevo Contribuyente'
    #     context['list_url'] = reverse_lazy('userhome')
    #     context['entity'] = 'Usuarios'
    #     context['action'] = 'add'
    #     return context

class EditContribuyente(PermissionRequiredMixin, UpdateView):
    # permission_required = 'view_contribuyente'
    # model = Profile
    # form_class = ProfileForm
    # template_name = 'edit.html'
    # success_url = reverse_lazy('userhome')

   




    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Edicion de un nuevo Contribuyente'
    #     context['list_url'] = reverse_lazy('userhome')
    #     context['entity'] = 'Usuarios'
    #     context['action'] = 'edit'
    #     return context
    # permission_required = 'view_contribuyente'
    # model = Profile
    # form_class = ProfileForm
    # template_name = 'edit.html'
    # success_url = reverse_lazy('userhome')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if 'user_form' not in context:
    #         context['user_form'] = self.get_user_form()
    #     if 'profile_form' not in context:
    #         context['profile_form'] = self.get_profile_form()
    #     return context

    # def get_user_form(self):
    #     instance = self.object.user
    #     user_form = UserForm(instance=instance)
    #     return user_form

    # def get_profile_form(self):
    #     instance = self.object
    #     profile_form = ProfileForm(instance=instance)
    #     return profile_form

    # def form_valid(self, form):
    #     user_form = self.get_user_form()
    #     profile_form = self.get_profile_form()
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #     return super().form_valid(form)
    permission_required = 'view_contribuyente', 'delete_user'
    model = Profile
    form_class = ProfileForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('userhome')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('userhome')
        if 'user_form' not in context:
            context['user_form'] = self.get_user_form(instance=self.object.user)
        if 'profile_form' not in context:
            context['profile_form'] = self.get_profile_form(instance=self.object)
        return context
    
    def form_valid(self, form):
        user_form = self.get_user_form(instance=self.object.user, data=self.request.POST)
        profile_form = self.get_profile_form(instance=self.object, data=self.request.POST, files=self.request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        user_form = self.get_user_form(instance=self.object.user, data=self.request.POST)
        profile_form = self.get_profile_form(instance=self.object, data=self.request.POST, files=self.request.FILES)
        user_errors = user_form.errors if user_form.errors else None
        profile_errors = profile_form.errors if profile_form.errors else None
    
        context = self.get_context_data(user_form_errors=user_errors, profile_form_errors=profile_errors)
        return self.render_to_response(context)

    def get_user_form(self, **kwargs):
        return UserForm(**kwargs)

    def get_profile_form(self, **kwargs):
        return ProfileForm(**kwargs)

class DeleteContribuyente(DeleteView):
    model = Profile
    template_name = 'delete.html'
    success_url = reverse_lazy('userhome')  # Redirección exitosa después de la eliminación

    def form_valid(self, form):
        # Obtenemos el perfil a eliminar
        profile = self.get_object()
        
        # Obtenemos el usuario asociado al perfil
        user = profile.user

        # Eliminamos el perfil y el usuario
        profile.delete()
        user.delete()

        # Redireccionamos a la URL de éxito
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Contribuyente'
        context['list_url'] = reverse_lazy('userhome')
        context['entity'] = 'Usuarios'
        context['action'] = 'del'
        return context
