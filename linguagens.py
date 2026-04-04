import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

# Linguagens que você realmente trabalha
linguagens_trabalhadas = {"Python", "JavaScript", "TypeScript", "Java", "HTML", "CSS"}

linguagens_filtradas = {lang: bytes for lang, bytes in linguagens.items() if lang in linguagens_trabalhadas}

# Adicionar React e PostgreSQL como categorias extras
linguagens_filtradas["React"] = linguagens_filtradas.get("JavaScript", 0) + linguagens_filtradas.get("TypeScript", 0)
linguagens_filtradas["PostgreSQL"] = 0  # ajuste manual se quiser somar SQL

# Ordenar
linguagens_ordenadas = dict(sorted(linguagens_filtradas.items(), key=lambda x: x[1], reverse=True))

fig, ax = plt.subplots(figsize=(10,4))
langs = list(linguagens_ordenadas.keys())
values = list(linguagens_ordenadas.values())
bars = ax.bar(langs, [0]*len(values), color="skyblue")

ax.set_xlabel("Linguagens e Ferramentas")
ax.set_ylabel("Bytes de código")
ax.set_title("Tecnologias que utilizo nos meus repositórios")
plt.xticks(rotation=45)

def animate(i):
    for bar, val in zip(bars, values):
        bar.set_height(val * i / 100)

ani = animation.FuncAnimation(fig, animate, frames=100, interval=30, repeat=False)
ani.save("linguagens.gif", writer="pillow", fps=30)

print("GIF animado gerado em linguagens.gif")
