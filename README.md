#Footyapp Backend - REST API

This is the backend to the footyapp for querying the database using REST.

Here is a list of the commands:

# GET /players

Returns a list of all players from the database.
The fields are:
- id
- name
- total

Use filters to manipulate the result. A python function example below:

```
player_api_url = "http://footyapp-api:8080/players"

def get_playing_players(player_api_url):
    response = requests.get(player_api_url)

    if response.status_code == 200:
        players = response.json()
        playing_players = [{  
                player["name"], 
                player["playing"]
                } for player in players if player.get("playing")
        ]
        return playing_players
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []
```


# POST /players

Posts a new player. Must be in JSON format using the following syntax:

```
    {
      "name": "Amy",
      "total": 77,
      "wins": 0,
      "draws": 0,
      "losses": 0,
      "score": 0,
      "playing": true,
      "played": 0,
      "percent": 0,
      "winpercent": 0
    }
```