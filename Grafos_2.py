# Nome: Renan Cristyan Araujo Pinheiro
# Matrícula: 17/0044386

# Código bastante incompleto, mas foi o que eu consegui fazer...

# Cada nó do grafo é um objeto do tipo Node
class Node(object):
  def __init__(self, value, name = None, adj = None, visited = False):
    self.value = value       # Valor do nó
    self.name = name         # Nome do nó (para facilitar a visualização)
    self.adj = adj           # Lusta de nós adjacentes
    self.visited = visited   # Diz se o nó já foi visitado ou não
    
  # Método para adcionar as conexões de um nó
  def setConnex(self, conex):
    self.adj = conex
  
  # Imprime as conexões do nó. Por padrão imprime os nomes. Para
  # imprimir os valores dos nós adjacentes, usar o parâmetro "value"
  def showConnex(self, mode = None):
    i = 0
    aux = []
    while i < len(self.adj):
      if mode == "value":
        aux.append(self.adj[i].value)
      else:
        aux.append(self.adj[i].name)
      i += 1
    if mode == "value":
        print("Conexões de " + str(self.value) + " : ", aux)
    else:
        print("Conexões de " + self.name + " : ", aux)

# Função que retorna True se os nós u e v forem adjacentes, 
# ou False caso contrário 
def isAdjacent(u, v):
  i = 0
  while i < len(u.adj):
    if u.adj[i].value == v.value:
      return True
    i += 1
  return False

# Busca em largura começando em 'u'
# NÃO FUNCIONA (loop infinito)
def BFS(u):
  print("Começo da função BFS")
  target = u # target é o nó atual
  tree = []
  print("\nPrimeiro loop: ")
  while True:
    target.visited = True
    i = 0
    while i < len(target.adj):
      print("\ni = ", i)
      print("target: ", target.name)
      print("vizinho do target: ", target.adj[i].name)
      print("Esse vizinho foi visitado? ", target.adj[i].visited)
      if target.adj[i].visited == False:
        target.adj[i].visited == True
        print("vizinho marcado como visitado: ", target.adj[i].visited)
        tree.append(target.adj[i].value)
        print("i = ", i)
        print("tree: ", tree)
      i += 1
    i = 0
    print("Saiu do primeiro loop.\nSegundo loop: ")
    tam = len(target.adj)
    while i < tam:
      print("\ni = ", i)
      print("target: ", target.name)
      print("vizinho do target: ", target.adj[i].name)
      print("Esse vizinho foi visitado? ", target.adj[i].visited)
      if target.adj[i].visited == False:
        target = target.adj[i]
      i += 1
    print("Fim do segundo loop.\n")
    print("Updated target: ", target.name)
  print("Tree: ", tree)
    
# Busca em profundidade começando em 'u'
# Até faz a busca (não tenho certeza se de forma correta),
# mas buga quando todos os vizinhos de um nó já foram visitados...
def DFS(u):
  print("\nComeço da iteração:")
  print("Nó atual: ", u.name)
  print("u.visited = ", u.visited)
  u.visited = True
  print("Agora, ", u.name, " foi marcado como visitado")
  i = 0
  while i < len(u.adj):
    print("Vizinho: ", u.adj[i].name)
    print("u.adj[",i,"].visited = ", u.adj[i].visited)
    if u.adj[i].visited == False:
      print("Valor no momento = ", u.adj[i].value)
      DFS(u.adj[i])
    i += 1
  print("Fim da função:")
  
# Criando alguns nós...
a = Node(1, "a")
b = Node(2, "b")
d = Node(4, "d")
e = Node(5, "e")
f = Node(6, "f")

a.setConnex([b,d,e])
b.setConnex([a,d,f])
d.setConnex([a,b,e])
e.setConnex([a,d])
f.setConnex([b])

'''
a.showConnex()
b.showConnex("value")
d.showConnex()
e.showConnex("value")
f.showConnex()
'''
BFS(a)