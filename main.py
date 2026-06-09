import json
from src.genetico import run_genetic_algorithm
from src.utils import otimizar_sequencia, animar_solucao, mostrar_passo_a_passo

def carregar_configuracao(dificuldade):
    try:
        with open('testes/configuracoes.json', 'r') as f:
            config = json.load(f)
        return config.get(dificuldade)
    except Exception as e:
        print(f"Erro ao ler o JSON: {e}")
        return None

def main():
    print("=======================================")
    print(" AG: RESOLVEDOR DO 8-PUZZLE AVANÇADO")
    print("=======================================")
    
    dificuldade = "extremo" 
    estado_inicial = carregar_configuracao(dificuldade)
    
    if estado_inicial is None:
        print(f"\n[ERRO] A configuração '{dificuldade}' não foi encontrada!")
        return

    print(f"Iniciando busca para dificuldade: {dificuldade.upper()}\n")
    
    # 1. Roda o Algoritmo
    melhor_cromossomo, caminho_real = run_genetic_algorithm(estado_inicial)
    sequencia_super_limpa = otimizar_sequencia(caminho_real)
    
    # Aguarda o fechamento do gráfico para não sobrepor a animação
    input("\n[!] Feche o gráfico e pressione ENTER no terminal para iniciar a ANIMAÇÃO...")
    
    # 2. Exibe a Animação Limpando a Tela
    animar_solucao(estado_inicial, sequencia_super_limpa)
    
    # Trava a tela para que o usuário confirme antes de jogar todo o log na tela
    input("\n[!] Animação concluída! Pressione ENTER para gerar o RELATÓRIO FINAL ESTÁTICO...")
    
    # 3. Exibe os Cromossomos e o Histórico Estático
    print("\n\n" + "="*60)
    print(" RELATÓRIO FINAL DA SOLUÇÃO")
    print("="*60)
    
    print("\n[CROMOSSOMO ORIGINAL - GERADO PELO AG]:")
    print(melhor_cromossomo)
    
    print(f"\n[SEQUÊNCIA LIMPA - SOLUÇÃO FINAL COM {len(sequencia_super_limpa)} PASSOS]:")
    print(sequencia_super_limpa)
    
    print("\n\n--- INICIANDO HISTÓRICO DE ESTADOS ---")
    mostrar_passo_a_passo(estado_inicial, sequencia_super_limpa)
    
    print("\nFim da Simulação!")

if __name__ == "__main__":
    main()