# Dicionário de Dados: breast_cancer_screening_bcsc.csv

O dataset tem **39.998 mamografias de 36.714 mulheres e 13 colunas**. Os dados vêm do **Breast Cancer Surveillance Consortium (BCSC)**, um consórcio de pesquisa dos EUA. É uma amostra aleatória de 20.000 mamografias digitais e 19.998 em filme, feitas em mulheres de 60 a 89 anos entre janeiro de 2005 e dezembro de 2008. Algumas mulheres aparecem em mais de um exame. Não há imagens, só dados clínicos.

Fontes: [OpenML (ID 43687)](https://www.openml.org/d/43687) e [BCSC](https://www.bcsc-research.org/datasets/mammography_dataset)

Os valores ausentes aparecem vazios no CSV (no arquivo original eram a palavra "Missing").

## Identificação

| Coluna | O que é | Valores |
|---|---|---|
| **Patients_Study_ID** | Identificador da mulher. Não é uma feature, serve só para saber quais exames são da mesma pessoa | 36.714 valores distintos |

## Dados da paciente

| Coluna | O que é | Valores |
|---|---|---|
| **Age_At_The_Time_Of_Mammography** | Idade na data da mamografia | 60 a 89 anos (média de 69,6) |
| **Body_Mass_Index** | Índice de massa corporal (IMC) | 15 a 71,7 (média de 26,9). **58% ausentes** |
| **Family_History_Of_Breast_Cancer** | Se uma parente de primeiro grau (mãe, irmã ou filha) teve câncer de mama | No (33.027), Yes (6.743), ausente (228) |
| **Current_Use_Of_Hormone_Therapy** | Se usava terapia hormonal na data do exame | No (33.977), Yes (4.249), ausente (1.772) |
| **History_Of_Breast_Biopsy** | Se já fez biópsia de mama antes | No (28.733), Yes (10.450), ausente (815) |

## Características da mama e do exame

| Coluna | O que é | Valores |
|---|---|---|
| **Patients_BI_RADS_Breast_Density** | Densidade da mama pela escala BI-RADS. Mamas mais densas escondem tumores no exame e também têm risco maior | Almost entirely fatty (5.429), Scattered fibroglandular densities (21.246), Heterogeneously dense (12.028), Extremely dense (1.295) |
| **Is_Film_Or_Digital_Mammogram** | Tipo de mamografia | True = digital (20.000), False = filme (19.998) |
| **Binary_Indicator** | Se a mulher já tinha feito alguma mamografia antes. O nome da coluna no arquivo original é genérico | Yes (39.124), No (296), ausente (578) |
| **Comparison_Mammogram_From_Mammography** | Se havia uma mamografia anterior disponível para o radiologista comparar | Yes (34.016), No (1.302), ausente (4.680) |

## Avaliação do radiologista

| Coluna | O que é | Valores |
|---|---|---|
| **Radiologists_Assessment** | Resultado do exame na escala BI-RADS, em ordem do menos para o mais preocupante | Negative (26.031), Benign findings (10.717), Needs additional imaging (3.049), Probably benign (139), Suspicious abnormality (57), Highly suggestive of malignancy (5) |

Essa é a feature mais forte do dataset. A taxa de câncer vai de 0,1% nos exames "Negative" e "Benign findings" a 6,5% em "Needs additional imaging", 42% em "Suspicious abnormality" e 80% em "Highly suggestive of malignancy". Os valores têm ordem natural, então podem ser codificados como números.

## Desfecho

| Coluna | O que é | Valores |
|---|---|---|
| **Is_Binary_Indicator_Of_Cancer_Diagnosis** | Se houve diagnóstico de câncer de mama em até 1 ano após a mamografia. **É a variável alvo da classificação** | False (39.739), True (259) |
| **Cancer_Type** | Tipo do câncer diagnosticado | No cancer diagnosis (39.739), Invasive cancer (203), ductal carcinoma in situ (56) |

## Pontos de atenção para o pré-processamento

1. **Vazamento de dados (data leakage).** `Cancer_Type` é só o alvo com mais detalhes: vale "No cancer diagnosis" exatamente quando o alvo é False. Deve ser removida antes de treinar qualquer modelo.
2. **Classes muito desbalanceadas.** Só 259 exames (0,65%) tiveram câncer. Um modelo que sempre responde "sem câncer" acerta 99,35%, então acurácia sozinha engana. Use recall, precisão, F1 ou AUC e avalie técnicas de balanceamento.
3. **Valores ausentes.** O IMC está ausente em 58% das linhas, então é preciso decidir entre imputar ou descartar a coluna. As outras colunas têm entre 0,6% e 11,7% de ausentes.
4. **Quase tudo é categórico.** Só `Age_At_The_Time_Of_Mammography` e `Body_Mass_Index` são numéricas. As demais precisam de codificação (ordinal para BI-RADS e densidade, one-hot ou 0/1 para Yes/No).
5. **Mesma mulher em vários exames.** Há 39.998 exames de 36.714 mulheres. Ao separar treino e teste, mantenha todos os exames de uma mulher do mesmo lado (por exemplo, com `GroupKFold` usando `Patients_Study_ID`). Se não, o modelo pode "ver" a mesma paciente no treino e no teste.
6. **Avaliação do radiologista como feature.** Ela prevê bem o câncer, mas já é uma conclusão feita por uma pessoa olhando a imagem. Compare os modelos com e sem essa coluna: sem ela, o modelo só usa fatores de risco da paciente.
