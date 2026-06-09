import copy

TARGET_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1), 'N': (0, 0)}

def find_position(state, value):
    for r in range(3):
        for c in range(3):
            if state[r][c] == value:
                return r, c
    return None

def apply_moves(initial_state, chromosome):
    """
    Aplica movimentos com EARLY STOP. 
    Retorna o estado final e a lista de movimentos reais aplicados (ignorando paredes).
    """
    state = copy.deepcopy(initial_state)
    empty_r, empty_c = find_position(state, 0)
    caminho_real = []
    
    for gene in chromosome:
        # Early Stop: se o tabuleiro já está ordenado, para de ler o cromossomo!
        if state == TARGET_STATE:
            break
            
        if gene == 'N':
            continue
            
        dr, dc = MOVES[gene]
        new_r, new_c = empty_r + dr, empty_c + dc
        
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            state[empty_r][empty_c], state[new_r][new_c] = state[new_r][new_c], state[empty_r][empty_c]
            empty_r, empty_c = new_r, new_c
            caminho_real.append(gene) # Só salva o movimento se ele de fato aconteceu
            
    return state, caminho_real

def calculate_fitness(state):
    manhattan = 0
    conflito_linear = 0
    
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:
                t_r, t_c = find_position(TARGET_STATE, val)
                manhattan += abs(r - t_r) + abs(c - t_c)
                
    for r in range(3):
        for c1 in range(3):
            for c2 in range(c1 + 1, 3):
                v1, v2 = state[r][c1], state[r][c2]
                if v1 != 0 and v2 != 0:
                    tr1, tc1 = find_position(TARGET_STATE, v1)
                    tr2, tc2 = find_position(TARGET_STATE, v2)
                    if tr1 == r and tr2 == r and tc1 > tc2:
                        conflito_linear += 2

    for c in range(3):
        for r1 in range(3):
            for r2 in range(r1 + 1, 3):
                v1, v2 = state[r1][c], state[r2][c]
                if v1 != 0 and v2 != 0:
                    tr1, tc1 = find_position(TARGET_STATE, v1)
                    tr2, tc2 = find_position(TARGET_STATE, v2)
                    if tc1 == c and tc2 == c and tr1 > tr2:
                        conflito_linear += 2
                        
    return manhattan + conflito_linear