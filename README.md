# Breast-Cancer-Analysis-and-Classification
Projeto educacional TT002 para classificar a **avaliação registrada pelo radiologista** em uma de seis categorias, usando dados tabulares da paciente e da mamografia. Um segundo modelo prevê o diagnóstico de câncer de mama em até um ano. Ambos usam as mesmas oito entradas.

## Dataset

Dados do **Breast Cancer Surveillance Consortium (BCSC)**, um consórcio de pesquisa dos EUA.

- **Página oficial:** https://www.bcsc-research.org/datasets/mammography_dataset
- **Documentação das colunas:** https://www.bcsc-research.org/datasets/mammography_dataset/dataset_documentation
- **Cópia pública no OpenML (licença CC0), de onde o `main.py` baixa os dados:** https://www.openml.org/search?type=data&id=43687
- **CSV usado neste projeto:** [dataset/breast_cancer_screening_bcsc.csv](https://github.com/arthurMalveste/Breast-Cancer-Analysis-and-Classification/blob/main/dataset/breast_cancer_screening_bcsc.csv)

- 39.998 mamografias de 36.714 mulheres de 60 a 89 anos, realizadas entre 2005 e 2008 (20.000 digitais e 19.998 em filme). Algumas mulheres aparecem em mais de um exame.
- Dados tabulares, sem imagens.
- **Alvo do modelo:** `Radiologists_Assessment`, em seis categorias. O menor grupo, altamente sugestivo de malignidade, tem apenas cinco exames.
- **Entradas:** idade, densidade mamária, tipo de mamografia, disponibilidade de imagens anteriores para comparação, histórico familiar de câncer de mama, terapia hormonal, mamografia prévia e histórico de biópsia.
- **IMC:** fica fora do modelo e do CSV processado devido aos 58% de ausentes.
- **Identificador da paciente:** usado exclusivamente para manter todos os exames de uma mesma paciente na mesma partição.
- **Desfecho binário:** a confirmação de câncer em até um ano é o alvo do segundo modelo. As oito entradas dos dois modelos são descritas acima.

O BCSC recomenda esses dados para ensino de análise de dados e métodos estatísticos, e pede que seja citado como fonte e que se reconheça o financiamento do NCI.

## Como usar

1. Com Python 3.11 ou superior, instale as dependências com `python -m pip install -r requirements.txt`. Os CSVs já estão no repositório. Se necessário, rode `python main.py` para baixar novamente o CSV bruto.
2. Rode [pre-processado.ipynb](notebooks/pre-processado.ipynb) para regenerar o CSV usado na exploração. Abra [analise.ipynb](notebooks/analise.ipynb) para os gráficos com legendas e interpretações. Execute esses dois notebooks a partir da pasta `notebooks/`.
3. Rode [treinamento.ipynb](notebooks/treinamento.ipynb) do início ao fim. Ele parte do CSV bruto, compara cinco algoritmos e uma linha de base, salva o pipeline selecionado e recarrega o arquivo para prever a classe de um exame fictício. O notebook também baixa o CSV automaticamente quando executado fora da cópia do repositório, como no Colab.
4. Rode [dois-focos.ipynb](notebooks/dois-focos.ipynb) para reproduzir o ajuste multicategórico e a avaliação binária. O notebook inclui recall por categoria, curva precisão–recall e matriz de confusão.
5. Use [os slides da Parte 2](apresentacao/Parte_2_Avaliacao_do_Radiologista.pptx) para apresentar o objetivo, a comparação e a demonstração do notebook.

No [Colab](https://colab.research.google.com/github/arthurMalveste/Breast-Cancer-Analysis-and-Classification/blob/avaliacao-radiologista/notebooks/treinamento.ipynb), para reproduzir a versão de referência, execute `%pip install scikit-learn==1.8.0` em uma célula antes do treino e reinicie a sessão se solicitado.

O [dicionário de dados](dataset/DICIONARIO_DE_DADOS.md) documenta as colunas. O [modelo treinado](modelos/avaliacao-radiologista.joblib) usa scikit-learn 1.8.0. O formato das entradas e o exemplo de carregamento estão na seção 5 do notebook de treinamento.

## Primeiro experimento multicategórico

A floresta aleatória obteve o melhor F1 macro médio na validação cruzada (**17,12%**). No teste, obteve **16,66% de F1 macro**, **20,72% de recall macro** e **36,26% de acurácia**. A linha de base que sempre prevê Negativo obteve **13,14% de F1 macro** e **65,09% de acurácia**.

A floresta identificou **2 dos 11** exames suspeitos e **0 de 1** na categoria altamente sugestiva. O resultado mostra que é possível executar e avaliar a classificação com os dados disponíveis. O desempenho obtido e a baixa quantidade de exames nas classes raras limitam a utilidade das previsões.

## Comparação dos dois focos

O [notebook dos dois focos](notebooks/dois-focos.ipynb) executa o ajuste da classificação das seis avaliações e treina o classificador de diagnóstico em até um ano. Os dois modelos usam os mesmos oito atributos disponíveis antes da avaliação radiológica final. O teste tem 8.000 exames de pacientes ausentes do treino. O IMC segue excluído pela alta proporção de ausências.

**Foco 1.** A floresta com pesos intermediários subiu de 17,12% para 20,65% de F1 macro na validação e de 16,66% para 20,16% no teste já consultado no experimento original. A leitura desse ganho é exploratória. A acurácia passou de 36,26% para 57,31%. O modelo ajustado acertou zero dos 28 exames provavelmente benignos, zero dos 11 suspeitos e zero do único altamente sugestivo. A floresta original acertou dois dos 11 suspeitos. O ganho médio concentrou-se nas classes mais frequentes. A raridade dificulta aprender e medir o desempenho nas classes menores. A base também carece das imagens e dos achados visuais usados na avaliação radiológica.

**Foco 2.** Entre cinco algoritmos, a regressão logística obteve a melhor precisão média (AP) na validação. No teste, a AP foi 1,34%, com prevalência de 0,75%, e a ROC AUC foi 0,598. O limiar escolhido pelo F1 dos positivos na validação identificou 7 dos 60 diagnósticos, deixou 53 sem sinalização e gerou 392 falsos positivos. Dos 399 alertas, 1,75% corresponderam a diagnósticos. O modelo binário responde diretamente à pergunta do trabalho, mas esse desempenho é insuficiente para justificar triagem clínica.

Os dois pipelines treinados estão em `modelos/avaliacao-ajustada.joblib` e `modelos/diagnostico-em-um-ano.joblib`. O segundo inclui o limiar selecionado no treino. A seção **Modelos treinados e previsão individual** recarrega os arquivos e demonstra a previsão para um exame.
