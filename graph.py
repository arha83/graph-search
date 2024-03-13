import numpy as np
from typing import Tuple

class Graph:
    def __init__(self, vertices: list, edges: list) -> None:
        self.vertices= vertices
        self.edges= edges # (from, to, value)
        self.adjacencyMatrix= -np.ones((len(self.vertices), len(self.vertices)), dtype= np.float64)
        for edge in self.edges:
            fromIndex= self.vertices.index(edge[0])
            toIndex= self.vertices.index(edge[1])
            edgeValue= edge[2]
            self.adjacencyMatrix[fromIndex, toIndex]= edgeValue

    def adjacent(self, fromVertex, toVertex) -> float:
        fromIndex= self.vertices.index(fromVertex)
        toIndex= self.vertices.index(toVertex)
        return self.adjacencyMatrix[fromIndex, toIndex]
    
    def neighbors(self, vertex) -> Tuple[list, list]:
        neighbors= []
        values= []
        for v in self.vertices:
            if (value:= self.adjacent(vertex, v)) != -1:
                neighbors.append(v)
                values.append(value)
        return neighbors, values
    
    def addVertex(self, vertex) -> None:
        self.vertices.append(vertex)
        self.adjacencyMatrix= -np.ones((len(self.vertices), len(self.vertices)), dtype= np.float64)
        for edge in self.edges:
            fromIndex= self.vertices.index(edge[0])
            toIndex= self.vertices.index(edge[1])
            edgeValue= edge[2]
            self.adjacencyMatrix[fromIndex, toIndex]= edgeValue

    def addEdge(self, fromVertex, toVertex, value) -> None:
        self.edges.append((fromVertex, toVertex, value))
        fromIndex= self.vertices.index(fromVertex)
        toIndex= self.vertices.index(toVertex)
        self.adjacencyMatrix[fromIndex, toIndex]= value

    def removeVertex(self, vertex) -> None:
        self.vertices.remove(vertex)
        removingEdges= []
        for edge in self.edges:
            fromVertex= edge[0]
            toVertex= edge[1]
            if fromVertex == vertex or toVertex == vertex: removingEdges.append(edge)
        while len(removingEdges) != 0:
            edge= removingEdges.pop()
            self.edges.remove(edge)
        self.adjacencyMatrix= -np.ones((len(self.vertices), len(self.vertices)), dtype= np.float64)
        for edge in self.edges:
            fromIndex= self.vertices.index(edge[0])
            toIndex= self.vertices.index(edge[1])
            edgeValue= edge[2]
            self.adjacencyMatrix[fromIndex, toIndex]= edgeValue
    
    def removeEdge(self, fromVertex, toVertex) -> None:
        for edge in self.edges:
            if edge[0] == fromVertex and edge[1] == toVertex:
                self.edges.remove(edge)

    def getGraphDict(self) -> dict:
        return dict(zip(self.vertices, [[*zip(self.neighbors(v)[0], self.neighbors(v)[1])] for v in self.vertices]))

    def uniformCostSearch(self, startVertex, goalVertex) -> list | None:
        path= [0, startVertex]
        que= [path]
        expanded= set()
        while True:
            if len(que) == 0: return None
            path= que.pop(que.index(min(que, key= lambda p: p[0])))
            # print(path)
            node= path[-1]
            if node == goalVertex: return path
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]+= cost
                    neighborPath.append(neighbor)
                    que.append(neighborPath)
    
    def depthFirstSearch(self, startVertex, goalVertex) -> list | None:
        path= [0, startVertex]
        que= [path]
        expanded= set()
        while True:
            if len(que) == 0: return None
            path= que.pop() # was it that easy???
            # print(path)
            node= path[-1]
            if node == goalVertex: return path
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]+= cost
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

    def breadthFirstSearch(self, startVertex, goalVertex) -> list | None:
        path= [0, startVertex]
        que= [path]
        expanded= set()
        while True:
            if len(que) == 0: return None
            path= que.pop(0) # really!?
            # print(path)
            node= path[-1]
            if node == goalVertex: return path
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]+= cost
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

    def AStarSearch(self, startVertex, goalVertex, heuristics: dict) -> list | None:
        path= [heuristics[startVertex], startVertex]
        que= [path]
        expanded= set()
        while True:
            if len(que) == 0: return None
            path= que.pop(que.index(min(que, key= lambda p: p[0]))) # it's fine I guess...
            # print(path)
            node= path[-1]
            if node == goalVertex: return path
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]= path[0] - heuristics[node] + cost + heuristics[neighbor]
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

    def uniformCostSearch_yield(self, startVertex, goalVertex) -> list | None:
        path= [0, startVertex]
        que= [path]
        paths= []
        expanded= set()
        while True:
            if len(que) == 0: break
            path= que.pop(que.index(min(que, key= lambda p: p[0])))
            paths.append(path)
            # print(path)
            node= path[-1]
            if node == goalVertex: break
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]+= cost
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

        for path in paths: yield path
    
    def depthFirstSearch_yield(self, startVertex, goalVertex) -> list | None:
        path= [0, startVertex]
        paths= []
        que= [path]
        expanded= set()
        while True:
            if len(que) == 0: break
            path= que.pop() # was it that easy???
            paths.append(path)
            node= path[-1]
            if node == goalVertex: break
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]+= cost
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

        for path in paths: yield path

    def breadthFirstSearch_yield(self, startVertex, goalVertex) -> list | None:
        path= [0, startVertex]
        que= [path]
        paths= []
        expanded= set()
        while True:
            if len(que) == 0: break
            path= que.pop(0) # really!?
            paths.append(path)
            # print(path)
            node= path[-1]
            if node == goalVertex: break
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]+= cost
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

        for path in paths: yield path

    def AStarSearch_yield(self, startVertex, goalVertex, heuristics: dict) -> list | None:
        path= [heuristics[startVertex], startVertex]
        que= [path]
        paths= []
        expanded= set()
        while True:
            if len(que) == 0: break
            path= que.pop(que.index(min(que, key= lambda p: p[0]))) # it's fine I guess...
            paths.append(path)
            # print(path)
            node= path[-1]
            if node == goalVertex: break
            expanded.add(node)
            for (neighbor, cost) in zip(*self.neighbors(node)):
                if not neighbor in expanded:
                    neighborPath= path.copy()
                    neighborPath[0]= path[0] - heuristics[node] + cost + heuristics[neighbor]
                    neighborPath.append(neighbor)
                    que.append(neighborPath)

        for path in paths: yield path


