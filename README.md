# Winlog Classifier

## 1. Descrição do Projeto

O **Winlog Classifier** é um programa desenvolvido em Python que realiza a **classificação automatizada de logs de aplicativos do Windows**. A ferramenta combina:

* **Regras pré-definidas** baseadas em Event ID (identificador de evento do Windows);
* **Modelos leves de Machine Learning** (implementados com `scikit-learn`).

O sistema identifica e alerta sobre logs com indícios de criticidade, além de gerar gráficos e relatórios de desempenho do classificador.

## 2. Objetivos

1. Automatizar a análise de logs de sistemas Windows.
2. Classificar logs de acordo com seu nível de criticidade.
3. Emitir alertas para logs críticos.
4. Fornecer métricas de avaliação (precisão, recall e F1-score).
5. Visualizar resultados por meio de gráficos.

## 3. Tecnologias Utilizadas

* **Python 3.6+**
* **scikit-learn**: criação e aplicação de modelos de ML;
* **pandas**, **numpy**: manipulação de dados;
* **matplotlib**: geração de gráficos.

Todas as dependências estão listadas em `requirements.txt`.

## 4. Estrutura de Diretórios

```
winlog-classifier/
├── app/
│   ├── classifier.py       # Script principal de classificação
│   ├── utils.py            # Funções auxiliares
│   └── data/
│       └── massive_logs_windows.csv  # Exemplo de logs de entrada
├── .gitignore
├── README.md              # Este arquivo
└── requirements.txt       # Dependências Python
```

## 5. Pré-requisitos

* Python 3.6 ou superior instalado.
* `pip` para instalação de pacotes.
* Acesso ao terminal (PowerShell, Bash, etc.).

## 6. Passo a Passo para Rodar o Projeto

1. **Clonar o repositório**:

   ```bash
   git clone https://github.com/murilosolino/winlog-classifier.git
   cd winlog-classifier
   ```

2. **Criar e ativar ambiente virtual (recomendado)**:

   ```bash
   python -m venv venv
   # No Windows (PowerShell):
   .\venv\Scripts\Activate.ps1

   # No macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Preparar os dados de logs**:

   * Por padrão, o arquivo de exemplo `massive_logs_windows.csv` já está em `app/data/`.
   * Para utilizar outros logs, copie seu arquivo `.csv` para esse diretório.

5. **Executar o classificador**:

   ```bash
   python app/classifier.py --input app/data/massive_logs_windows.csv --output results
   ```

   Onde:

   * `--input`: caminho para o arquivo de logs;
   * `--output`: diretório para salvar saídas (alertas, gráficos e relatório de métricas).

6. **Visualizar resultados**:

   * Alertas de criticidade serão exibidos no terminal.
   * Gráficos de status geral dos logs e relatório de performance estarão em `results/`.

7. **(Opcional) Ajustes do Modelo**:

   * Dentro de `app/classifier.py`, modifique parâmetros como `test_size` e `random_state` para experimentar diferentes divisões de treino/teste.

## 7. Métricas de Avaliação

Ao final da execução, um arquivo `report.txt` é gerado em `results/`, contendo:

* **Acurácia**
* **Precisão (Precision)**
* **Revocação (Recall)**
* **F1-score**

Essas métricas permitem avaliar o desempenho do classificador em diferentes cenários.

## 9. Autores e Contato

* **Cauã Pacheco de Souza**
* **Murilo Almeida Solino de Oliveira**
