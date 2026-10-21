# Breast-Cancer-Analysis-and-Classification
Análise e classificação de diagnósticos de câncer de mama. A ideia é usar a biblioteca Pandas do Python para fazer todo o pré processamento dos dados e análises e depois usar modelos de aprendizado de máquina para identificar quais pacientes receberão um diagnóstico de câncer. É um repositório para fins educacionais.

## Dataset

Dados do **Breast Cancer Surveillance Consortium (BCSC)**, um consórcio de pesquisa dos EUA.

- **Página oficial:** https://www.bcsc-research.org/datasets/mammography_dataset
- **Documentação das colunas:** https://www.bcsc-research.org/datasets/mammography_dataset/dataset_documentation
- **Cópia pública no OpenML (licença CC0), de onde o `main.py` baixa os dados:** https://www.openml.org/search?type=data&id=43687
- **CSV usado neste projeto:** [dataset/breast_cancer_screening_bcsc.csv](https://github.com/arthurMalveste/Breast-Cancer-Analysis-and-Classification/blob/main/dataset/breast_cancer_screening_bcsc.csv)

- 39.998 mamografias de 36.714 mulheres de 60 a 89 anos, realizadas entre 2005 e 2008 (20.000 digitais e 19.998 em filme). Algumas mulheres aparecem em mais de um exame.
- Dados tabulares, sem imagens.
- **Alvo:** `Is_Binary_Indicator_Of_Cancer_Diagnosis`, que indica se houve diagnóstico de câncer em até 1 ano após a mamografia.
- **Features:** idade, avaliação do radiologista (BI-RADS), densidade da mama, histórico familiar, uso de terapia hormonal, mamografia anterior, biópsia anterior, tipo de mamografia (filme ou digital) e IMC.

Pontos de atenção:
- **Classes muito desbalanceadas:** só 259 exames (0,65%) tiveram diagnóstico de câncer. Acurácia sozinha engana, então é preciso olhar recall, precisão e AUC.
- **`Cancer_Type` vaza a resposta** e deve ser removida antes de treinar os modelos.
- O IMC está ausente em 58% das linhas (por isso é removido no pré-processamento), e outras colunas têm poucos valores ausentes.
- A coluna `Binary_Indicator` indica se a mulher já tinha feito alguma mamografia antes.

O BCSC recomenda esses dados para ensino de análise de dados e métodos estatísticos, e pede que seja citado como fonte e que se reconheça o financiamento do NCI.

## Como usar

1. Crie o ambiente virtual e instale as dependências: `pandas` (e `ipykernel` para rodar os notebooks).
2. Rode `python main.py` para baixar o dataset. Ele será salvo em `dataset/breast_cancer_screening_bcsc.csv`.
3. Abra `notebooks/teste.ipynb` para ver a visão geral dos dados.
4. Rode `notebooks/pre-processado.ipynb` para gerar `dataset/breast_cancer_screening_bcsc_processed.csv`, a versão numérica e sem valores ausentes usada nos modelos.

O significado de cada coluna está em [dataset/DICIONARIO_DE_DADOS.md](dataset/DICIONARIO_DE_DADOS.md).
