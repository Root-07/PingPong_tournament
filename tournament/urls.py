from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, TournamentViewSet, MatchViewSet
from .views import tournament_dashboard


# Créer un routeur DRF
router = DefaultRouter()

# Enregistrer les viewsets avec le routeur
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'tournaments', TournamentViewSet, basename='tournament')
router.register(r'matches', MatchViewSet, basename='match')


# Inclure les routes dans les URLs de l'application
urlpatterns = [
    path('', include(router.urls)),  # Cela inclut toutes les routes générées par le routeur
	path('tournaments/<int:pk>/results/', TournamentViewSet.as_view({'get': 'get_results'}), name='tournament-results'), # Ajouter une route personnalisée pour obtenir les résultats d'un tournoi
	path('tournament-dashboard/', tournament_dashboard, name='tournament-dashboard'),


	# Ajouter les routes spécifiques pour start_tournament et join
	path('tournaments/<int:pk>/start_tournament/', TournamentViewSet.as_view({'post': 'start_tournament'}), name='start_tournament'),
	path('tournaments/<int:pk>/join/', TournamentViewSet.as_view({'post': 'join'}), name='join_tournament'),
	# path('tournaments/<int:tournament_id>/players/', TournamentPlayerViewSet.as_view({'get': 'list'}), name='tournament-players'),  # Utilisez une route manuelle pour gérer ce cas spécifique
]
