from django.shortcuts import render
import random
from rest_framework import viewsets
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import Player, Tournament, Match, TournamentPlayer
from .serializers import PlayerSerializer, TournamentSerializer, MatchSerializer


def tournament_dashboard(request):
    return render(request, 'frontend/index.html')


# ViewSet pour gérer les joueurs
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# ViewSet pour gérer les tournois
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def perform_create(self, serializer):
        # Récupérer l'ID du créateur du tournoi
        creator_id = self.request.data.get('creator_id', None)

        if not creator_id:
            creator = Player.objects.first()  # Choisir le premier joueur disponible
            if creator:
                tournament = serializer.save(creator=creator)  # Créer le tournoi avec le créateur
                tournament.players.add(creator)  # Ajouter le créateur comme premier joueur
                self.add_player_to_tournament(creator, tournament)  # Ajouter le créateur au tournoi
            else:
                return Response({"detail": "Aucun joueur disponible."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                creator = Player.objects.get(id=creator_id)
                tournament = serializer.save(creator=creator)  # Créer le tournoi avec le créateur
                tournament.players.add(creator)  # Ajouter le créateur comme premier joueur
                self.add_player_to_tournament(creator, tournament)  # Ajouter le créateur au tournoi
            except Player.DoesNotExist:
                return Response({"detail": "Le créateur spécifié n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

    def add_player_to_tournament(self, player, tournament):
        """Ajoute un joueur à un tournoi."""
        # Vérifier si le joueur est déjà dans le tournoi
        if not TournamentPlayer.objects.filter(player=player, tournament=tournament).exists():
            TournamentPlayer.objects.create(player=player, tournament=tournament)
            print(f'Joueur {player.name} ajouté au tournoi {tournament.name}.')

    def create(self, request, *args, **kwargs):
        # Utilisation de `perform_create` pour la création
        return super().create(request, *args, **kwargs)

    # Créer un tournoi et avec un joueur qui va cree print message de succès
    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     print('Tournament created successfully')
    #     return response


    # supprimer un tournoi et print message de succès
    # def destroy(self, request, *args, **kwargs):
    #     response = super().destroy(request, *args, **kwargs)
    #     print('Tournament deleted successfully')
    #     return response


    @action(detail=True, methods=['post'])
    def start_tournament(self, request, pk=None):
        tournament = self.get_object()
        player_count = tournament.players.count()

        if player_count != tournament.max_players:
            return Response({'message': f'Tournament requires exactly {tournament.max_players} players to start'}, status=400)

        # Démarrer le tournoi
        winners = self.play_quarter_finals(tournament)

        # Continue jusqu'à ce qu'il ne reste qu'un seul gagnant
        while len(winners) > 1:
            winners = self.play_semi_finals(tournament, winners)

        if winners:
            self.finish_tournament(tournament, winners[0])  # Le gagnant final
        return Response({'message': 'Tournament finished successfully', 'winner': str(winners[0])})

    def get_results(self, request, pk=None):
        tournament = self.get_object()
        results = {
            "tournament": tournament.name,
            "status": tournament.status,
            "winner": tournament.winner.name if tournament.winner else None,
            "players": [player.name for player in tournament.players.all()],
            "current_round": tournament.current_round,
        }
        return Response(results)

    def play_quarter_finals(self, tournament):
        players = [tp.player for tp in tournament.tournamentplayer_set.all()]
        matches = self.generate_matches(tournament, players)
        winners = self.simulate_matches(matches)
        return winners

    def play_semi_finals(self, tournament, winners):
        matches = self.generate_matches(tournament, winners)
        winners = self.simulate_matches(matches)
        return winners

    def finish_tournament(self, tournament, winner):
        tournament.status = 'finished'
        tournament.winner = winner
        tournament.save()
        print(f'Tournament finished. Winner: {winner}')

    def generate_matches(self, tournament, players):
        random.shuffle(players)  # Mélanger les joueurs
        matches = []

        for i in range(0, len(players), 2):
            match = Match(
                tournament=tournament,
                player1=players[i],
                player2=players[i + 1],
                round_number=tournament.current_round
            )
            match.save()
            matches.append(match)

        return matches

    def simulate_matches(self, matches):
        winners = []
        for match in matches:
            winner = random.choice([match.player1, match.player2])
            match.winner = winner
            match.played_at = timezone.now()
            match.save()
            winners.append(winner)
            print(f'Match {match} a été gagné par {winner}.')
        return winners

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
    queryset = Match.objects.all().select_related('player1', 'player2')
    serializer_class = MatchSerializer

    @action(detail=True, methods=['post'])
    def set_winner(self, request, pk=None):
        try:
            match = self.get_object()
            winner_id = request.data.get('winner_id')

            if winner_id:
                match.winner_id = winner_id
                match.save()
                return Response({"message": "Le gagnant a été défini avec succès."})
            else:
                return Response({"error": "Aucun gagnant spécifié."}, status=400)
        except Match.DoesNotExist:
            return Response({"error": "Match non trouvé."}, status=404)

