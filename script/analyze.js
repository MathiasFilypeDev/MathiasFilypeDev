const fetch = require("node-fetch");
const fs = require("fs");

const username = process.env.GITHUB_USERNAME;

async function getLanguages() {
  const reposRes = await fetch(`https://api.github.com/users/${username}/repos?per_page=100`);
  const repos = await reposRes.json();

  const langStats = {};

  for (const repo of repos) {
    if (repo.fork) continue;

    const langRes = await fetch(repo.languages_url);
    const langs = await langRes.json();

    for (const [lang, bytes] of Object.entries(langs)) {
      langStats[lang] = (langStats[lang] || 0) + bytes;
    }
  }

  return langStats;
}

function generateMarkdown(langStats) {
  const total = Object.values(langStats).reduce((a, b) => a + b, 0);

  let md = "## 📊 Linguagens mais usadas (Atualizado automaticamente)\n\n";
  md += "| Linguagem | Uso (%) | Barra |\n";
  md += "|----------|---------|-------|\n";

  const sorted = Object.entries(langStats).sort((a, b) => b[1] - a[1]);

  for (const [lang, bytes] of sorted.slice(0, 10)) {
    const percent = ((bytes / total) * 100).toFixed(2);
    const bar = "█".repeat(Math.round(percent / 5));
    md += `| ${lang} | ${percent}% | ${bar} |\n`;
  }

  return md;
}

(async () => {
  const stats = await getLanguages();
  const markdown = generateMarkdown(stats);

  const readme = fs.readFileSync("README.md", "utf-8");

  const newReadme = readme.replace(
    /<!-- LANG-STATS-START -->([\s\S]*?)<!-- LANG-STATS-END -->/,
    `<!-- LANG-STATS-START -->\n${markdown}\n<!-- LANG-STATS-END -->`
  );

  fs.writeFileSync("README.md", newReadme);
})();
