# Projeto_CloudWalk
Meu projeto para o processo seletivo

Separei em 2 atos:

# First Act
Nesse ato é onde aplica-se a primeira parte do projeto, onde analisa-se 2 arquivos CSVs (checkout_1 e checkout_2) e conclusões são retiradas por meio de scripts.
Os gráficos são exibidos no script detect_anomalies.py com as devidas anomalias presentes, sendo consideradas por meio de uma função presente em utils.py.
O script query.py exibe um gráfico separado de comparação entre Today vs. Average Last Month exibindo as anomalias desta comparação.

# Second Act
Prosseguindo, temos o segundo ato, onde o objetivo é resolver um problema. Usa-se 2 CSVs (transaction_1 e transaction_2) e cria-se um sistema de monitoramento com alertas.
O script app.py é responsável pela criação do banco de dados e do endpoint para exibir o gráfico, o envio de alertas para possíveis anomalias e cria logs para melhor planejamento e controle.
Já no script dashboard.py, é onde o gráfico é gerado e exibido no endpoint e também é feito uma atualização contínua de um determinado período.
