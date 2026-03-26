# note everything is commented because it wasn't possible to run it all cohesively due to nba.com's rate limits
# this file also isnt needed to run the app

import time
import random
import json, csv
import os
import psycopg2
from nba_api.stats.endpoints import PlayerCareerStats
from nba_api.stats.static import players, teams
from dotenv import load_dotenv

## --------------player data --------------
# load_dotenv()
# p = players.get_players()

# with open("players.json", "w") as f:
#     json.dump(p, f, indent=4)


try:
    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    cur = conn.cursor()
    

    ## -------------- load up all the players (1) --------------
    # p = players.get_players()
    # for player in p:
    #     cur.execute("INSERT INTO players(player_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (player['id'], player['full_name']))


    ## -------------- load up each player's career profile (team and season) (2) --------------
    # cur.execute("SELECT * FROM players")
    # p = cur.fetchall()

    # for player_id, player_name in p[5000:]: # had to do it in ranges ([0: 250], [250: 500], etc.) otherwise it would timeout
    #     try:
    #         career = PlayerCareerStats(player_id=player_id, per_mode36='Totals').season_totals_regular_season.data['data']
    #         for year in career:
    #             cur.execute("INSERT INTO tenures(player_id, team_id, season) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (year[0], year[3], year[1]))
    #     except Exception as e:
    #         with open('missing.txt', 'a') as f:
    #             f.write(f'{str(player_id)}: {e}')
    #             f.write('\n')
    #         continue

    #     time.sleep(random.randint(3,8))


    ## -------------- build connections via profiles (3) --------------
    # cur.execute('SELECT * FROM tenures;')
    # temp = cur.fetchall()
    # m = {}

    # for i in temp:
    #     m[i[0]] = []

    # for j in temp:
    #     teammate_key = j[1:]
    #     for k in temp:
    #         if (k[1:] == teammate_key) and k != j:
    #             m[j[0]].append(list(k))

    # with open('connections.json', 'w') as f:
    #     json.dump(m, f, indent=4)

    # conn.commit()
        

except Exception as e:
    print(f'Something went wrong: {e}')


## -------------- fill in team data (4) --------------
# t = teams.get_teams()
# m = {}
 
# with open('teams.json', 'w') as f: # basic team data
#     json.dump(t, f, indent=4)

# with open('data/teams.json', 'r') as f:
#     temp = json.load(f)
#     for i in temp:
#         m[i['id']] = []

# with open('data/NBA_Team_IDs.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         m[int(row['NBA_Current_Link_ID'])].append([row['Season'], row['BBRef_Team_Name']])

# with open('data/better_teams.json', 'w') as f:
#     json.dump(m, f, indent=4)