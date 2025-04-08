# Classificação automatizada de Logs de Aplicativos Windows utilizando regras baseadas em eventID e modelos de machine learning leves

O objetivo desse projeto é fazer a classificação automática de logs de aplicativos windows, utilizando o eventID como parâmetro para fazer a identificação do tipo do log através de modelos leves de machine learning, nesse caso, utilizando a biblioteca do sklearn para fazer a análise de LOGS e gerar tanto avisos para LOGS com indícies de criticalidade quanto gráficos que mostrem de maneira geral os STATUS dos LOGS. O objetivo principal desse programa é facilitar na identificação de LOGS e o seu nível de criticalidade, poupando horas de trabalho manual e recursos.

**Principais Funcionalidades**

- Fazer análise com IA para determinar a criticalidades dos logs
- Emitir os Logs que possuam alertas críticos
- Fazer um gráfico que mostre os STATUS dos logs de maneira geral
- Emitir um relatório de classificação da IA (precisão, recall, f1 score)
- Ajudar funcionários a poupar tempo e recursos utilizando de uma análise automática ao invés de uma análise manual.

```
**Instruções de Instalação**

- Baixar todas as bibliotecas necessárias (Dependencies, consulte o arquivo "requirements.txt")
- Cole o código do "simuladorDeLogs" em uma interface que permita execução de código (jupyter notebook, VSCode, etc)
- Rode o código do "simuladorDeLogs" para gerar o arquivo "massive_logs_windows" (Ou use o "massive_logs_windows" que já está presente na pasta)
- Cole o código do "main.py" na mesma pasta que estiver o "massive_logs_windows" em uma interface que permita execução de código (jupyter notebook, VSCode, etc)
- Rode o código utilizando o terminal da interface
- (Opicional) Caso trablhando com uma amostra de dados maior, é possível modificar os parâmetros de leitura da IA alterando o "test_size" e o "random_state".
```

**Autores:**

- *Cauã Pacheco de Souza*
- *Murilo Almeida Solino de Oliveira*