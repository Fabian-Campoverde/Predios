from django.contrib.auth.views import LoginView
# from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

class ViewLogin(LoginView):
    template_name = 'login.html'
    def form_valid(self, form):
        # Llama al método form_valid de la clase base para autenticar al usuario
        super().form_valid(form)

        # Autenticar al usuario manualmente usando el formulario
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        # Verifica si el usuario está autenticado y activo
        if user is not None and user.is_active:
            # Inicia sesión manualmente
            login(self.request, user)

        # Redirige al usuario a la página adecuada después de iniciar sesión
        if user.is_superuser:
            # Si es un admin, redirige a 'home'
            return redirect('home')
        else:
            # Si es un usuario normal, redirige a 'dashboard'
            return redirect('dashboard')