# Sixth Man
## What is this?
Sixth Man is a "six degrees of separation" app for the NBA. Given any two players, it finds the shortest chain of mutual teammates connecting them using Breadth-First Search or Depth-First Search.

## Quick Start
1. Navigate to your folder and clone the repository:
```bash
git clone https://github.com/sanchezner/sixth-man
cd sixth-man
```

2. Set up virtual environment:
From the project root `/sixth-man`, run:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install uvicorn
pip install flask
pip install flask-cors
```

4. Run the program:
From the project root, with the virtual environment activated `(.venv) /sixth-man`, run the main file:
```bash
python main.py
```
or another method.

5. Visit localhost on your browser:
`http://0.0.0.0:5000/`

## How?
Player, team, and career data are sourced from [nba_api](https://github.com/swar/nba_api) and stored in a PostgreSQL database. Each player's team history is used to build a teammate graph, where edges are defined by two players playing on the same team in the same season. 

When it's time to compute, the app runs either BFS or DFS depending on input over an adjacency list to find a path between the two selected players. Each edge/connection in the result carries the shared team and season, which the frontend uses to render the cards.

Extraneous team details like historical names and logos were sourced from [this repository](https://github.com/djblechn-su/nba-player-team-ids/blob/master/NBA_Team_IDs.csv) and [sportslogohistory](https://sportslogohistory.com/nba-logo-history) respectively.

## Tech Stack
- FastAPI, Uvicorn for backend/hosting
- Vanilla JS, Fuse.js (search), CSS for frontend
- nba_api, PostreSQL for data pipeline