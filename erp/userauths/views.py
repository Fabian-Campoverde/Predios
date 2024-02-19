from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from erp.userauths.forms import UserRegisterForm, ProfileForm
from erp.userauths.models import Profile, User


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)  # No guardes el usuario todavía
            new_user.set_password(form.cleaned_data['password1'])  # Establece la contraseña encriptada
            new_user.save()  
            form.save_m2m() 
            profile = Profile.objects.create(user=new_user)  # Crea el perfil asociado al usuario
            # email = form.cleaned_data['email']  # Obtener el email ingresado

            username = form.cleaned_data.get("username")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
        
            profile_form = ProfileForm({'email': email})
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = User  # Asociar el perfil al usuario
                profile.save()

            messages.success(request, f"Hey {username}, Tu cuenta fue creada exitosamente!")
            # new_user =authenticate(request, email=email, password=password)
                                    
            
            login(request, new_user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

    else:
        form = UserRegisterForm()

    context = {'form':form}
    return render(request, 'sign-up.html', context)

