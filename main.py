from math import inf, sqrt
from time import sleep
import pygame
import pygame.gfxdraw as gfxdraw
import sys
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

## COLORS
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

pygame.init()
SCREEN_W = SCREEN_H = 700
screen = pygame.display.set_mode((SCREEN_W , SCREEN_H))
screen.fill(white)

def display_graph(graph):
    for vertex in graph.verteces:
        pygame.draw.circle(screen, blue, (vertex.x,vertex.y), 2, 2)
    for edge in graph.edges:
        pygame.draw.line(screen, red, (edge.v1.x,edge.v1.y), (edge.v2.x,edge.v2.y))
        
    pol = [(vertex.x, vertex.y) for vertex in graph.verteces]
    if len(pol) != 0:
        gfxdraw.filled_polygon(screen, pol, green)
        
    pygame.display.update()


class Graph:
    def __init__(self):
        self.verteces = list()
        self.edges = list()
    
    def get_connected_verteces(self):
        connected_verteces = list()
        for edge in self.edges:
            for vertex in [edge.v1, edge.v2]:
                if vertex not in connected_verteces:
                    connected_verteces.append(vertex)
        return connected_verteces
            
    
    def get_area(self):
        outer_bound_dots = [(vertex.x , vertex.y) for vertex in self.get_connected_verteces()]
        pgon = Polygon(zip([d[0] for d in outer_bound_dots ], [d[1] for d in outer_bound_dots]))
        return pgon.area


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.dfc = inf ## distance from centroid

class Edge:
    def __init__(self, vertex1 : Vertex , vertex2: Vertex):
        self.v1 = vertex1
        self.v2 = vertex2
        
        
def constructGraph(input_graph : Graph , file_path, scale=5):
    with open(file_path, "r") as f:
        points = [p for p in f.read().split("\n") if p!=""]
    for point in points:
        x, y = point.split(" ")[:2]
        input_graph.verteces.append(Vertex(scale*int(x), scale*int(y)))
    return input_graph
    ...
    
def total_area_centroid_of_graph(graph: Graph):
    ratio = 0.95
    XS = []
    YS = []
    for vertex in graph.verteces:
        XS.append(vertex.x)
        YS.append(vertex.y)
    leftmost_x = min(XS)
    rightmost_x = max(XS)
    top_y = min(YS)
    bottom_y = max(YS)
    outer_bound_dots = [(leftmost_x,top_y), (leftmost_x,bottom_y), (rightmost_x,bottom_y), (rightmost_x,top_y)]
    pgon = Polygon(zip([d[0] for d in outer_bound_dots ], [d[1] for d in outer_bound_dots]))
    target_area = ratio * pgon.area
    # x,y = pgon.exterior.xy
    # plt.plot(x,y)
    # plt.show()
    # print(pgon.area)
    return target_area, (pgon.centroid.x, pgon.centroid.y)


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1)**2 + (y2-y1)**2)


def display_info_on_screen(screen , target_area, current_area, generation):
    text = font.render('Target Area: {}'.format(target_area), True, green, blue)
    textRect = text.get_rect()
    textRect.center = (SCREEN_W*0.2, SCREEN_H*0.8)
    screen.blit(text, textRect)
    text = font.render('Current Area: {}'.format(current_area), True, green, blue)
    textRect = text.get_rect()
    textRect.center = (SCREEN_W*0.2, SCREEN_H*0.85)
    screen.blit(text, textRect)
    text = font.render('Generation: {}'.format(generation), True, green, blue)
    textRect = text.get_rect()
    textRect.center = (SCREEN_W*0.2, SCREEN_H*0.9)
    screen.blit(text, textRect)

def update_edges(graph, centeroid):
    if len(graph.edges) == 0:
        ## initialize the polygon with a triangle
        
        ## first sort verteces by their distance from centroid
        for vertex in graph.verteces:
            vertex.dfc = distance((vertex.x, vertex.y) , (centeroid[0], centeroid[1]))
        
        graph.verteces.sort(key=lambda x:x.dfc , reverse=False)
        graph.edges.append(Edge(graph.verteces[0], graph.verteces[1]))
        graph.edges.append(Edge(graph.verteces[0], graph.verteces[2]))
        graph.edges.append(Edge(graph.verteces[2], graph.verteces[1]))
        
        ...
            
            
        
    
empty_graph = Graph()
graph = constructGraph(empty_graph, r"verteces.txt")
target_area , centeroid =  total_area_centroid_of_graph(graph)
area_threshhold = 0.9

font = pygame.font.Font('freesansbold.ttf', 20)


generation = 0

while True:
    display_info_on_screen(screen, target_area, 0, generation)
    display_graph(graph)
    
    update_edges(graph, centeroid)
    
    generation += 1
    sleep(0.5)
    ...