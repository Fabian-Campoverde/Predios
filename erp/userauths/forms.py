from django import forms
from django.contrib.auth.forms import UserCreationForm
from erp.userauths.models import User, Profile
from django.forms import *


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    email = EmailField(widget=EmailInput(attrs={'placeholder': 'Email'}))
    password1= CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = CharField(widget=PasswordInput(attrs={'placeholder': 'Confirm Password'}))


    class Meta:
        model = User
        fields = ['username','email']
        
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    # username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    # email = EmailField(widget=EmailInput(attrs={'placeholder': 'Email'}))
    # password= CharField(widget=PasswordInput(render_value=True,attrs={'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ['username','email','password']
        widgets= {
            'username': TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}),
            'email': EmailInput(attrs={'placeholder': 'Ingreso su correo'}),
            'password': PasswordInput(render_value=True,attrs={'placeholder': 'Ingrese su contraseña'})
        }
    
    

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control mb-3'


    nombres = CharField(widget=TextInput(attrs={'placeholder': 'Nombres '}))
    apellidos = CharField(widget=TextInput(attrs={'placeholder': 'Apellidos '}))
    #email = EmailField(widget=EmailInput(attrs={'placeholder': 'Email'}))
    cod_contri_rentas = IntegerField(widget=TextInput(attrs={'placeholder': 'Introduzca su Codigo de rentas ', 'type':'number'}))
    cod_predial_rentas = IntegerField(widget=TextInput(attrs={'placeholder': 'Introduzca su Codigo Predial de rentas ', 'type':'number'}))
    DNI = IntegerField(widget=TextInput(attrs={'placeholder': 'Introduzca su DNI', 'type':'number'}))
    telefono = IntegerField(widget=TextInput(attrs={'placeholder': 'Introduzca su Telefono', 'type':'number'}))

    class Meta:
        model = Profile
        fields = ['nombres', 'DNI','image', 'telefono', 'apellidos','cod_contri_rentas','cod_predial_rentas','ruc','persona_juridica']  # Incluye el campo email en la lista de campos
        exclude = ['Deudas',]
    
    def clean_cod_contri_rentas(self):
        cod_contri_rentas = self.cleaned_data['cod_contri_rentas']
        if cod_contri_rentas is not None and cod_contri_rentas < 0:
            raise ValidationError("El código de contribuyente no puede ser negativo.")
        return cod_contri_rentas

    def clean_cod_predial_rentas(self):
        cod_predial_rentas = self.cleaned_data['cod_predial_rentas']
        if cod_predial_rentas is not None and cod_predial_rentas < 0:
            raise ValidationError("El código predial no puede ser negativo.")
        return cod_predial_rentas

    def clean_DNI(self):
        DNI = self.cleaned_data.get('DNI')       
        if DNI is not None and DNI < 0:
            raise forms.ValidationError("El DNI no puede ser negativo.")
        return DNI
    
    def clean_telefono(self):
        DNI = self.cleaned_data['telefono']
        if DNI is not None and DNI < 0:
            raise ValidationError("El Numero telefonico no puede ser negativo.")
        return DNI


