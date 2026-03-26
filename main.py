from backend.graph import Graph
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['GET'])

app.mount('/static', StaticFiles(directory='static'), name='static')
g = Graph.build('data/connections.json')

@app.get('/')
def index():
    return FileResponse('static/index.html')

@app.get('/search')
def search_graph(start, end, traversal):
    if traversal == 'bfs':
        result = g.bfs(int(start), int(end))
        return result
    elif traversal == 'dfs':
        result = g.dfs(int(start), int(end))
        return result

@app.get('/players')
def get_players():
    with open('data/players.json') as f:
        return json.load(f)

@app.get('/teams')
def get_players():
    with open('data/better_teams.json') as f:
        return json.load(f)
    
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)