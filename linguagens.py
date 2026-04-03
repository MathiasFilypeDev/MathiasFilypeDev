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

# Lista das linguagens que você realmente trabalhou
linguagens_trabalhadas = {"Python", "Reactjs", "JavaScript", "Typescript", "HTML", "CSS"}

# Filtrar apenas essas
linguagens_filtradas = {lang: bytes for lang, bytes in linguagens.items() if lang in linguagens_trabalhadas}

# Gráfico mais baixo
plt.figure(figsize=(6,3))
plt.bar(linguagens_filtradas.keys(), linguagens_filtradas.values(), color="skyblue")
plt.xlabel("Linguagens")
plt.ylabel("Bytes de código")
plt.title("Minhas linguagens mais usadas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("linguagens.png")
