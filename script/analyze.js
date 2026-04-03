const fs = require("fs");

const username = "MathiasFilypeDev";

async function safeFetch(url) {
  const res = await fetch(url, {
    headers: {
      "User-Agent": "readme-bot"
    }
  });

  if (!res.ok) {
    console.log(`⚠️ Erro ao buscar: ${url}`);
    return null;
  }

  return res.json();
}

async function getLanguages() {
  const repos = await safeFetch(`https://api.github.com/users/${username}/repos?per_page=100`);

  if (!repos) throw new Error("Erro ao buscar repositórios");

  const langStats = {};

  for (const repo of repos) {
    if (repo.fork || !repo.languages_url) continue;

    const langs = await safeFetch(repo.languages_url);

    if (!langs) continue;

    for (const [lang, bytes] of Object.entries(langs)) {
      langStats[lang] = (langStats[lang] || 0) + bytes;
    }
  }

  return langStats;
}

function generateMarkdown(langStats) {
  const total = Object.values(langStats).reduce((a, b) => a + b, 0);

  if (total === 0) {
    return "⚠️ Nenhuma linguagem encontrada.";
  }

  let md = "## 📊 Linguagens mais usadas\n\n";
  md += "| Linguagem | Uso (%) | Nível |\n";
  md += "|----------|---------|--------|\n";

  const sorted = Object.entries(langStats).sort((a, b) => b[1] - a[1]);

  for (const [lang, bytes] of sorted.slice(0, 10)) {
    const percent = ((bytes / total) * 100).toFixed(2);
    const bar = "█".repeat(Math.round(percent / 5));
    md += `| ${lang} | ${percent}% | ${bar} |\n`;
  }

  return md;
}

(async () => {
  try {
    console.log("🚀 Iniciando análise...");

    const stats = await getLanguages();
    const markdown = generateMarkdown(stats);

    if (!fs.existsSync("README.md")) {
      throw new Error("README.md não encontrado");
    }

    const readme = fs.readFileSync("README.md", "utf-8");

    if (!readme.includes("<!-- LANG-STATS-START -->")) {
      throw new Error("Marcador LANG-STATS não encontrado no README");
    }

    const newReadme = readme.replace(
      /<!-- LANG-STATS-START -->([\s\S]*?)<!-- LANG-STATS-END -->/,
      `<!-- LANG-STATS-START -->\n${markdown}\n<!-- LANG-STATS-END -->`
    );

    fs.writeFileSync("README.md", newReadme);

    console.log("✅ README atualizado com sucesso!");
  } catch (err) {
    console.error("❌ ERRO REAL:", err.message);
    process.exit(1);
  }
})();
