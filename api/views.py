from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import *
from .pagination import *
from .serializers import *
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


# Create your views here.

class Registro(ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        if instance.tipo_usuario == 1:
            Coordenador.objects.create(usuario=instance)
        elif instance.tipo_usuario == 2:
            Profissional.objects.create(usuario=instance)
        elif instance.tipo_usuario == 3:
            Paciente.objects.create(usuario=instance)
        instance.save()

class CoordenadorList(ListCreateAPIView):
    serializer_class = CoordenadorSerializer
    pagination_class = PaginationDefault
    queryset = Coordenador.objects.all().reverse().order_by('id')

# ---------------------------

class ProfissionalList(ListCreateAPIView):
    serializer_class = ProfissionalSerializer
    pagination_class = PaginationDefault
    queryset = Profissional.objects.all().reverse().order_by('id')

class AssociarProfissionalEstabelecimento(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        try:
            profissional = Profissional.objects.get(pk=kwargs.get('pk_profissional'))
            estabelecimento =  Estabelecimento.objects.get(pk = kwargs.get('pk_estabelecimento'))
            if profissional.estabelecimento:
                return Response('Não foi possível associar o profissional. Já há uma associacao com um estabelecimento',
                                status=status.HTTP_401_UNAUTHORIZED)
            elif estabelecimento:
                profissional.estabelecimento = estabelecimento
                profissional.save()
                return Response({"sucesso": ("O estabelecimento foi associado.")}, status=status.HTTP_200_OK)
            else:
                return Response('Estabelecimento não existe', status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            estabelecimento =  Estabelecimento.objects.get(pk=kwargs.get('pk_estabelecimento'))
            profissional = Profissional.objects.get(pk=kwargs.get('pk_profissional'))
            if profissional.estabelecimento:
                profissional.estabelecimento = None
                profissional.save()
                return Response('Removida associacao entre Profissional e Estabelecimento', status=status.HTTP_200_OK)
            else:
                return Response('O profissional não possui associação com um estabelecimento', status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------------

class PacienteList(ListCreateAPIView):
    serializer_class = PacienteSerializer
    pagination_class = PaginationDefault
    queryset = Paciente.objects.all().reverse().order_by('id')

# VINCULA UM PACIENTE A UM AGENDAMENTO CRIADO
class AssociarPacienteAgendamento(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(pk=kwargs.get('pk_paciente'))
            agendamento =  Agendamento.objects.get(pk=kwargs.get('pk_agendamento'))
            if agendamento.paciente:
                return Response('Não foi possível agendar o horário para o Paciente. O Paciente já agendou o horario',
                                status=status.HTTP_401_UNAUTHORIZED)
            elif agendamento:
                agendamento.paciente = paciente
                agendamento.save()
                return Response({"sucesso": ("O agendamento foi realizado.")}, status=status.HTTP_200_OK)
            else:
                return Response('Agendamento não existe', status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(pk=kwargs.get('pk_paciente'))
            agendamento =  Agendamento.objects.get(pk = kwargs.get('pk_agendamento'))

            if agendamento.paciente:
                agendamento.paciente = None
                agendamento.save()
                return Response('Agendamento Removido', status=status.HTTP_200_OK)
            else:
                return Response('O paciente não possui agendamento', status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# CRIA AGENDAMENTO

class AgendamentoList(ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    pagination_class = PaginationDefault
    queryset = Agendamento.objects.all()

class AplicacaoList(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AplicacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# ---------------------------

class UsuarioList(ListCreateAPIView):
    serializer_class = UsuarioSerializer
    pagination_class = PaginationDefault
    queryset = Usuario.objects.all().reverse().order_by('id')

class VacinaList(ListCreateAPIView):
    serializer_class = VacinaSerializer
    pagination_class = PaginationDefault
    queryset = Vacina.objects.all().reverse().order_by('id')

# ---------------------------

class MunicipioList(ListCreateAPIView):
    serializer_class = MunicipioSerializer
    pagination_class = PaginationDefault
    queryset = Municipio.objects.all().reverse().order_by('id')

class EstabelecimentoList(ListCreateAPIView):
    serializer_class = EstabelecimentoSerializer
    pagination_class = PaginationDefault
    queryset = Estabelecimento.objects.all().reverse().order_by('id')

# ---------------------------


class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        usuario = UsuarioSerializer(user)
        return Response({
            'token': token.key,
            'usuario': usuario.data
        })