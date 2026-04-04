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

# Ordenar e converter para percentuais
total = sum(linguagens_filtradas.values())
linguagens_percentuais = {lang: (val/total*100 if total > 0 else 0) for lang, val in linguagens_filtradas.items()}
linguagens_ordenadas = dict(sorted(linguagens_percentuais.items(), key=lambda x: x[1], reverse=True))

# Preparar gráfico
fig, ax = plt.subplots(figsize=(10,4))
langs = list(linguagens_ordenadas.keys())
values = list(linguagens_ordenadas.values())
bars = ax.bar(langs, [0]*len(values), color="skyblue")

ax.set_xlabel("Linguagens e Ferramentas")
ax.set_ylabel("Uso (%)")
ax.set_title("Tecnologias que utilizo nos meus repositórios")
plt.xticks(rotation=45)

# Função de animação: cresce barra por barra
def animate(i):
    for idx, bar in enumerate(bars):
        if i >= idx*10:  # cada barra começa em um frame diferente
            progress = min((i-idx*10)/10, 1)
            bar.set_height(values[idx] * progress)

ani = animation.FuncAnimation(fig, animate, frames=len(values)*20, interval=50, repeat=False)
ani.save("linguagens.gif", writer="pillow", fps=30)

print("GIF animado otimizado gerado em linguagens.gif")
