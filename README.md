#  DeepRacer — Reward e comportamento
### Igor Paço Sguissardi de Oliveira - Grupo 2 - Subgrupo 02

## Proposta
Essa ponderada teve como objetivo principal explorar o impacto da função de recompensa no comportamento de um agente de Reinforcement Learning dentro do ambiente simulado do DeepRacer for Cloud. Como integrante do subgrupo 2, apresento a seguir duas tentativas estruturadas de modelagem da reward function, documentando as justificativas das escolhas realizadas e comparando como cada variação influenciou a estratégia de tomada de decisão e o desempenho do carrinho na pista.

Os vídeos podem ser baixado no caminho ```assets\```.

## Primeira versão do código 

### Escolhas de Parâmentros 

A primeira versão propõe uma abordagem baseada em limites discretos para orientar o comportamento do agente. A lógica de centralização divide a pista em três faixas fixas, atribuindo recompensas progressivamente menores à medida que o veículo se afasta do centro. Além disso, o código introduz penalidades rígidas para movimentos bruscos de direção (ângulos superiores a 15 graus) e restringe o incentivo de alta velocidade a momentos em que o carro está em linha reta (ângulo inferior a 5 graus). Também é incluído um bônus de eficiência baseado na relação entre o progresso alcançado e a quantidade de passos tomados.  

A **peculiaridade** desta versão é a sua estrutura baseada em thresholds (limites rígidos) através de blocos condicionais (if/elif/else).

O **objetivo** primário desta modelagem foi estabelecer um comportamento conservador e previsível. Forçando o agente a aprender regras estritas de segurança, espera-se que ele priorize a permanência exata no centro da pista, acelere apenas em situações de baixo risco (retas) e complete o percurso no menor número de passos possível.

### Justificativa das Escolhas Realizadas

A justificativa central para a estruturação dessa primeira versão reside na tentativa de incentivar uma conclusão rápida do circuito. Ao definir divisões rígidas na pista, recompensando o agente dependendo de se ele está a 10%, 25% ou 50% de distância do centro, a intenção foi criar um mapa de recompensas direto, onde o objetivo primário é forçar o modelo a priorizar a distância percorrida e a velocidade em trechos seguros.

Para garantir que essa busca por velocidade não resultasse em um comportamento destrutivo, optou-se por aplicar punições rígidas que desencorajassem saídas da pista ou curvas exageradas. Há penalização severa caso nem todas as rodas estejam na pista (reduzindo a recompensa ao valor mínimo de 1e-3) e a redução de 20% na pontuação caso o ângulo de direção ultrapasse 15 graus funcionam como barreiras estritas de segurança. Com essas regras, o agente é condicionado a evitar movimentos bruscos que poderiam desestabilizar o veículo.

Por fim, a lógica por trás do incentivo de aceleração consolida essa estratégia: o bônus que multiplica a recompensa em 1.5 vezes exige que o carro esteja a uma velocidade maior que 2.0 e com o volante praticamente reto (ângulo menor que 5 graus). Aliado a isso, a adição de um bônus de eficiência baseado na proporção de progresso por passos tomados (`progress / steps`) direciona o agente a buscar trajetórias mais curtas e rápidas, equilibrando a agressividade na conclusão do trajeto com as travas conservadoras de direção.

<video controls width="55%">
  <source src="https://github.com/igorPassoCS/DeepRacer_Ponderada/blob/master/assets/ponderada-cc10-s02-01-training.mp4" type="video/mp4">
</video>
<br>
<em>Evidência das fases iniciais do treinamento na primeira versão, onde o carrinho ainda dá uns tipos de saltos e não anda de forma fluida.</em>

<video controls width="55%">
  <source src="https://github.com/igorPassoCS/DeepRacer_Ponderada/blob/master/assets/ponderada-cc10-s02-01-evaluating.mp4" type="video/mp4">
</video>
<br>
<em>*Evidência da fase final de avaliação da primeira versão.*</em>


![Vídeo de Avaliação](assets/ponderada-cc10-s02-01-evaluating.mp4)


## Segunda versão do código

### Escolhas de Parâmentros 

A segunda versão substitui a lógica de limites discretos por uma modelagem matemática contínua. O cálculo da distância em relação ao centro e a penalização para o ângulo de direção utilizam funções exponenciais negativas para criar uma curva de recompensa suave. A recompensa de velocidade não está mais isolada em uma regra condicional, mas sim diretamente multiplicada pelos fatores de centralização e suavidade do volante.

A **peculiaridade** central desta abordagem é a ausência de blocos condicionais para a tomada de decisão em movimento; o carro experimenta as mudanças de recompensa de maneira gradativa e fluida, sem "degraus" ou quebras abruptas na pontuação. 

O **objetivo** desta versão é induzir uma condução muito mais orgânica e estável. Ao utilizar funções contínuas, busca-se evitar solavancos e o comportamento de "ziguezague" constante, permitindo que o agente perceba nuances da pista e otimize a velocidade dinamicamente de acordo com a suavidade com que realiza as curvas.

### Justificativa das Escolhas Realizadas

A justificativa fundamental para a adoção de uma superfície de recompensa contínua baseia-se na própria natureza matemática dos algoritmos de aprendizado por reforço que operam por gradiente, como o Proximal Policy Optimization (PPO), amplamente utilizado no DeepRacer. Esses modelos tendem a apresentar uma performance superior e uma convergência mais rápida quando expostos a cenários onde pequenas mudanças no estado do veículo refletem em pequenas mudanças proporcionais na recompensa. Essa continuidade facilita a otimização da política de condução, orientando o algoritmo de forma clara sem os "saltos" abruptos ou zonas cegas geradas por condicionais estritos.

Nesse sentido, a escolha por funções matemáticas exponenciais negativas para calcular a centralização e a penalização dos movimentos de direção foi feita exatamente para mitigar a instabilidade no comportamento do agente. Ao invés de punições engessadas, as curvas suaves das exponenciais ensinam o modelo a não realizar correções bruscas no volante. O agente passa a perceber de forma fluida que ajustes mínimos rendem pontuações quase intactas, enquanto manobras exageradas degradam a recompensa gradativamente, eliminando solavancos e o indesejado efeito de ziguezague na pista sem confundir o processo de otimização.

Além disso, a estrutura matemática escolhida justifica-se pela capacidade de interligar os objetivos do carrinho de forma orgânica. Ao multiplicar os fatores de centralização, suavidade de direção e o fator de velocidade no cálculo final, o carrinho compreende que a aceleração só é devidamente recompensada se executada com o volante alinhado e o carro bem posicionado. Dessa forma, a arquitetura garante que a velocidade seja aprendida como uma consequência direta da precisão e estabilidade contínuas.

<figure>
    <video src="assets/ponderada-cc10-s02-02-training.mp4"controls width="55%"></video>
    <figcaption>Evidência das fases iniciais do treinamento da segunda versão, exploração inicial. </figcaption>
</figure>

<figure>
    <video src="assets/ponderada-cc10-s02-02-evaluating.mp4"controls width="55%"></video>
    <figcaption>Evidência da fase final de avaliação da segunda versão, completando a pista de forma fluída e suave. </figcaption>
</figure>

## Análise do Comportamento Observado e Comparações

Durante as fases de treinamento e validação no simulador, as duas abordagens de função de recompensa resultaram em comportamentos e estratégias de navegação fundamentalmente distintos. 

### Quadro Comparativo

| Característica | Modelo 1 (Recompensa Discreta) | Modelo 2 (Recompensa Contínua) |
| :--- | :--- | :--- |
| **Episódios para Conclusão**| ~40 episódios | ~60 episódios |
| **Estabilidade do Veículo** | Instável (movimentação mecânica e não natural) | Fluida, suave e orgânica |
| **Comportamento Inicial** | Falhas rápidas com efeito visual de "teletransporte" | Exploração lenta, segura e consistente |

### Análise da Primeira Versão: Instabilidade e Efeito de "Saltos"
Nas iterações iniciais da primeira versão, observou-se que o veículo parecia saltar ou se teletransportar pela pista em vez de seguir um traçado contínuo. Esse fenômeno não é um erro do simulador, mas um reflexo da lógica de recompensas implementada:

1. **Resets Constantes por Ação Agressiva:** Como a função bonifica fortemente a relação de progresso rápido, o agente tenta maximizar a aceleração logo no início, antes mesmo de dominar a dinâmica das curvas. Isso faz com que ele saia da pista em milissegundos, acionando o *reset* automático do simulador sucessivas vezes, o que gera o efeito visual de saltos rápidos.
2. **Caos no Gradiente devido aos "Degraus":** A estrutura de pontuação dividida em marcos rígidos envia sinais de gradiente muito instáveis durante a otimização. O modelo, ao perceber que a pontuação cai drasticamente de uma zona para outra, tenta compensar com ações extremas de direção, resultando em acidentes e na movimentação errática observada. Ainda assim, por forçar a velocidade, conseguiu fechar o circuito mais rápido em termos de episódios de treinamento (~40).

### Análise da Segunda Versão: Condução Fluida e Cautelosa
Em forte contraste, a segunda versão apresentou uma navegação muito mais orgânica. A utilização de penalidades exponenciais contínuas eliminou a necessidade de viradas bruscas de volante, ensinando o agente a realizar micro-correções para se manter alinhado.

Apesar da alta estabilidade, a dependência matemática da suavidade direcional tornou o comportamento do agente notavelmente mais conservador. Por penalizar gradualmente qualquer desvio não otimizado, o veículo evitou riscos, resultando em uma fase de exploração inicial muito mais lenta. Essa "cautela" algorítmica explica por que o Modelo 2 demandou um número maior de episódios (~60) para mapear o circuito com segurança e concluí-lo integralmente.

## Reflexão sobre possíveis melhorias

* **Desenvolvimento de uma Função Híbrida (*Reward Shaping*):** Unir os pontos fortes das duas tentativas. Pode-se manter as funções matemáticas contínuas (exponenciais) da Segunda Versão para garantir estabilidade orgânica, introduzindo multiplicadores de velocidade mais agressivos inspirados na Primeira Versão, para incentivar a redução do tempo de volta de forma controlada.
* **Otimização do *Action Space*:** Ajustar os limites físicos e a granularidade das ações disponíveis para o agente nas configurações do simulador. Reduzir o ângulo máximo de direção (*steering angle*) pode mitigar mecanicamente as viradas extremas e a instabilidade observada na Primeira Versão.
* **Implementação de *Racing Line* via *Waypoints*:** Substituir a recompensa focada unicamente no eixo central da pista por uma lógica de trajetória ideal (*optimal racing line*). Utilizar o parâmetro de `waypoints` para recompensar o agente ao tangenciar e "cortar" as curvas adequadamente, maximizando a velocidade real ao invés de forçá-lo a fazer curvas abertas apenas para seguir o centro.
* **Ajuste Fino de Hiperparâmetros (*Hyperparameter Tuning*):** Testar variações nos parâmetros intrínsecos do algoritmo PPO. Ajustar a taxa de aprendizado (*learning rate*), o tamanho do lote (*batch size*) ou a entropia (*entropy*) poderia acelerar consideravelmente o processo de exploração e convergência do Modelo 2, diminuindo a quantidade de episódios necessários para mapear a pista.
* **Penalização Preditiva de Saída de Pista:** Em vez de atribuir a punição máxima ($1e-3$) apenas quando o veículo já cometeu o erro fatal (`all_wheels_on_track == False`), pode-se criar uma penalidade que avalie o risco iminente combinando alta velocidade, direção apontada para a borda e proximidade da margem. Isso ensinaria o agente a corrigir a trajetória antes que o simulador force o *reset*.