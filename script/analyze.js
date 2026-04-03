const fs = require("fs");

console.log("🔥 Script rodando");

if (!fs.existsSync("README.md")) {
  console.log("❌ README não existe");
  process.exit(1);
}

console.log("✅ README existe");
