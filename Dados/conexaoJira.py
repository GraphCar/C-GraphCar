import requests
from requests.auth import HTTPBasicAuth
import json
from jira import JIRA


# TOKEN PARA AUTENTICACAO
jira_token = "seu token aqui"

# CREDENCIAIS PARA AUTENTICAÇÃO
url = "https://graphcar.atlassian.net/rest/api/3/issue"
server_name = "https://graphcar.atlassian.net"
email = "seu email aqui"


jira_connection = JIRA(
  basic_auth=(email, jira_token),
  server=server_name
)


def chamado(mensagem, descricao):
  issue_dict = {
    'project': {'key': 'GRAP'},
    'summary': mensagem,
    'description': descricao,
    'issuetype': {'id': '10002'},
  }

  new_issue = jira_connection.create_issue(fields=issue_dict)
  print(new_issue)

chamado()