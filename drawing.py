import cv2 as cv
import numpy as np
from graph import *

class GraphDrawer:
    def __init__(self, graph: Graph, canvasWidth: int, canvasHeight: int, scale= 1.0) -> None:
        self.graph= graph
        self.scale= scale
        self.canvasWidth= canvasWidth
        self.canvasHeight= canvasHeight

        self.adjacencyMatrix= self.graph.adjacencyMatrix
        self.graphPos= np.random.random((len(self.graph.vertices), 2))
        self.graphPos[:, 0]*= canvasWidth
        self.graphPos[:, 1]*= canvasHeight
        self.graphVelocity= np.zeros_like(self.graphPos)
        self._calcDistances()

    def draw(self, canvas: np.ndarray, path= None):
        self._drawEdges(canvas)
        self._drawVertices(canvas)
        if path != None: self._drawPath(canvas, path)

    def _drawVertices(self, canvas: np.ndarray):
        for i, vertexPos in enumerate(self.graphPos):
            cv.circle(canvas, vertexPos.astype(np.int32), 8, (255,255,255), -1)
            cv.putText(canvas, self.graph.vertices[i], (vertexPos + [9,4]).astype(np.int32), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0))

    def _drawEdges(self, canvas: np.ndarray):
        for i, vertex in enumerate(self.adjacencyMatrix):
            for j, value in enumerate(vertex):
                if value != -1:
                    cv.line(canvas, self.graphPos[i].astype(np.int32), self.graphPos[j].astype(np.int32), (0, 0, 255), 1)
                    # cv.arrowedLine(canvas, self.graphPos[i].astype(np.int32), self.graphPos[j].astype(np.int32), (0, 0, 255), 1)

    def _drawPath(self, canvas: np.ndarray, path: list):
        lastIndex= self.graph.vertices.index(path[1])
        for vertex in path[2:]:
            index= self.graph.vertices.index(vertex)
            point1= self.graphPos[lastIndex]
            point2= self.graphPos[index]
            # cv.line(canvas, point1.astype(np.int32), point2.astype(np.int32), (255,0,0), 2)
            cv.arrowedLine(canvas, point1.astype(np.int32), point2.astype(np.int32), (255,0,0), 2)
            lastIndex= index

    def update(self, iterations= 1):
        for i in range(iterations):
            applyingVelocity= np.where(
                self.graphVelocity > 0,
                np.ones_like(self.graphVelocity),
                -np.ones_like(self.graphVelocity)
            ) * np.log10(np.abs(self.graphVelocity) + 1)
            self.graphPos+= applyingVelocity

            self._calcDistances()
            absAdjacency= np.where(self.adjacencyMatrix == -1, np.zeros_like(self.adjacencyMatrix), self.adjacencyMatrix)
            meanAdjacency= (absAdjacency + absAdjacency.T) / 2
            reshapedMeanAdjacency= np.tile(np.reshape(meanAdjacency, (*meanAdjacency.shape, 1)), (1,1,2))
            reshapedDistances= np.tile(np.reshape(self.distances, (*self.distances.shape, 1)), (1,1,2))
            unitVectors= np.divide(self.vectors, reshapedDistances, where= reshapedDistances != 0)
            forces= np.where(
                reshapedMeanAdjacency != 0,
                (reshapedDistances - (reshapedMeanAdjacency*75)) * unitVectors * 0.01,
                np.zeros_like(unitVectors)
            )
            repulsion= np.where(
                reshapedDistances != 0,
                10 * np.ones_like(reshapedDistances)/reshapedDistances * unitVectors,
                np.zeros_like(self.vectors)
            )
            gravity= -(self.graphPos - np.array([self.canvasWidth/2, self.canvasHeight/2], np.float64)) * 0.001

            # print(repulsion, sep= '\n\n')

            self.graphVelocity= np.sum(forces - repulsion, axis=0) + gravity

    def _calcDistances(self):
        self.vectors= np.zeros((*self.adjacencyMatrix.shape, 2), np.float64)
        self.distances= np.zeros_like(self.adjacencyMatrix)
        graphPos_2d= np.reshape(self.graphPos, (1, *self.graphPos.shape))
        tiledPos= np.tile(graphPos_2d, (len(self.graphPos), 1, 1))
        self.vectors+= np.transpose(tiledPos, axes=(1,0,2)) - tiledPos
        self.distances+= np.sqrt(np.sum((self.vectors) ** 2, axis= 2))

        
    
