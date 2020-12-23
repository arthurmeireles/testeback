from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

# ------------------------------------------------------------------------------

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class RegistroSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

# ------------------------------------------------------------------------------

class ProfissionalSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    class Meta:
        model = Profissional
        fields = '__all__'
# ------------------------------------------------------------------------------

class PacienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    class Meta:
        model = Paciente
        fields = '__all__'

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'


# ------------------------------------------------------------------------------
class CoordenadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    class Meta:
        model = Coordenador
        fields = '__all__'

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = '__all__'

class AplicacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicacao
        fields = '__all__'

# ------------------------------------------------------------------------------



class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estabelecimento
        fields = '__all__'

# -------------------------
