Com base em toda a nossa jornada, nos gráficos gerados e nos logs detalhados do terminal, aqui está a proposta completa para o seu **Relatório Final**.

Ele foi estruturado em formato acadêmico/técnico, detalhando cada engrenagem do seu código e traduzindo os comportamentos observados em conclusões sólidas. Você pode copiar, adaptar e utilizar este texto diretamente no seu trabalho.

---

# Relatório Técnico: Resolução do 8-Puzzle utilizando Algoritmos Genéticos

## 1. Introdução

O 8-Puzzle é um problema clássico de otimização combinatória e busca em espaço de estados, consistindo em um tabuleiro de matriz 3x3 contendo oito peças numeradas de 1 a 8 e um espaço vazio. O objetivo é, a partir de uma configuração inicial desordenada, alcançar um estado ordenado deslizando as peças ortogonalmente.
Este projeto implementou um **Algoritmo Genético (AG)** para encontrar a sequência de movimentos capaz de resolver o quebra-cabeça. Por se tratar de um método heurístico inspirado na evolução biológica, o desafio principal foi modelar os operadores genéticos para navegar eficientemente pelo espaço de busca sem ficar permanentemente preso em ótimos locais.

---

## 2. Abordagem e Metodologia do Algoritmo Genético

A modelagem do problema exigiu a tradução das regras do tabuleiro para uma linguagem genética compreensível pelo algoritmo. As seguintes metodologias foram adotadas:

### 2.1 Representação do Cromossomo (Codificação)

Em vez de representar o estado do tabuleiro no cromossomo, optou-se por codificar a **sequência de ações**.

* Cada indivíduo (cromossomo) é um vetor de caracteres de tamanho fixo, onde cada gene representa um movimento do espaço vazio: **'U'** (Up/Cima), **'D'** (Down/Baixo), **'L'** (Left/Esquerda) e **'R'** (Right/Direita).
* O tamanho do cromossomo foi definido entre 40 e 80 genes, garantindo espaço suficiente para a resolução de tabuleiros de alta complexidade.

### 2.2 Função de Avaliação (Fitness)

Como o objetivo do algoritmo é minimizar o erro, tratou-se de um problema de minimização. O fitness foi calculado baseando-se na **Distância de Manhattan**. Para cada peça no tabuleiro, calcula-se a distância horizontal e vertical até a sua posição alvo final utilizando a fórmula:

$d(p, q) = |x_1 - x_2| + |y_1 - y_2|$

A soma das distâncias de todas as peças resulta no valor de Fitness do indivíduo.

* **Critério de Penalidade:** Movimentos inválidos (ex: tentar mover o espaço vazio contra as bordas do tabuleiro) foram tratados ignorando o movimento (No-Op), mas gastando um gene do cromossomo, o que atua como uma penalidade natural de eficiência espacial.
* **Early Stop:** Se um indivíduo atinge o Fitness 0 (solução perfeita) durante a simulação de seus movimentos, o processo de avaliação é interrompido antecipadamente, economizando processamento computacional.

### 2.3 Operadores Genéticos

* **Seleção por Torneio:** Para a seleção dos pais, utilizou-se o método de Torneio (tamanho $k = 3$). Indivíduos são escolhidos aleatoriamente da população e o melhor entre eles vence. Isso garante a pressão evolutiva ao mesmo tempo que mantém a diversidade genética, evitando a convergência prematura comum na seleção por roleta.
* **Crossover:** Foi aplicado um cruzamento de ponto único ou duplo para recombinar as sequências de movimentos de dois pais, permitindo que blocos de movimentos bem-sucedidos fossem passados para a próxima geração.
* **Mutação:** Para evitar a estagnação em mínimos locais, implementou-se uma taxa de mutação (ex: **5%**). Genes aleatórios sofrem alteração para um novo movimento randômico, injetando novidade no ecossistema.
* **Elitismo:** Para garantir que soluções promissoras não fossem destruídas pela mutação ou cruzamento, os melhores indivíduos de cada geração (ex: os 5 melhores) foram copiados intactos para a próxima geração.

---

## 3. Pós-Processamento e Otimização

A natureza estocástica do AG frequentemente gera sequências de "sobrevivência" com ruído genético (movimentos redundantes que se anulam, como ir para a Esquerda e voltar para a Direita no gene seguinte).
Para contornar isso, foi desenvolvido um algoritmo de **limpeza de rota** pós-processamento. Este filtro lê o caminho bruto executado até o "Early Stop" e remove pares de movimentos diretamente opostos sequenciais, extraindo a lógica pura da solução e reduzindo drasticamente o número de passos finais exibidos ao usuário.

---

## 4. Testes Realizados

Os testes foram realizados em diferentes cenários de complexidade utilizando a seguinte configuração de hiperparâmetros básicos:

* **Tamanho da População:** 150 a 200 indivíduos.
* **Taxa de Mutação:** 0.05 (5%).
* **Elitismo:** 5 indivíduos.
* **Máximo de Gerações:** 500.

**Cenários Avaliados:**

**Dificuldade Fácil** (Entropia quase nula): O tabuleiro exigia apenas 1 movimento para ser resolvido (apenas a peça 8 estava deslocada). Devido à distância imediata, foi solucionado instantaneamente por amostragem aleatória na Geração 0, gerando um gráfico de ponto único no Matplotlib.

**Dificuldade Média** (Baixa entropia inicial): O tabuleiro exigia entre 3 e 4 movimentos para reordenar o quadrante inferior direito. A população inicial de 150 indivíduos encontrou a resposta ainda na Geração 0 por pura probabilidade matemática e sorte estatística.

**Dificuldade Difícil** (Entropia moderada): O tabuleiro exigia de 6 a 8 movimentos, apresentando peças desalinhadas verticalmente (como o 4 e o 7). O algoritmo tendeu ao comportamento Random Walk, gerando sequências brutas longas na Geração 0 que precisaram obrigatoriamente do filtro de redundâncias para serem limpas.

**Dificuldade Extrema** (Alta entropia inicial): O tabuleiro exigia no mínimo 15 movimentos perfeitamente coordenados, com quase nenhuma peça perto do estado meta. Foi o único cenário complexo o suficiente para desafiar a sorte inicial, forçando a evolução real (cruzamento e mutação) por 18 a 25 gerações para quebrar os platôs de mínimos locais.
---

## 5. Análise de Resultados

O acompanhamento das métricas de evolução via interface gráfica (Matplotlib) e logs de terminal forneceu os seguintes insights comportamentais:

* **O Fenômeno da Solução Randômica (Geração 0):** Nos testes de dificuldade "Média", o algoritmo frequentemente encontrou a solução na Geração 0. Como a população inicial de 150 cromossomos gera centenas de milhares de combinações de movimentos de forma pseudo-aleatória, distâncias curtas (menores que 8 passos) mostraram-se estatisticamente propensas a serem resolvidas por "acidente". Isso validou a eficácia do mecanismo de *Early Stop*.
* **Comportamento em Degraus e Mínimos Locais:** No cenário "Extremo", o gráfico de convergência demonstrou um comportamento clássico de degraus na linha do "Melhor Fitness". O algoritmo ficava retido em valores de fitness como 6 ou 2 por diversas gerações consecutivas. Esse platô ocorre porque o tabuleiro atinge um estado onde a maioria das peças está correta, mas consertar as últimas peças exige "desmanchar" partes corretas temporariamente (piorando o fitness no curto prazo). A saída desses mínimos locais foi garantida apenas pela ação conjunta da Mutação e da manutenção de uma População grande.
* **Queda Constante do Fitness Médio:** A linha tracejada que representa o fitness médio da população apresentou um declínio constante e suave na maioria dos testes, comprovando matematicamente o funcionamento do filtro de Seleção Natural: os indivíduos inaptos foram mortos sistematicamente e o pool genético tornou-se mais focado a cada rodada.
* **Eficiência do Filtro Pós-Processamento:** No teste final do cenário Extremo, o AG levou 24 gerações para achar a resposta. A sequência bruta possuía mais de 20 movimentos. O filtro otimizador limpou a rota, resultando em precisos 15 passos contínuos e sem redundâncias, demonstrando que o algoritmo consegue encontrar o caminho, mas precisa de um refinamento determinístico no fim.

---

## 6. Conclusões

Com base na arquitetura desenvolvida e nos dados coletados, é possível concluir que:

1. **Eficácia Comprovada:** O Algoritmo Genético demonstrou ser **altamente eficaz** na resolução do 8-Puzzle, conseguindo ordenar o caos inicial e encontrar estados de vitória consistentes, respeitando rigorosamente as regras de transição do tabuleiro.
2. **Eficácia vs. Eficiência Matemática:** Embora encontre a solução, o AG não é eficiente na garantia da otimalidade (*menor caminho matemático*) de forma nativa. Por ser uma busca "suja", ele descobre uma solução de contorno, diferente de algoritmos tradicionais de busca em grafos (como o A-Estrela ou a Busca em Largura), que calculam rotas mínimas perfeitas, mas podem gastar muito mais memória.
3. **Poder Heurístico:** A maior força da abordagem genética demonstrada neste projeto foi a sua resiliência. O AG é agnóstico à complexidade do estado em si; ele apenas segue a "bússola" da Distância de Manhattan. Combinado com o filtro de otimização de rota, o sistema provou ser um modelo robusto, adaptável e uma excelente aplicação prática da computação bioinspirada para problemas de ordenação espacial.