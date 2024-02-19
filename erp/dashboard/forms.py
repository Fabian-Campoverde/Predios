from django.forms import *

from erp.userauths.models import Deuda, Predio,Construccion



class DateTimePickerInput(DateInput):
        input_type = 'date'

class PredioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['placeholder'] = 'Introduzca su '+ form.label
        self.fields['propietario'].widget.attrs['class'] = 'form-control select2 '
        self.fields['propietario'].queryset = self.fields['propietario'].queryset.exclude(DNI=None)
        self.fields['descripcion'].widget.attrs['rows'] = 4
        # self.fields['provincia'].widget.attrs['disabled'] = 'true'
        # self.fields['distrito'].widget.attrs['disabled'] = 'true'
        # self.fields['zona'].widget.attrs['disabled'] = 'true'
        

    class Meta:
        model = Predio
        fields = ['cuc','cod_ref_catastral','tamaño_propiedad','descripcion','propietario','ubicacion','departamento'
                  ,'provincia','distrito','zona']



class DeudaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['contribuyente'].widget.attrs['class'] = 'form-control select2'
        self.fields['contribuyente'].queryset = self.fields['contribuyente'].queryset.exclude(DNI=None)
        self.fields['detalles'].widget.attrs['rows'] = 4

    class Meta:
        model = Deuda
        fields = '__all__'
        widgets = {
            'fecha_vencimiento' : DateTimePickerInput(),
            
        }
        


class ConstruccionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']='form-control'
        self.fields['predio'].widget.attrs['class'] = 'form-control select2'
        # self.fields['predio'].queryset = self.fields['predio'].queryset.exclude(DNI=None)  

    class Meta:
        model= Construccion
        fields = '__all__'



