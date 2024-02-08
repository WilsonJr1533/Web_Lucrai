from django.urls import path
from . import views
from .views import grafico, adicionar_transacao, index
from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('index/', index, name='dashboard'),
    path('obter_resposta_ia/', views.obter_resposta_ia_view),
    path('grafico/', grafico, name='grafico'),
    path('adicionar_transacao/', adicionar_transacao, name='adicionar_transacao'),

    
   
    
    
    
    
]

