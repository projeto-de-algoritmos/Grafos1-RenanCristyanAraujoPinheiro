# Nome: Renan Cristyan Araújo Pinheiro
# Matrícula: 17/0044386

# Código retirado de: http://prorum.com/?qa=2414/implementar-extrair-informacoes-conectividade-aciclicidade
# Acesso em 02 de Abril de 2019

import numpy as np
from collections import deque
from sortedcontainers import SortedSet

class Graph:
    def __init__(self, directedGraph=False):
        self.__V = list()
        self.__directedGraph = directedGraph
        self.__time = 0
        return
      
    def addVertex(self, v):
        if (not (v in self.__V)):
            v.setIndex(len(self.__V))
            self.__V.append(v)
        return v

    def createVertex(self):
        return self.addVertex(Vertex(self))

    def addEdge(self, u, v):
        if (isinstance(u, Vertex) and isinstance(v, Vertex)):
            if ((u in self.__V) and (v in self.__V)):
                u.addAdjacentVertex(v)

                if (not self.__directedGraph):
                    v.addAdjacentVertex(u)

                return
            else:
                raise("addEdge error. u and v must belong to graph.")
        elif (isinstance(u, int) and isinstance(v, int)):
            self.addEdge(self[u], self[v])
        else:
            raise("addEdge error. u and v must be of class Vertex or integers.")
        return

    def __getitem__(self, k):
        if ((len(self.__V) > 0) and (k >= 0) and (k < len(self.__V))):
            return self.__V[k]
        return None

    def __len__(self):
        return len(self.__V)

    def __str__(self):
        graphStr = str("")
        for index, vertex in enumerate(self.__V):
            graphStr += str(vertex)
            if (index < len(self.__V) - 1):
                graphStr += "\n"
        return graphStr

    def setVertexListAsUnexplored(self):
        for v in self.__V:
            v.setAsUnexplored()
        return

    def BFS(self, source=0, exploreObj=None):
        self.setVertexListAsUnexplored()

        if ((exploreObj is not None) and (source != exploreObj.getInitialVertexIndex())):
            source = exploreObj.getInitialVertexIndex()

        self[source].d = 0
        self[source].explore(exploreObj)

        queue = deque([self[source]])

        while len(queue)!=0:
            v = queue.popleft()

            for adjacentVertex in v.getAdjacentVertexSet():
                if(not adjacentVertex.wasExplored()):
                    adjacentVertex.predecessor = v
                    adjacentVertex.d = v.d + 1
                    adjacentVertex.explore(exploreObj)

                    queue.append(adjacentVertex)

        return exploreObj

    def DFS_Stack(self, exploreObj=None):
        self.setVertexListAsUnexplored()

        self.__time = 0

        for vertex in self.__V:
            if (not vertex.wasExplored()):
                self.__DFS_VISIT_STACK(vertex, exploreObj)

        return exploreObj

    def __DFS_VISIT_STACK(self, initialVertex, exploreObj=None):

        stack = deque([initialVertex])
        while len(stack)!=0:
            vertex = stack.pop()

            if (not vertex.wasExplored()):
                self.__time += 1
                vertex.d = self.__time
                vertex.explore(exploreObj)

                stack.append(vertex)

                for adjacentVertex in reversed(vertex.getAdjacentVertexSet()):
                    if (not adjacentVertex.wasExplored()):
                        adjacentVertex.predecessor = vertex
                        stack.append(adjacentVertex)
            else:
                if (vertex.f == np.inf):
                    self.__time += 1
                    vertex.f = self.__time

        return exploreObj

    def DFS_Rec(self, exploreObj=None):
        self.setVertexListAsUnexplored()

        self.__time = 0

        for vertex in self.__V:
            if (not vertex.wasExplored()):
                self.__DFS_VISIT_REC(vertex, exploreObj)

        return exploreObj

    def __DFS_VISIT_REC(self, vertex, exploreObj=None):

        self.__time += 1
        vertex.d = self.__time
        vertex.explore(exploreObj)

        for adjacentVertex in vertex.getAdjacentVertexSet():
            if(not adjacentVertex.wasExplored()):
                adjacentVertex.predecessor = vertex
                self.__DFS_VISIT_REC(adjacentVertex, exploreObj)

        self.__time += 1
        vertex.f = self.__time

        return exploreObj

    def isConnected(self):

        if (self.__directedGraph):
            for v in self.__V:
                self.setVertexListAsUnexplored()
                self.__DFS_VISIT_REC(v, None)
                for u in self.__V:
                    if (u.d == np.inf):
                        return False
            return True
        else:
            self.BFS(0, None)

            for v in self.__V:
                if (v.d == np.inf):
                    return False

            return True

    def isAcyclic(self):
        if (self.__directedGraph):
            self.DFS_Stack(None)
            for u in self.__V:
                for v in u.getAdjacentVertexSet():
                    if (Edge.isBackEdge(u, v)):
                        return False
            return True
        return False

    def getArticulationPoints(self):
        articulationPoints = list()

        n = len(self.__V)
        for i in range(n):
            vertex = self.__V.pop(0)

            if (not self.isConnected()):
                articulationPoints.append(vertex)

            self.__V.append(vertex)

        return articulationPoints


    def topologicalSort(self):
        if (self.isAcyclic()):
            self.DFS_Stack()

            self.__V = sorted(self.__V, cmp=topological_comparator, reverse=True)
        else:
            raise("Topological sort not possible. Graph is not acyclic.")


def topological_comparator(u, v):
        return u.f - v.f

class Edge:
    @staticmethod
    def isBackEdge(u, v):
        return (v.d <= u.d) and (u.d < u.f) and (u.f <= v.f)

    @staticmethod
    def isTreeEdgeOrForwardEdge(u, v):
        return (u.d < v.d) and (v.d < v.f) and (v.f < u.f)

    @staticmethod
    def isCrossEdge(u, v):
        return (v.d < v.f) and (v.f < u.d) and (u.d < u.f)

class Vertex:
    def __init__(self, parentGraph, index=0):
        self.__parentGraph = parentGraph
        self.__index = index
        self.__adjacentVertexSet = SortedSet()
        self.__explored = False
        self.__name = ""

        self.d = np.inf
        self.f = np.inf
        self.predecessor = None

    def setIndex(self, index):
        self.__index = index

    def getIndex(self):
        return self.__index

    def addAdjacentVertex(self, adjacentVertex):
        if (isinstance(adjacentVertex, Vertex)):
            if (not (adjacentVertex in self.__adjacentVertexSet)):
                self.__adjacentVertexSet.add(adjacentVertex)
        else:
            raise("addAdjacentVertex error. adjacentVertex must be of class Vertex.")
        return

    def setName(self, name):
        self.__name = name
        return self

    def getName(self):
        if (len(self.__name) == 0):
            return str(self.__index)
        return self.__name

    def getAdjacentVertexSet(self):
        return self.__adjacentVertexSet

    def wasExplored(self):
        return self.__explored

    def setAsUnexplored(self):
        self.__explored = False
        self.d = np.inf
        self.f = np.inf
        self.predecessor = None
        return

    def explore(self, exploreObj=None):
        if ((not self.__explored) and (exploreObj is not None)):
            exploreObj.explore(self)

        self.__explored = True

        return

    def vertex2str(self, showCompleteInfo=False):
        vertexStr = str("")
        vertexStr += self.getName()
        if (showCompleteInfo):
            vertexStr += " [d=" + str(self.d) + "][f=" + str(self.f) + "]"
        vertexStr += " -> "

        if (len(self.__adjacentVertexSet) > 0):
            for adjacentVertex in self.__adjacentVertexSet:
                vertexStr += " " + adjacentVertex.getName()

        return vertexStr

    def __lt__(self, other):
        return self.__index < other.__index

    def __gt__(self, other):
        return self.__index > other.__index

    def __str__(self):
        return self.vertex2str()

class CExplore:
    def __init__(self, graph = None):
        self._graph = graph
        self.__initialVertexIndex = 0
        self._indexVertex1 = -1
        self._indexVertex2 = -1
        return

    def check(self, indexVertex1, indexVertex2):
        if (isinstance(indexVertex1, Vertex) and isinstance(indexVertex2, Vertex)):
            return self.check(indexVertex1.getIndex(), indexVertex2.getIndex())

        elif (isinstance(indexVertex1, int) and isinstance(indexVertex2, int)):
            self._indexVertex1 = indexVertex1

            self._indexVertex2 = indexVertex2

            self.setInitialVertexIndex(indexVertex1)

            self._makeCalculations()

        else:
            raise("Error! u and v must be of class Vertex or integers.")

        return self

    def _makeCalculations(self):
        return self

    def setInitialVertexIndex(self, index):
        self.__initialVertexIndex = index
        return

    def getInitialVertexIndex(self):
        return self.__initialVertexIndex

    def explore(self, vertex):
        print ("Exploring vertex ", vertex.getIndex(), " d=", vertex.d)

class CShortestPath(CExplore):
    def __init__(self, graph):
        CExplore.__init__(self, graph)

        self.__shortestPath = np.inf

        self.__path = list()

        return

    def _makeCalculations(self):
        self.__shortestPath = np.inf

        self.__path = list()

        self._graph.BFS(self._indexVertex1, self)

        return self

    def explore(self, vertex):

        if (self._indexVertex2 == vertex.getIndex()):
            self.__shortestPath = vertex.d

            v = vertex
            while (v is not None):
                self.__path.insert(0, v.getIndex())
                v = v.predecessor

        return

    def getShortestPath(self):
        return self.__shortestPath

    def getPathVertexList(self):
        return self.__path

    def __str__(self):
        shortestPathStr = str("Shortest path: ")
        shortestPathStr += str(self.getPathVertexList())
        shortestPathStr += " -> "
        shortestPathStr += str(self.getShortestPath())
        return shortestPathStr