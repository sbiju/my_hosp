from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions
from .models import Patient, Payment


class PatientSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='patients_detail_api')

    class Meta:
        model = Patient


class PaymenttSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='payments_detail_api')

    class Meta:
        model = Payment
