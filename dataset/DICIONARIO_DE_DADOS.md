# Dicionário de Dados: Breast_Cancer.csv

O dataset tem **4024 pacientes e 16 colunas**. Os dados vêm do programa **SEER** (Surveillance, Epidemiology, and End Results), o registro de câncer do governo dos EUA. Ele reúne mulheres com carcinoma ductal ou lobular infiltrante diagnosticadas entre 2006 e 2010.

Fonte: [Kaggle: Breast Cancer](https://www.kaggle.com/datasets/reihanenamdari/breast-cancer/data)

## Dados da paciente

| Coluna | O que é | Valores |
|---|---|---|
| **Age** | Idade no diagnóstico | 30 a 69 anos (média de 54) |
| **Race** | Raça | White (3413), Other (320), Black (291) |
| **Marital Status** | Estado civil | Married (2643), Single (615), Divorced (486), Widowed (235), Separated (45) |

## Estadiamento do tumor (sistema TNM)

O TNM descreve o quanto o câncer avançou. São três eixos: **T** é o tumor, **N** são os linfonodos e **M** é a metástase.

| Coluna | O que é | Valores |
|---|---|---|
| **T Stage** | Tamanho e extensão do tumor primário | T1 (≤ 2 cm), T2 (2–5 cm), T3 (> 5 cm), T4 (invadiu a pele ou a parede torácica) |
| **N Stage** | Quantos linfonodos regionais foram atingidos | N1 (1–3), N2 (4–9), N3 (≥ 10 ou em regiões mais distantes) |
| **6th Stage** | Estágio geral pela 6ª edição do manual AJCC. É calculado combinando T e N | IIA, IIB, IIIA, IIIB, IIIC (quanto maior, mais grave) |
| **A Stage** | Estágio resumido do SEER | Regional (3932): espalhou só para perto. Distant (92): chegou a partes distantes do corpo |

## Características das células do tumor

| Coluna | O que é | Valores |
|---|---|---|
| **differentiate** | Quanto as células do tumor ainda se parecem com células normais | Well, Moderately, Poorly differentiated, Undifferentiated |
| **Grade** | A mesma informação em forma de número | 1 = Well, 2 = Moderately, 3 = Poorly, IV = Undifferentiated (anaplásico) |

Quanto menos diferenciado o tumor (ou seja, quanto maior o grau), mais agressivo ele costuma ser.

## Medidas

| Coluna | O que é | Valores |
|---|---|---|
| **Tumor Size** | Tamanho do tumor, em **milímetros** | 1 a 140 mm (média de 30,5) |
| **Regional Node Examined** | Quantos linfonodos regionais foram retirados e examinados | 1 a 61 (média de 14,4) |
| **Reginol Node Positive** | Quantos desses linfonodos tinham câncer. O nome tem um erro de digitação: deveria ser "Regional" | 1 a 46 (média de 4,2) |

## Hormônios

| Coluna | O que é | Valores |
|---|---|---|
| **Estrogen Status** | Se o tumor tem receptores de estrogênio (ER) | Positive (3755), Negative (269) |
| **Progesterone Status** | Se o tumor tem receptores de progesterona (PR) | Positive (3326), Negative (698) |

Tumores positivos para esses receptores costumam ter prognóstico melhor, porque respondem à hormonioterapia.

## Desfecho

| Coluna | O que é | Valores |
|---|---|---|
| **Survival Months** | Meses de acompanhamento desde o diagnóstico | 1 a 107 (média de 71,3) |
| **Status** | Situação da paciente no fim do acompanhamento. **É a variável alvo da classificação** | Alive (3408), Dead (616) |

## Pontos de atenção para o pré-processamento

1. **Espaços sobrando.** O nome da coluna `"T Stage "` termina com um espaço. Também há espaço dentro de valores: `"Single "` em Marital Status e `" anaplastic; Grade IV"` em Grade.
2. **Grade não é totalmente numérica.** Ela tem os valores `"1"`, `"2"`, `"3"` e `" anaplastic; Grade IV"`, então o pandas lê a coluna como texto.
3. **Colunas redundantes.** `Grade` e `differentiate` têm exatamente a mesma informação. `6th Stage` é derivada de `T Stage` e `N Stage`. Para treinar modelos, considere manter só uma de cada grupo.
4. **Classes desbalanceadas.** Só cerca de 15% das pacientes estão como "Dead". Use métricas como recall, F1 ou AUC em vez de só acurácia, e avalie fazer balanceamento das classes.
5. **Risco de vazamento de dados (data leakage).** Se o objetivo é prever `Status`, a coluna `Survival Months` está diretamente ligada à resposta: quem morreu tende a ter menos meses de acompanhamento. Usar essa coluna no modelo é "trapacear". O ideal é deixá-la de fora.
6. **Não há estágio I nem N0.** Todas as pacientes têm pelo menos 1 linfonodo positivo. Isso limita o tipo de paciente para o qual o modelo pode ser usado.
