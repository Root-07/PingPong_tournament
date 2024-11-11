from rest_framework import serializers
from .models import Player, Tournament, Match

# Serializer pour le modèle Player
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'email']  # ou liste des champs spécifiques

# Serializer pour le modèle Tournament
class TournamentSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)  # Si tu veux inclure les joueurs dans la réponse JSON

    class Meta:
        model = Tournament
        fields = '__all__'

# Serializer pour le modèle Match
class MatchSerializer(serializers.ModelSerializer):
    player1_name = serializers.CharField(source='player1.name')
    player2_name = serializers.CharField(source='player2.name')
    winner_name = serializers.CharField(source='winner.name')

    class Meta:
        model = Match
        fields = ['id', 'player1_name', 'player2_name', 'round_number', 'winner_name']


