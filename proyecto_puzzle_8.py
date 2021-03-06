# Librerías
import queue as Q
import time
import math
import resource

# Clase que representa el Puzzle-n general

class PuzzleState(object):

    """docstring para PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """Expandir el nodo"""

        # Añadir nodos hijos en orden UDLR (Up-Down-Left-Right)

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

# Mis funciones
def writeOutput(resultado):
    """
    Función que escribe output.txt
    (Los estudiantes deben cambiar el método para que opere con los parametros necesarios).
    """

    ### SU CÓDIGO VA AQUÍ ###

    path_to_goal = resultado[0]
    cost_of_path = resultado[1]
    nodes_expande = resultado[2]
    search_depth = resultado[3]
    max_search_depth = resultado[4]

    file = open("output.txt","w")

    file.write(f"""path_to_goal: {path_to_goal}
cost_of_path: {cost_of_path}
nodes_expanded: {nodes_expande}
search_depth: {search_depth}               
max_search_depth: {max_search_depth} """)

    file.close()


#Funcion que indica si llego a la meta
def test_goal(puzzle_state):
    puzzle_completed = (0,1,2,3,4,5,6,7,8)
    if puzzle_state.config == puzzle_completed:
        return True


#Calculo de las heuristicas de las posiciones correctas
def calcular_heurisitica(estado):
    #estado = PuzzleState((1,2,5,3,4,0,6,7,8),3)
    correcto = [0,1,2,3,4,5,6,7,8]
    valor_correcto = 0
    piezas_correctas = 0
    piezas_incorrectas = 0

    for valor_pieza, valor_correcto in zip(list(estado.config), correcto):

        if valor_pieza == valor_correcto:
            piezas_correctas += 1

        else:
            piezas_incorrectas += 1

        valor_correcto += 1 

    return (piezas_incorrectas - 1) + estado.cost


#Funcion que calcula la ruta
def calcular_ruta(state):

    ruta = [state.action]

    ruta_padres = state.parent

    while ruta_padres:

        if ruta_padres.parent:
          ruta.append(ruta_padres.action)

        ruta_padres = ruta_padres.parent

    return ruta[::-1]


# Funcion que calcula el costo de una ruta
def calcular_costo(ruta):
    return len(ruta)


# Estructura de datos
# Queue Personalizado
class myQueue():

    def __init__(self, initial=""):
        self.lista = list()
        self.push(initial)

    def push(self, dato):
        self.lista.append(dato)

    def pop(self):
        dato = self.lista.pop(0)

        return dato

    def top(self):
        dato = self.lista[0]

        return dato

    def empty(self):
        return len(self.lista) == 0


#Stack Personalizado
class MyStack:

    def __init__(self, initial=""):
        self.lista = list()
        self.push(initial)

    def push(self, dato):
        self.lista.append(dato)

    def pop(self):
       dato = self.lista[-1]
       self.lista.pop()

       return dato

    def top(self):
        dato = self.lista[-1]

        return dato

    def empty(self):

        return len(self.lista) == 0


# PriorityQueue personalizado
class MyPriorityQueue:
    def __init__(self, initial=""):
        self.lista = []
        self.push(initial)
    
    def push(self, dato):
        self.lista.append(dato)

    def pop(self):
        self.lista = sorted(self.lista, key= lambda x : x[0])

        return self.lista.pop(0)

    def top(self):
        dato = self.lista[0]

        return dato

    def empty(self):
        return len(self.lista) == 0

#Algoritmos de busqueda

#BFS Search
def bfs_search(initial_state):

    frontier = myQueue(initial_state)
    frontier_dic = {}
    frontier_dic[tuple(initial_state.config)] = "add"
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            path_to_goal = calcular_ruta(state)
            search_depth = len(path_to_goal)     

            return (path_to_goal, 
                    state.cost, 
                    nodes_expanded, 
                    search_depth, 
                    max_search_depth)

        nodes_expanded += 1

        for node in state.expand():
            if tuple(node.config) not in frontier_dic and node.config not in explored:
                frontier_dic[tuple(node.config)] = "add"
                frontier.push(node)
                
                if node.cost > max_search_depth:
                    max_search_depth = node.cost

    return False


# DFS Search
def dfs_search(initial_state):
    frontier = MyStack(initial_state)
    frontier_dic = {}
    frontier_dic[tuple(initial_state.config)] = "add"
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            path_to_goal = calcular_ruta(state)
            cost_of_path = calcular_costo(path_to_goal)
            search_depth = len(path_to_goal)  

            return (path_to_goal, 
                    state.cost, 
                    nodes_expanded, 
                    search_depth, 
                    max_search_depth)

        nodes_expanded += 1

        for node in state.expand()[::-1]:
            if tuple(node.config) not in frontier_dic and node.config not in explored:
                frontier_dic[tuple(node.config)] = "add"
                frontier.push(node)

                if node.cost > max_search_depth:
                    max_search_depth = node.cost
                    
    return False


# A*Search
def A_star_search(initial_state):
    """A * search"""
    frontier = MyPriorityQueue((calcular_heurisitica(initial_state), initial_state))
    frontier_dic = {}
    frontier_dic[tuple(initial_state.config)] = "add"
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():  
        state_heuristic, state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            path_to_goal = calcular_ruta(state)
            search_depth = len(path_to_goal)     

            return (path_to_goal, 
                    state.cost, 
                    nodes_expanded, 
                    search_depth, 
                    max_search_depth)

        nodes_expanded += 1

        for node in state.expand():
            if tuple(node.config) not in frontier_dic and node.config not in explored:
                frontier_dic[tuple(node.config)] = "add"
                frontier.push((calcular_heurisitica(node), node))

                if node.cost > max_search_depth:
                    max_search_depth = node.cost
    return False


# Funcion principal llamada desde el punto de acceso
def run():
    
    data = input() 

    agente_busqueda = data[:3].lower()
    numeros_data = data[3:]
    numeros_fichas = list(numeros_data)
    numeros_fichas = tuple(map(int, numeros_fichas))

    size = int(math.sqrt(len(numeros_fichas)))

    hard_state = PuzzleState(numeros_fichas, size)

    if agente_busqueda == "bfs":
        resultado = bfs_search(hard_state)

    elif agente_busqueda == "dfs":
        resultado = dfs_search(hard_state)

    elif agente_busqueda == "ast":
        resultado = A_star_search(hard_state)

    writeOutput(resultado)


#Punto de acceso
if __name__ == '__main__':
    run()
