# Lista das linguagens que você realmente trabalhou
linguagens_trabalhadas = {"Python", "JavaScript", "HTML", "CSS", "Typescript", "React"}

# Filtrar apenas essas
linguagens_filtradas = {lang: bytes for lang, bytes in linguagens.items() if lang in linguagens_trabalhadas}

plt.figure(figsize=(6,3))
plt.bar(linguagens_filtradas.keys(), linguagens_filtradas.values(), color="skyblue")
plt.xlabel("Linguagens")
plt.ylabel("Bytes de código")
plt.title("Minhas linguagens mais usadas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("linguagens.png")
