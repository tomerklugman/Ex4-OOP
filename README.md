
# Ex4-OOP
# pokemon game


##### creation of a pokemon game with graph data structure from previous project Ex3 which contains: 
###### the two main files are client.py and student_code.py:

- client.py contains the main functions to which we interact with the server
- student_code.py contains the connection to the server and agent pokemon algorithm with gui 
##### results of cases 0-15 will be in the wiki

-------------

### algorithm explanation

in this project we need to catch the maximal number of pokemons with given number of agents. each pokemon will appear on an edge between connected nodes. first we will check between which nodes the pokemon exists. if pokemon is on that edge, we calculate distance between nodes and between pokemon and nodes, which should be almost equal to a very minimal epsilon. in this game we have 2 types of pokemon because the graph is a directed graph, each node has outgoing and ingoing edges. type 1(will have yellow icon) is a pokemon that exists from low node(1) to higher node(2), type -1(will have red icon) is a pokemon that exists from high node(2) to low node(1). if its a a type 1 pokemon we will send the agent to the edge source and then to the edge destination to catch the pokemon on the edge, same will happen with type -1 just the opposite way. we will use shortest path algorithm which implemented by dijkstras algorithm to keep updating distances to pokemons and shortest paths.

at the end of the game, there will be an game over screen which will represent the amount of moves and grade achieved.


----
### UML
![alt text](https://i.imgur.com/ZHUkFzZ.png)
----
## requirements

required imports are:

for the game:

pygame

for the graph representation:

matplotlib

numpy

pandas

----
## how to run
open main foler where Ex4_Server_v0.0 is, and open cmd in that folder with this command
change the 0 at the end to 0 to 15 cases like: java -jar Ex4_Server_v0.0.jar 13
```sh
java -jar Ex4_Server_v0.0.jar 0
```
then open client_python folder and open cmd in that folder with this command
```sh
py student_code.py
```
if it doesnt work you have to install pygame and run student_code.py in your interperter
an example of running the code is in the wiki
