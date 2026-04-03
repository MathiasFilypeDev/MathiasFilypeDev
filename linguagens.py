import requests
import matplotlib.pyplot as plt
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

# Se houver linguagens, gera gráfico com todas
if linguagens:
    plt.figure(figsize=(10,4))  # largura 10, altura 4 (mais baixo)
    plt.bar(linguagens.keys(), linguagens.values(), color="skyblue")
    plt.xlabel("Linguagens")
    plt.ylabel("Bytes de código")
    plt.title("Linguagens mais usadas nos meus repositórios")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("linguagens.png")

    print("Gráfico atualizado com todas as linguagens mais usadas.")
else:
    print("Não foi possível encontrar linguagens nos repositórios.")
