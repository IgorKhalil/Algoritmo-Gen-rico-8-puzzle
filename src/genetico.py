import random
import matplotlib.pyplot as plt
from src.puzzle import apply_moves, calculate_fitness, MOVES

POPULATION_SIZE = 150
CHROMOSOME_LENGTH = 40
MUTATION_RATE = 0.05
TOURNAMENT_SIZE = 3
ELITISM_COUNT = 5
GENERATIONS = 500

def crossover_two_point(parent1, parent2):
    pt1 = random.randint(1, CHROMOSOME_LENGTH - 3)
    pt2 = random.randint(pt1 + 1, CHROMOSOME_LENGTH - 1)
    
    child1 = parent1[:pt1] + parent2[pt1:pt2] + parent1[pt2:]
    child2 = parent2[:pt1] + parent1[pt1:pt2] + parent2[pt2:]
    return child1, child2

def mutate(chromosome):
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            chromosome[i] = random.choice(list(MOVES.keys()))
    return chromosome

def tournament_selection(population, fitnesses):
    best_idx = -1
    best_fit = float('inf')
    
    for _ in range(TOURNAMENT_SIZE):
        idx = random.randint(0, POPULATION_SIZE - 1)
        if fitnesses[idx] < best_fit:
            best_fit = fitnesses[idx]
            best_idx = idx
    return population[best_idx]

def plotar_evolucao(historico_melhor, historico_media):
    """Gera e exibe o gráfico de evolução do fitness."""
    plt.figure(figsize=(10, 5))
    plt.plot(historico_melhor, label='Melhor Fitness', color='blue', linewidth=2)
    plt.plot(historico_media, label='Fitness Médio da População', color='orange', linestyle='--')
    plt.title('Evolução do Algoritmo Genético - 8-Puzzle')
    plt.xlabel('Gerações')
    plt.ylabel('Distância de Manhattan + Conflito')
    plt.legend()
    plt.grid(True)
    plt.show()

def run_genetic_algorithm(initial_state):
    population = [[random.choice(list(MOVES.keys())) for _ in range(CHROMOSOME_LENGTH)] 
                  for _ in range(POPULATION_SIZE)]
    
    melhor_global = None
    melhor_fitness_global = float('inf')
    caminho_vencedor = []
    
    # Listas para o gráfico
    historico_melhor = []
    historico_media = []
    
    for generation in range(GENERATIONS):
        fitnesses = []
        
        for chromo in population:
            final_state, caminho_real = apply_moves(initial_state, chromo)
            fit = calculate_fitness(final_state)
            fitnesses.append(fit)
            
            if fit < melhor_fitness_global:
                melhor_fitness_global = fit
                melhor_global = chromo.copy()
                caminho_vencedor = caminho_real
            
            if fit == 0:
                print(f"\n[!] Solução perfeita encontrada na geração {generation}!")
                historico_melhor.append(0)
                historico_media.append(sum(fitnesses)/len(fitnesses))
                plotar_evolucao(historico_melhor, historico_media)
                return melhor_global, caminho_vencedor
                
        # Atualiza métricas para o gráfico
        media_gen = sum(fitnesses) / POPULATION_SIZE
        historico_melhor.append(melhor_fitness_global)
        historico_media.append(media_gen)

        sorted_indices = sorted(range(POPULATION_SIZE), key=lambda k: fitnesses[k])
        new_population = [population[i] for i in sorted_indices[:ELITISM_COUNT]]
        
        while len(new_population) < POPULATION_SIZE:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            c1, c2 = crossover_two_point(p1, p2)
            
            new_population.append(mutate(c1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(c2))
                
        population = new_population
        
        if generation % 20 == 0:
            print(f"Geração {generation:4d} | Melhor Fitness: {melhor_fitness_global} | Média: {media_gen:.2f}")
            
    print(f"\n[!] Limite atingido. Melhor solução parcial: Fitness {melhor_fitness_global}")
    plotar_evolucao(historico_melhor, historico_media)
    return melhor_global, caminho_vencedor