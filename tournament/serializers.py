from rest_framework import serializers
from .models import Player, Tournament, Match

# Serializer pour le modèle Player
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name']  # ou liste des champs spécifiques

# Serializer pour le modèle Tournament
class TournamentSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)  # Si tu veux inclure les joueurs dans la réponse JSON
    message = serializers.SerializerMethodField() # Champ personnalisé
    creator_id = serializers.IntegerField(write_only=True)  # Pour inclure les détails du créateur du tournoi dans la réponse JSON


    class Meta:
        model = Tournament
        fields = ['id','players','name', 'creator' , 'message', 'creator_id' ]


    def get_message(self, obj):
        return f"Le tournoi {obj.name} a été créé avec succès."

    def create(self, validated_data):
        # Le créateur sera ajouté dans la méthode perform_create de la vue
        return super().create(validated_data)

    # def create(self, validated_data):
    #     creator_id = validated_data.get('creator_id', None)

    #     if not creator_id:
    #         # Si aucun créateur n'est spécifié, on prend le premier joueur
    #         creator = Player.objects.first()
    #         if creator:
    #             validated_data['creator'] = creator
    #         else:
    #             raise serializers.ValidationError("Aucun joueur disponible.")

    #     return super().create(validated_data)


# Serializer pour le modèle Match
class MatchSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)
    player1_name = serializers.CharField(source='player1.name')
    player2_name = serializers.CharField(source='player2.name')
    winner_name = serializers.CharField(source='winner.name')

    class Meta:
        model = Match
        fields = ['id', 'tournament_name', 'player1_name', 'player2_name', 'round_number', 'winner_name']



