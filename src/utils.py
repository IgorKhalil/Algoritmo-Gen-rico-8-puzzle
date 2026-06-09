import os
import time
import copy
from src.puzzle import MOVES, find_position

def otimizar_sequencia(caminho):
    """Remove movimentos opostos em sequência."""
    opostos = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
    limpo = []
    
    for mov in caminho:
        if limpo and limpo[-1] == opostos.get(mov):
            limpo.pop() 
        else:
            limpo.append(mov)
            
    return limpo

def limpar_tela():
    """Limpa o terminal independentemente do sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tabuleiro(estado, passo=None, movimento=None):
    """Imprime o tabuleiro formatado."""
    print("=" * 20)
    if passo is not None:
        print(f" Passo: {passo:2} | Movimento: {movimento}")
    else:
        print(" Estado Inicial")
    print("=" * 20)
    
    for r in range(3):
        linha = "|"
        for c in range(3):
            val = estado[r][c]
            if val == 0:
                linha += "   |"
            else:
                linha += f" {val:1} |"
        print("-" * 13)
        print(linha)
    print("-" * 13)
    print()

def animar_solucao(estado_inicial, sequencia_limpa):
    """Apaga a tela e anima passo a passo a solução no terminal."""
    estado_atual = copy.deepcopy(estado_inicial)
    empty_r, empty_c = find_position(estado_atual, 0)
    
    limpar_tela()
    imprimir_tabuleiro(estado_atual)
    time.sleep(1.0)
    
    for i, gene in enumerate(sequencia_limpa, 1):
        dr, dc = MOVES[gene]
        new_r, new_c = empty_r + dr, empty_c + dc
        
        estado_atual[empty_r][empty_c], estado_atual[new_r][new_c] = estado_atual[new_r][new_c], estado_atual[empty_r][empty_c]
        empty_r, empty_c = new_r, new_c
            
        limpar_tela()
        imprimir_tabuleiro(estado_atual, passo=i, movimento=gene)
        time.sleep(0.4)

def mostrar_passo_a_passo(estado_inicial, sequencia_limpa):
    """Imprime o histórico de estados sequencialmente para o relatório."""
    estado_atual = copy.deepcopy(estado_inicial)
    empty_r, empty_c = find_position(estado_atual, 0)
    
    imprimir_tabuleiro(estado_atual)
    
    for i, gene in enumerate(sequencia_limpa, 1):
        dr, dc = MOVES[gene]
        new_r, new_c = empty_r + dr, empty_c + dc
        
        estado_atual[empty_r][empty_c], estado_atual[new_r][new_c] = estado_atual[new_r][new_c], estado_atual[empty_r][empty_c]
        empty_r, empty_c = new_r, new_c
            
        imprimir_tabuleiro(estado_atual, passo=i, movimento=gene)