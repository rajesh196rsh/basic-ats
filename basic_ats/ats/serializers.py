# candidates/serializers.py
from rest_framework import serializers
from .models import Candidate, Experience

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    experience = ExperienceSerializer()

    class Meta:
        model = Candidate
        fields = '__all__'
