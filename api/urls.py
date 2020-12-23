from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from django.shortcuts import render


urlpatterns = [

    # Login - Logout
    path('login', CustomAuthToken.as_view()),
    # path('logout', Logout.as_view()),

    # ESSA ROTA CRIA TODOS OS TIPOS DE USUARIOS E LISTA TODOS ELES
    path('registro', Registro.as_view()),
    #retorna todos os USUARIOS
    path('usuario', UsuarioList.as_view()),
    #Edita um usuario
    # path('usuario/<int:pk>', UsuarioDetail.as_view()),
    # Cria Associação e Remove Associação entre profissional e um estabelecimento
    path('associar-profissional/<int:pk_profissional>/<int:pk_estabelecimento>', AssociarProfissionalEstabelecimento.as_view()),

    # ESSA ROTA CRIA AS VACINAS E LISTA TODAS ELAS
    path('vacina', VacinaList.as_view()),

    path('municipio', MunicipioList.as_view()),
    
    path('estabelecimento', EstabelecimentoList.as_view()),


    #Lista todos os PROFISSIONAIS
    path('profissional', ProfissionalList.as_view()),
    
    #Lista todos os PACIENTES
    path('paciente', PacienteList.as_view()),

    # Criar AGENDAMENTO
    path('agendamento', AgendamentoList.as_view()),

    # Associa um PACIENTE a um AGENDAMENTO - Função de Agendar
    path('associar-paciente/<int:pk_paciente>/<int:pk_agendamento>', AssociarPacienteAgendamento.as_view())

    # Cria uma APLICACAO 
    

]
