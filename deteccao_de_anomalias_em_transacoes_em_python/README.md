# Detecção de Anomalias em Transações de Cartão de Crédito

Este projeto consiste no desenvolvimento e avaliação de modelos de Machine Learning para detecção de transações fraudulentas utilizando um dataset altamente desbalanceado.

## 📌 Visão Geral do Projeto

O objetivo principal é identificar transações fraudulentas minimizando os falsos negativos (alto Recall), sem comprometer excessivamente a precisão de alarmes falsos.

## 📊 Etapas do Projeto

1. **Exploração e Análise do Dataset (EDA)**:
   - Base de dados com **284.807 transações** e 31 colunas.
   - Altíssimo desbalanceamento: **99,83% de transações normais** e apenas **0,17% de fraudes**.
   - Identificação de 1.081 linhas duplicadas. Optou-se por mantê-las para evitar a perda de dados importantes da classe minoritária (fraude).
   - Análise de comportamento das variáveis `Amount` (Valores) e `Time` (Tempo).

2. **Preparação dos Dados**:
   - Engenharia de Features: Aplicação de transformação logarítmica na variável `Amount` (`Log_Amount` via `np.log1p`) para normalização dos dados.
   - Divisão estratificada entre treino (80%) e teste (20%).

3. **Modelagem Baseline**:
   - Treinamento de uma **Regressão Logística** como baseline, atingindo **99,92% de acurácia**, porém com apenas **65,31% de Recall** (deixando passar 34 das 98 fraudes do conjunto de teste).

4. **Tratamento do Desbalanceamento**:
   - Teste de técnicas de balanceamento de dados utilizando o pipeline de Regressão Logística:
     - **Undersampling (Subamostragem)**: Recall de 91,84%, mas baixíssima Precisão (4,98%).
     - **Oversampling (SMOTE)**: Recall de 89,80% e Precisão de 13,29%.

5. **Classificadores Avançados (Ensembles)**:
   - **Random Forest (Balanced)**: Excelente precisão (96,10%) com recall de 75,51% (F1-score de 84,57%).
   - **XGBoost (Weighted)**: Ótimo equilíbrio geral com **87,10% de Precisão** e **82,65% de Recall** (F1-score de 84,82%).

6. **Ajuste de Limiar (Threshold Tuning)**:
   - Ajustando o limiar de decisão do XGBoost para **0.3**, o modelo atinge um excelente equilíbrio de **83,84% de Precisão** e **84,69% de Recall**.

7. **Explicabilidade do Modelo**:
   - Uso da importância nativa de variáveis do XGBoost e da biblioteca **SHAP** para interpretar quais variáveis (como `V14`, `V4` e `V12`) mais influenciam nas previsões de fraude.

## 🛠️ Tecnologias Utilizadas

- Python 3
- Pandas e NumPy
- Scikit-Learn
- XGBoost
- Imbalanced-Learn (SMOTE / RandomUnderSampler)
- Matplotlib e Seaborn
- SHAP (SHapley Additive exPlanations)
