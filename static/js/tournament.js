// Récupérer la liste des tournois depuis l'API
function fetchTournaments() {
    fetch('/api/tournaments/')
      .then(response => response.json())
      .then(tournaments => {
        const tournamentList = document.getElementById('tournament-list');
        tournamentList.innerHTML = '';
        tournaments.forEach(tournament => {
          const listItem = document.createElement('li');
          listItem.textContent = tournament.name;
          listItem.onclick = () => fetchTournamentDetails(tournament.id);
          tournamentList.appendChild(listItem);
        });
      })
      .catch(error => console.error('Erreur:', error));
  }
  
  // Récupérer les détails d'un tournoi via l'API
  function fetchTournamentDetails(tournamentId) {
    fetch(`/api/tournaments/${tournamentId}/`)
      .then(response => response.json())
      .then(tournament => {
        const detailsDiv = document.getElementById('tournament-details');
        detailsDiv.innerHTML = `
          <h3>${tournament.name}</h3>
          <p>Statut: ${tournament.status}</p>
          <button onclick="joinTournament(${tournamentId}, 1)">Rejoindre le tournoi</button>
        `;
      })
      .catch(error => console.error('Erreur:', error));
  }
  
  // Fonction pour rejoindre un tournoi via l'API
  function joinTournament(tournamentId, playerId) {
    fetch(`/api/tournaments/${tournamentId}/join/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ player_id: playerId }) // Assure-toi que 'player_id' est correct
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de la participation au tournoi.');
        }
        return response.json();
      })
      .then(data => {
        alert(data.message || 'Participation réussie au tournoi.');
        fetchTournamentDetails(tournamentId); // Recharger les détails après avoir rejoint
      })
      .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de la participation au tournoi.');
      });
}
  
  
  // Charger la liste des tournois au démarrage
  fetchTournaments();


  // version ameliorer 

  // Afficher un message pendant le chargement
function showLoading(message) {
    const tournamentList = document.getElementById('tournament-list');
    tournamentList.innerHTML = `<li>${message}</li>`;
  }
  
  // Récupérer la liste des tournois depuis l'API
  function fetchTournaments() {
    showLoading('Chargement des tournois...');
    
    fetch('/api/tournaments/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors du chargement des tournois.');
        }
        return response.json();
      })
      .then(tournaments => {
        const tournamentList = document.getElementById('tournament-list');
        tournamentList.innerHTML = '';
        if (tournaments.length === 0) {
          tournamentList.innerHTML = '<li>Aucun tournoi disponible pour le moment.</li>';
        } else {
          tournaments.forEach(tournament => {
            const listItem = document.createElement('li');
            listItem.textContent = tournament.name;
            listItem.onclick = () => fetchTournamentDetails(tournament.id);
            tournamentList.appendChild(listItem);
          });
        }
      })
      .catch(error => {
        console.error('Erreur:', error);
        showLoading('Erreur lors de la récupération des tournois.');
      });
  }
  
  // Récupérer les détails d'un tournoi via l'API
  function fetchTournamentDetails(tournamentId) {
    const detailsDiv = document.getElementById('tournament-details');
    detailsDiv.innerHTML = 'Chargement des détails...';
  
    fetch(`/api/tournaments/${tournamentId}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de la récupération des détails du tournoi.');
        }
        return response.json();
      })
      .then(tournament => {
        detailsDiv.innerHTML = `
          <h3>${tournament.name}</h3>
          <p>Statut: ${tournament.status}</p>
          <button onclick="joinTournament(${tournamentId}, 1)">Rejoindre le tournoi</button>
        `;
      })
      .catch(error => {
        console.error('Erreur:', error);
        detailsDiv.innerHTML = 'Erreur lors de la récupération des détails du tournoi.';
      });
  }
  
  // Fonction pour rejoindre un tournoi via l'API
  function joinTournament(tournamentId, playerId) {
    fetch(`/api/tournaments/${tournamentId}/join/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ player_id: playerId })
    })
      .then(response => response.json())
      .then(data => {
        alert(data.message || 'Erreur lors de la participation au tournoi.');
        fetchTournamentDetails(tournamentId); // Recharger les détails après avoir rejoint
      })
      .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de la participation au tournoi.');
      });
  }
  
  // Charger la liste des tournois au démarrage
  document.addEventListener('DOMContentLoaded', fetchTournaments);
  