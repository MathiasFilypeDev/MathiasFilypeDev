import requests
from collections import Counter
import os

usuario = "Antonio"
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}

url = f"https://api.github.com/users/{usuario}/repos"
repos = requests.get(url, headers=headers).json()

linguagens = Counter()

for repo in repos:
    lang_url = repo["languages_url"]
    langs = requests.get(lang_url, headers=headers).json()
    linguagens.update(langs)

# Descobrir a linguagem mais usada
if linguagens:
    linguagem_top = max(linguagens, key=linguagens.get)
    print(f"A linguagem mais usada nos seus repositórios é: {linguagem_top}")
else:
    print("Não foi possível encontrar linguagens nos repositórios.")
