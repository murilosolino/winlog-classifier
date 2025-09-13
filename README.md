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
* **pandas**: manipulação de dados;
* **matplotlib**, **seaborn**: geração de gráficos.
* **nltk**: processamento de linguagem natural

Todas as dependências estão listadas em `requirements.txt`.

## 4. Estrutura de Diretórios

```
winlog-classifier/
├── app/
│   ├── src/                    # Código-fonte
│   │   ├── classifiers/        # Implementação de classificadores
│   │   │   └── rule_based.py   # Classificador baseado em regras
│   │   ├── data/              # Dados e carregamento
│   │   │   ├── data_loader.py  # Carregamento de dados
│   │   │   ├── logAppsWindows.txt  # Regras e mapeamentos de Event IDs
│   │   │   └── massive_logs_windows.txt  # Exemplo de logs
│   │   ├── helper/            # Scripts auxiliares
│   │   │   └── simuladorDeLogs.py  # Gerador de logs de teste
│   │   ├── ml/                # Modelos de Machine Learning
│   │   │   └── ml_model.py    # Definição e treino de modelo ML
│   │   ├── pre_processor/     # Processamento de dados
│   │   │   └── preprocessor.py  # Limpeza e transformação de dados
│   │   └── ui/                # Interface do usuário
│   │       ├── main.py        # Aplicação principal com Streamlit
│   │       └── no_ia.py       # Fluxo sem uso de IA
│   └── __init__.py            # Arquivo de inicialização do pacote
├── .gitignore
└── README.md                  # Este arquivo
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

2. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Preparar os dados de logs**:
   * Por padrão, o arquivo de exemplo `massive_logs_windows.txt` já está disponível em `app/src/data/`
   * Para gerar um novo arquivo de logs, execute:
   ```bash
   python -m app.src.helper.simuladorDeLogs
   ```

4. **Executar o projeto**:
   * Para iniciar a aplicação web com Streamlit:
   ```bash
   cd app
   streamlit run src/ui/main.py
   ```
   
   * Para executar a versão sem IA:
   ```bash
   streamlit run src/ui/no_ia.py
   ```

5. **Acessar a interface**:
   * A aplicação abrirá automaticamente no seu navegador padrão
   * Caso não abra, acesse: `http://localhost:8501`

6. **Usar a aplicação**:
   * Carregue um arquivo de logs ou use o conjunto de dados padrão
   * Visualize gráficos e métricas em tempo real
   * Faça download dos resultados em formato CSV

7. **(Opcional) Customização**:
   * Ajuste parâmetros do modelo em `src/ml/ml_model.py`
   * Modifique regras de classificação em `src/classifiers/rule_based.py`
   * Personalize a interface em `src/ui/main.py`


## 📸 Demonstrações

### Resultados via gráficos
![Resultado do Gráfico](screenshots/grafico.png)

### Resultados via console
![Analise de resultados no console](screenshots/resultado.png)

* Essas métricas permitem avaliar o desempenho do classificador em diferentes cenários.

## 🧠 Disciplinas Envolvidas

- Linguagens Formais e Autômatos



## 👥 Equipe

* **Cauã Pacheco de Souza**
* **Murilo Almeida Solino de Oliveira**

## 🏫 Informações Acadêmicas

- Universidade: **Universidade Braz Cubas**
- Curso: **Ciência da Computação**
- Semestre: 7º
- Período: Noite
- Professora orientadora: **Dra. Andréa Ono Sakai**
- Evento: **Mostra de Tecnologia 1º Semestre de 2025**
- Local: Laboratório 12
- Datas: 05 e 06 de junho de 2025

## 📄 Licença

MIT License — sinta-se à vontade para utilizar, estudar e adaptar este projeto.
