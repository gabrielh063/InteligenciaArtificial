import os
import time
import heapq
from collections import deque

MOVES = {
    'C': (-1, 0),  # cima
    'B': (1, 0),   # baixo
    'E': (0, -1),  # esquerda
    'D': (0, 1),   # direita
}

# ---------- Funções utilitárias ----------
def ler_mapa(nome_arquivo):
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(pasta_atual, nome_arquivo)

    grid = []
    start = goal = None
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for r, line in enumerate(l.strip('\n') for l in f):
            grid.append(list(line))
            for c, ch in enumerate(line):
                if ch == 'S':
                    start = (r, c)
                elif ch == 'G':
                    goal = (r, c)
    if start is None or goal is None:
        raise ValueError("Mapa inválido: faltam S ou G.")
    return grid, start, goal

def vizinhos(grid, r, c):
    R, C = len(grid), len(grid[0])
    for move, (dr, dc) in MOVES.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#':
            yield move, (nr, nc)

def marcar_caminho(grid, start, moves):
    r, c = start
    for mv in moves:
        dr, dc = MOVES[mv]
        r, c = r + dr, c + dc
        if grid[r][c] not in ('S', 'G'):
            grid[r][c] = '*'
    return grid

def imprimir_grid(grid):
    for linha in grid:
        print(''.join(linha))

# ---------- BFS (referência) ----------
def bfs(grid, start, goal):
    fila = deque([start])
    visitado = {start}
    pai = {start: (None, None)}
    expandidos = 0
    max_fronteira = 1

    while fila:
        atual = fila.popleft()
        expandidos += 1
        if atual == goal:
            caminho_moves = []
            cur = atual
            while pai[cur][0] is not None:
                caminho_moves.append(pai[cur][1])
                cur = pai[cur][0]
            caminho_moves.reverse()
            return caminho_moves, expandidos, max_fronteira

        r, c = atual
        for move, nxt in vizinhos(grid, r, c):
            if nxt not in visitado:
                visitado.add(nxt)
                pai[nxt] = (atual, move)
                fila.append(nxt)
                max_fronteira = max(max_fronteira, len(fila))

    return None, expandidos, max_fronteira

# ---------- A* ----------
def heuristica(a, b):
    # Distância de Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    fila = []
    heapq.heappush(fila, (0, start))  # (f, estado)
    g_score = {start: 0}
    pai = {start: (None, None)}
    expandidos = 0
    max_fronteira = 1

    while fila:
        _, atual = heapq.heappop(fila)
        expandidos += 1

        if atual == goal:
            caminho_moves = []
            cur = atual
            while pai[cur][0] is not None:
                caminho_moves.append(pai[cur][1])
                cur = pai[cur][0]
            caminho_moves.reverse()
            return caminho_moves, expandidos, max_fronteira

        r, c = atual
        for move, nxt in vizinhos(grid, r, c):
            novo_g = g_score[atual] + 1
            if nxt not in g_score or novo_g < g_score[nxt]:
                g_score[nxt] = novo_g
                f = novo_g + heuristica(nxt, goal)
                pai[nxt] = (atual, move)
                heapq.heappush(fila, (f, nxt))
                max_fronteira = max(max_fronteira, len(fila))

    return None, expandidos, max_fronteira

# ---------- Main ----------
if __name__ == "__main__":
    mapa = input("Nome do mapa (ex: mapa2.txt): ").strip()
    grid, start, goal = ler_mapa(mapa)

    print("\n--- BFS ---")
    t0 = time.time()
    caminho_bfs, exp_bfs, max_bfs = bfs([row[:] for row in grid], start, goal)
    t1 = time.time()
    if caminho_bfs is None:
        print("Sem solução.")
    else:
        print("Passos mínimos:", len(caminho_bfs))
        print("Caminho (moves):", ''.join(caminho_bfs))
    print("Nós expandidos:", exp_bfs)
    print("Máx. fronteira:", max_bfs)
    print("Tempo: %.6fs" % (t1 - t0))

    print("\n--- A* ---")
    t0 = time.time()
    caminho_astar, exp_astar, max_astar = astar([row[:] for row in grid], start, goal)
    t1 = time.time()
    if caminho_astar is None:
        print("Sem solução.")
    else:
        print("Passos mínimos:", len(caminho_astar))
        print("Caminho (moves):", ''.join(caminho_astar))
        grid_marcado = marcar_caminho(grid, start, caminho_astar)
        imprimir_grid(grid_marcado)
    print("Nós expandidos:", exp_astar)
    print("Máx. fronteira:", max_astar)
    print("Tempo: %.6fs" % (t1 - t0))
