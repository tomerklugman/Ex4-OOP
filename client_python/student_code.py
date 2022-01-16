"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from DiGraph import *
from GraphAlgo import *

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
Background=pygame.image.load("..\\pics\\background.jpg")
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

a = DiGraph()  # adding client graph to my graph
for node in graph.Nodes:
    x, y, z = node.pos.split(',')
    node.pos = SimpleNamespace(x=float(x), y=float(y))
    id = node.id
    a.add_node(id, (float(x), float(y), float(z)))
    for edge in graph.Edges:
        src = edge.src
        dest = edge.dest
        w = edge.w
        a.add_edge(src, dest, float(w))

algo = GraphAlgo(a)


 # get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15



client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


    # refresh surface
    screen.fill(Color(0, 0, 0))
    screen.blit(Background, (0, 0))


    # text on top

    getInfo = json.loads(client.get_info()).get("GameServer")

    grade = getInfo["grade"]
    gradeText = FONT.render(f"overall points: {grade}", True, Color(0, 0, 0))
    rect = gradeText.get_rect(center=(700, 10))
    screen.blit(gradeText, rect)

    time = FONT.render(f"time to end: {float(client.time_to_end()) / 1000}", True, Color(0, 0, 0))
    rect = time.get_rect(center=(860, 10))
    screen.blit(time, rect)

    moves = getInfo["moves"]
    movesText = FONT.render(f"moves: {moves}", True, Color(0, 0, 0))
    rect = movesText.get_rect(center=(1000, 10))
    screen.blit(movesText, rect)

    stopButton = FONT.render("click here to stop", True, Color(255, 0, 0))
    rect = stopButton.get_rect(center=(450, 10))
    screen.blit(stopButton, rect)

    message1 = FONT.render("low to high node is yellow pokemon", True, Color(0, 0, 0))
    rect = message1.get_rect(center=(142, 10))
    screen.blit(message1, rect)

    message2 = FONT.render("high to low node is red pokemon", True, Color(0, 0, 0))
    rect = message2.get_rect(center=(130, 30))
    screen.blit(message2, rect)


    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    agentIcon = pygame.image.load("..\\pics\\trainer.png")
    # draw agents
    for agent in agents:
        screen.blit(agentIcon, (int(agent.pos.x) - 20, int(agent.pos.y) - 20))

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    pokeplus = pygame.image.load("..\\pics\\pokplus.png")
    pokeminus = pygame.image.load("..\\pics\\pokminus.jpg")
    for p in pokemons:
        if p.type == -1:
            screen.blit(pokeminus, (int(p.pos.x) - 20, int(p.pos.y) - 20))
        if p.type == 1:
            screen.blit(pokeplus, (int(p.pos.x) - 20, int(p.pos.y) - 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x >= 380 and x <= 520 and y >= 0 and y <= 30:
                pygame.quit()
                exit(0)


    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.stop_connection()
            exit(0)




    # choose next edge
    for agent in agents:

        if agent.dest == -1:
            min = 1000000000

            for p in pokemons:
                for edge in graph.Edges:

                    srcX,srcY,zero1 = algo.algo.nodes.get(edge.src) # lets get edge and node postions
                    destX,destY,zero2 = algo.algo.nodes.get(edge.dest)

                    #lets calculate distances

                    nodeDist=pow((pow((my_scale(srcX,x=True)-my_scale(destX,x=True)),2) +pow((my_scale(srcY,y=True)-my_scale(destY,y=True)),2)),0.5) #distance from nodes
                    #distance from each node to pokemon
                    PokeDist=pow((pow((my_scale(srcX,x=True)-float(p.pos.x)),2)+pow((my_scale(srcY,y=True)-float(p.pos.y)),2)),0.5)+pow((pow((my_scale(destX,x=True)-float(p.pos.x)),2)+pow((my_scale(destY,y=True)-float(p.pos.y)),2)),0.5)


                    #if its less then epsilon then its on edge
                    if abs(nodeDist - PokeDist) < 0.0000001:
                        if p.type == -1: # high node to low node
                            destNode = edge.dest
                            break
                        if p.type == 1: # low node to high node
                            destNode = edge.src
                            break

                dist, shortestPath = algo.shortest_path(agent.src, destNode)  # find shortest path between agent and pokemon

                if dist == 0: #arrived to node
                    if p.type == -1: # high node to low node
                        destNode= edge.src
                    if p.type == 1: # low node to high node
                        destNode= edge.dest
                    next_node = destNode
                    break
                if dist < min:
                    min = dist
                    next_node = shortestPath[1]  # put next node in path

            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

            if int(ttl) <= 400:  # game finish screen
                while True:

                    screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
                    Background = pygame.image.load( "..\\pics\\background.jpg")
                    screen.blit(Background, [0, 0])

                    FONT = pygame.font.SysFont('Arial', 100, bold=True)

                    finish = FONT.render("GAME FINISHED!!!", True, Color(0, 0, 0))
                    rect = finish.get_rect(center=(550, 200))
                    screen.blit(finish, rect)

                    points = FONT.render(f"over all points: {grade}", True, Color(0, 0, 0))
                    rect = points.get_rect(center=(550, 400))
                    screen.blit(points, rect)

                    moves1 = FONT.render(f"moves: {moves}", True, Color(0, 0, 0))
                    rect = moves1.get_rect(center=(550, 500))
                    screen.blit(moves1, rect)

                    stopButton = FONT.render("click here to exit", True, Color(255, 0, 0))
                    rect = stopButton.get_rect(center=(550, 600))
                    screen.blit(stopButton, rect)

                    display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            client.stop()
                            client.stop_connection()
                            pygame.quit()
                            exit(0)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if x >= 230 and x <= 870 and y >= 570 and y <= 630:
                                pygame.quit()
                                exit(0)

        client.move()
