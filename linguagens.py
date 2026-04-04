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

# Defina aqui as linguagens/ferramentas que você realmente usa
linguagens_trabalhadas = {
    "Python", "JavaScript", "C#", "C++", "HTML", "CSS", "TypeScript"
}

# Filtrar apenas essas linguagens
linguagens_filtradas = {
    lang: bytes for lang, bytes in linguagens.items() if lang in linguagens_trabalhadas
}

# Ordenar da mais usada para a menos usada
linguagens_ordenadas = dict(sorted(linguagens_filtradas.items(), key=lambda x: x[1], reverse=True))

# Gráfico mais baixo e só com as linguagens filtradas
if linguagens_ordenadas:
    plt.figure(figsize=(10,4))  # largura 10, altura 4
    plt.bar(linguagens_ordenadas.keys(), linguagens_ordenadas.values(), color="skyblue")
    plt.xlabel("Linguagens")
    plt.ylabel("Bytes de código")
    plt.title("Linguagens que utilizo nos meus repositórios")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("linguagens.png")

    print("Gráfico atualizado com as linguagens que você realmente usa.")
else:
    print("Nenhuma das linguagens selecionadas foi encontrada nos repositórios.")
