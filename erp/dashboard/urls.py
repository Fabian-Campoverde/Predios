from django.urls import path
from erp.dashboard.views.views import *
from erp.dashboard.views.users_views.views import *
from erp.dashboard.views.deudas.views import *
from erp.dashboard.views.predios.views import *
from erp.dashboard.views.construcciones.views import *
urlpatterns = [
    path('Dashadmin/', IndexView.as_view(), name="home"),

    path('Users', UserView.as_view(), name="userhome"),
    path('Predio', PredioList.as_view(), name="predio"),
    path('Deuda/', DeudasView.as_view(), name="deudas"),
    path('Construccion/', ConstruccionList.as_view(), name="construcciones"),

    path('Users/Create', NewContribuyente.as_view(), name="create"),
    path('Predio/Create', NewPredio.as_view(), name="newpredio"),
    path('Deuda/Create', NewDeuda.as_view(), name="new"),
    path('Construccion/Create', NewConstruccion.as_view(), name="newconstruccion"),

    path('Users/Edit/<int:pk>', EditContribuyente.as_view(), name="editcontrib"),
    path('Deuda/Edit/<int:pk>', EditDeuda.as_view(), name='edit'),
    path('Predio/Edit/<int:pk>', EditPredio.as_view(), name='editpredio'),
    path('Construccion/Edit/<int:pk>', EditConstruccion.as_view(), name='editconstruccion'),

    path('Users/Delete/<int:pk>', DeleteContribuyente.as_view(), name="delcontrib"),
    path('Deuda/Delete/<int:pk>', DeleteDeuda.as_view(), name="deldeuda"),
    path('Construccion/Delete/<int:pk>', DeleteConstruccion.as_view(), name="delconstruccion"),
]
