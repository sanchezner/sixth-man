import json
import os
from dotenv import load_dotenv
import psycopg2
# from nba_api.stats.endpoints import PlayerCareerStats, TeamGameLog, CommonTeamRoster, CommonPlayerInfo, CumeStatsTeamGames
# from nba_api.stats.static import players

load_dotenv()

conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

cur = conn.cursor()

# cur.execute('SELECT * FROM tenures;')
# test = cur.fetchall()
# h = {}

# for i in test:
#     h[i[0]] = []

# for j in test:
#     teammate_key = j[1:]
#     for k in test:
#         if (k[1:] == teammate_key) and k != j:
#             h[j[0]].append(list(k))

# with open('connections.json', 'w') as f:
#     json.dump(h, f, indent=4)

# t = PlayerCareerStats(player_id=2571, per_mode36='Totals').season_totals_regular_season.data['data']
# t = CumeStatsTeamGames(team_id=1610612737, season=2025).get_json()
# t = TeamGameLog(team_id=1610612766, season=2003).get_json()
# t = players.get_players()
# t = json.loads(t)

# print(t[-1])

# for i in t:
#     cur.execute("INSERT INTO tenures(player_id, team_id, season) VALUES (%s, %s, %s)", (i[0], i[3], i[1]))

# conn.commit()

# for i in t:
    # print(i)

# for i in t['data']:
#     print(f'player id: {i[0]}, team id: {i[3]}, season: {i[1]}')

# with open("test3.json", "w") as f:
#     json.dump(t, f, indent=4)

cur.execute("SELECT * FROM players")
p = cur.fetchall()
# print(p[:1])

print(p.index((78176, 'Belus Smawley')))