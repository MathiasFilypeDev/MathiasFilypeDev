const fs = require("fs");
const { ChartJSNodeCanvas } = require("chartjs-node-canvas");
const fetch = require("node-fetch");

const width = 800;
const height = 600;
const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

async function main() {
  const usuario = "Antonio";
  const token = process.env.GITHUB_TOKEN;
  const headers = token ? { Authorization: `token ${token}` } : {};

  const reposResponse = await fetch(`https://api.github.com/users/${usuario}/repos`, { headers });
  const repos = await reposResponse.json();

  const linguagens = {};

  for (const repo of repos) {
    const langResponse = await fetch(repo.languages_url, { headers });
    const langs = await langResponse.json();
    for (const [lang, bytes] of Object.entries(langs)) {
      linguagens[lang] = (linguagens[lang] || 0) + bytes;
    }
  }

  const configuration = {
    type: "bar",
    data: {
      labels: Object.keys(linguagens),
      datasets: [{
        label: "Bytes de código",
        data: Object.values(linguagens),
        backgroundColor: "rgba(54, 162, 235, 0.6)"
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Linguagens mais usadas no GitHub"
        }
      }
    }
  };

  const image = await chartJSNodeCanvas.renderToBuffer(configuration);
  fs.writeFileSync("linguagens.png", image);
}

main().catch(err => {
  console.error("Erro ao gerar gráfico:", err);
  process.exit(1);
});
