import json
from collections import deque

class Graph:
    def __init__(self):
        self.adj = dict()
    
    def add_node(self, val):
        if val not in self.adj:
            self.adj[val] = {}
        
    def add_edge(self, p1, p2, team_id, season):
        self.add_node(p1)
        self.add_node(p2)
        
        if p2 not in self.adj[p1]:
            self.adj[p1][p2] = []
        if p1 not in self.adj[p2]:
            self.adj[p2][p1] = []
        
        # teammates go both ways so when we add all players to the graph, we will find duplicated connections; this guard prevents that
        connection = (team_id, season)
        if connection not in self.adj[p1][p2]:
            self.adj[p1][p2].append(connection)
            self.adj[p2][p1].append(connection)

    @classmethod
    def build(cls, path): # loading all of the data and building the graph
        graph = cls()

        with open(path, 'r') as f:
            data = json.load(f)

        # crazy inefficient but we ball (fix this soon)
        for player_id, connections in data.items():
            player_id = int(player_id)
            for teammate_id, team_id, season in connections:
                graph.add_edge(player_id, teammate_id, team_id, season)
        
        return graph
    
    def bfs(self, start, end):
        q = deque()
        q.appendleft(start)
        visited = {}
        # using the dict to store parent nodes values at children keys, this way we can easily go back upward (inward?)
        visited[start] = None

        while q:
            current = q.pop()
            if current == end:
                break

            for teammate in self.adj[current]:
                if not any(conn[0] != 0 for conn in self.adj[current][teammate]):
                    continue
                if teammate not in visited:
                    q.appendleft(teammate)
                    visited[teammate] = current

        t = end
        path = []
        while t is not None: # going backwards (outward -> in)
            path.append(t)
            t = visited[t]
        path.reverse()

        result = []
        for i in range(len(path)):
            if i < len(path) - 1: # every node that isn't last gives [player_id, team_id, year]; the team and year is the edge it shares with its teammate in front of it
                connections = self.adj[path[i]][path[i + 1]]
                valid = None
                for conn in connections:
                    if conn[0] != 0:
                        valid = conn
                        break
                        
                if valid is None:
                    continue

                result.append([int(path[i]), valid[0], valid[1]])
            else: # last node gives player id only
                result.append(int(path[i]))
        
        return result
                
    def dfs(self, start, end): # almost exactly the same as bfs, just lifo
        s = [start]
        visited = {}
        visited[start] = None

        while s:
            current = s.pop()
            if current == end:
                break

            for teammate in self.adj[current]:
                if not any(conn[0] != 0 for conn in self.adj[current][teammate]):
                    continue
                if teammate not in visited:
                    s.append(teammate)
                    visited[teammate] = current

        t = end
        path = []
        while t is not None:
            path.append(t)
            t = visited[t]
        path.reverse()

        result = []
        for i in range(len(path)):
            if i < len(path) - 1: 
                connections = self.adj[path[i]][path[i + 1]]
                valid = None
                for conn in connections:
                    if conn[0] != 0:
                        valid = conn
                        break
                        
                if valid is None:
                    continue

                result.append([int(path[i]), valid[0], valid[1]])
            else:
                result.append(int(path[i]))
        
        return result