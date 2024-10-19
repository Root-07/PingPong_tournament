from rest_framework import viewsets
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Player, Tournament, Match, TournamentPlayer
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer

# ViewSet pour gérer les joueurs
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

# ViewSet pour gérer les tournois
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    # Créer un tournoi
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # Démarrer le tournoi une fois les joueurs inscrits
    @action(detail=True, methods=['post'])
    def start_tournament(self, request, pk=None):
        tournament = self.get_object()
        player_count = tournament.players.count()

        if player_count != tournament.max_players:
            return Response({'message': f'Tournament requires exactly {tournament.max_players} players to start'}, status=400)

        if player_count % 2 != 0:
            return Response({'message': 'Number of players must be even to start the tournament'}, status=400)
            # Créer les matchs du premier tour
        self.create_first_round_matches(tournament)
        tournament.status = 'ongoing'
        tournament.save()
        return Response({'message': 'Tournament started successfully'})
       
    
    # Créer les matchs du premier tour (par exemple, quart de finale)
    def create_first_round_matches(self, tournament):
        players = list(tournament.players.all())
        # Créer des matchs pour le premier tour (1v1)
        for i in range(0, len(players), 2):
            Match.objects.create(
                tournament=tournament,
                player1=players[i],
                player2=players[i+1],
                round_number=1  # Premier tour
            )
    
    # Action pour rejoindre un tournoi
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        tournament = self.get_object()
        player_id = request.data.get('player_id')

        if tournament.players.count() >= tournament.max_players:
            return Response({'message': 'Tournament is full'}, status=400)
    
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({'message': 'Player does not exist'}, status=404)

        if TournamentPlayer.objects.filter(player=player, tournament=tournament).exists():
            return Response({'message': 'Player is already in the tournament'}, status=400)

        TournamentPlayer.objects.create(player=player, tournament=tournament)
        return Response({'message': 'Player joined successfully'})


    # Action pour générer des matchs du tour suivant
    @action(detail=True, methods=['post'])
    def generate_next_round(self, request, pk=None):
        tournament = self.get_object()
        current_round = tournament.current_round
        matches = Match.objects.filter(tournament=tournament, round_number=current_round, winner__isnull=False)
        
        if matches.count() != tournament.max_players // (2 ** current_round):
            return Response({'message': 'Not all matches have been completed'}, status=400)

        winners = [match.winner for match in matches]
        if len(winners) % 2 != 0:
            return Response({'message': 'The number of winners must be even'}, status=400)
        
        tournament.current_round += 1
        for i in range(0, len(winners), 2):
            Match.objects.create(
                tournament=tournament,
                player1=winners[i],
                player2=winners[i + 1],
                round_number=tournament.current_round
            )
        
        tournament.save()
        return Response({'message': 'Next round generated successfully'})

# ViewSet pour gérer les matchs
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    # Action pour définir un gagnant d'un match
    @action(detail=True, methods=['post'])
    def set_winner(self, request, pk=None):
        match = self.get_object()
        winner_id = request.data.get('winner_id')
        try:
            winner = Player.objects.get(id=winner_id)
        except Player.DoesNotExist:
            return Response({'message': 'Player does not exist'}, status=404)
        if winner not in [match.player1, match.player2]:
            return Response({'message': 'Winner must be a participant in the match'}, status=400)
        
        match.winner = winner
        match.played_at = timezone.now()
        match.save()
        return Response({'message': 'Winner set successfully'})
