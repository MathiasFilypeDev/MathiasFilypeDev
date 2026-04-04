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

# Converter para percentuais e ordenar
total = sum(linguagens_filtradas.values())
linguagens_percentuais = {lang: (val/total*100 if total > 0 else 0) for lang, val in linguagens_filtradas.items()}
linguagens_ordenadas = dict(sorted(linguagens_percentuais.items(), key=lambda x: x[1], reverse=True))

langs = list(linguagens_ordenadas.keys())
values = list(linguagens_ordenadas.values())
colors = plt.cm.Set3(range(len(values)))  # paleta colorida

# Gráfico de barras com estilo
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(langs, [0]*len(values), color=colors, edgecolor="black", linewidth=1.2)

ax.set_ylabel("Uso (%)")
ax.set_title("Tecnologias que utilizo nos meus repositórios")

def animate(i):
    for idx, bar in enumerate(bars):
        progress = min(i/50, 1)
        bar.set_height(values[idx] * progress)
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+1,
                f"{values[idx]:.1f}%", ha='center', va='bottom', fontsize=10, fontweight="bold")

ani = animation.FuncAnimation(fig, animate, frames=60, interval=80, repeat=False)
ani.save("linguagens.gif", writer="pillow", fps=30)

# Também gerar gráfico de pizza
fig2, ax2 = plt.subplots(figsize=(6,6))
ax2.pie(values, labels=langs, autopct='%1.1f%%', colors=colors, startangle=140)
ax2.set_title("Distribuição das Tecnologias")
plt.savefig("linguagens_pizza.png")

print("GIF animado gerado em linguagens.gif e gráfico de pizza em linguagens_pizza.png")
