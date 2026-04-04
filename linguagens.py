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

# Tecnologias que você realmente usa
linguagens_trabalhadas = {"Python", "JavaScript", "TypeScript", "Java", "HTML", "CSS"}
linguagens_filtradas = {lang: bytes for lang, bytes in linguagens.items() if lang in linguagens_trabalhadas}

# Adicionar React e PostgreSQL
linguagens_filtradas["React"] = linguagens_filtradas.get("JavaScript", 0) + linguagens_filtradas.get("TypeScript", 0)
linguagens_filtradas["PostgreSQL"] = 0  # ajuste manual se quiser somar SQL

# Ordenar pela quantidade
linguagens_ordenadas = dict(sorted(linguagens_filtradas.items(), key=lambda x: x[0], reverse=False))

langs = list(linguagens_ordenadas.keys())
values = list(linguagens_ordenadas.values())
colors = plt.cm.Paired(range(len(values)))

# Gráfico de barras verticais
fig, ax = plt.subplots(figsize=(10,6))
bars = ax.bar(langs, [0]*len(values), color=colors)

ax.set_ylabel("Bytes de código")
ax.set_title("Tecnologias que utilizo nos meus repositórios")
plt.xticks(rotation=0)  # labels bem alinhados embaixo das barras

# Função de animação: cada barra cresce em sequência
def animate(i):
    for idx, bar in enumerate(bars):
        if i >= idx*20:  # cada barra começa em um momento diferente
            progress = min((i-idx*20)/20, 1)
            bar.set_height(values[idx] * progress)
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+1000,
                    f"{values[idx]:,}", ha='center', va='bottom', fontsize=9, fontweight="bold")

ani = animation.FuncAnimation(fig, animate, frames=len(values)*30, interval=50, repeat=False)
ani.save("linguagens.gif", writer="pillow", fps=30)

print("GIF animado gerado em linguagens.gif")
