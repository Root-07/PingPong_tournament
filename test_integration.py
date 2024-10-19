import requests

def test_create_tournament():
    url = 'http://127.0.0.1:8000/api/tournaments/'
    data = {'name': 'Integration Tournament', 'max_players': 8}
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Integration Tournament'

def test_join_tournament():
    # Create a player
    player_url = 'http://127.0.0.1:8000/api/players/'
    player_data = {'name': 'Integration Player'}
    player_response = requests.post(player_url, json=player_data)
    if player_response.status_code != 201:
        print("Error creating player:", player_response.json())
    assert player_response.status_code == 201
    player_id = player_response.json()['id']

    # Create a tournament
    tournament_url = 'http://127.0.0.1:8000/api/tournaments/'
    tournament_data = {'name': 'Integration Tournament', 'max_players': 8}
    tournament_response = requests.post(tournament_url, json=tournament_data)
    assert tournament_response.status_code == 201
    tournament_id = tournament_response.json()['id']

    # Join the tournament
    join_url = f'http://127.0.0.1:8000/api/tournaments/{tournament_id}/join/'
    join_data = {'player_id': player_id}
    join_response = requests.post(join_url, json=join_data)
    assert join_response.status_code == 200
    assert join_response.json()['message'] == 'Player joined the tournament'