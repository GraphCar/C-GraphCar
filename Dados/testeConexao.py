# Arquivo para teste de conexão com o Slack, caso haja algum erro na api rode esse código para saber o que está acontecendo.
# Caso o problema seja na url altere ela aqui na variável "chatEscolhido" e faça o mesmo nos outros arquivos de captura de dados.

import requests
import json

mensagemTeste = {"text": f""" 
🚨ALERTA🚨 TESTE DE CONEXÃO 🚨ALERTA🚨 
"""} 
chatEscolhido = "https://hooks.slack.com/services/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"
postMsg = requests.post(chatEscolhido, data=json.dumps(mensagemTeste))

if postMsg.status_code == 200:
    print("Mensagem enviada com sucesso: código",postMsg.status_code)
    print("Abra o Slack e verifique se a mensagem foi postada.")
else:
    print("Código de erro: ",postMsg.status_code)
    print("Motivo: ",postMsg.reason)
    print("Conteúdo: ",postMsg.content)