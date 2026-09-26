const fs = require("fs");
const path = require("path");
const readline = require("readline");
const connDb = require("../API/configs/conexaoDb");
const SenatranMarcaModelo = require("../API/models/SenatranMarcaModelo");

const FILE_PATH = path.resolve(__dirname, "../../../ai/data/raw/senatran/extracted/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Julho_2026.TXT");

async function importSenatranData() {
  console.log("Iniciando importação dos dados do SENATRAN...");
  await connDb.sync({ alter: true }); 

  const fileStream = fs.createReadStream(FILE_PATH, { encoding: "utf-8" });
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

  let batch = [];
  const BATCH_SIZE = 2000;
  let lineCount = 0;
  let isHeader = true;

  for await (const line of rl) {
    if (isHeader) {
      isHeader = false;
      continue;
    }

    const parts = line.split(";");
    if (parts.length < 5) continue;

    const [uf, municipio, marcaModelo, anoStr, qtdStr] = parts;
    if (!marcaModelo || !marcaModelo.includes("/")) continue;

    const [marca, ...restoModelo] = marcaModelo.split("/");
    const modelo = restoModelo.join("/").trim();

    batch.push({
      uf: uf.trim(),
      municipio: municipio.trim(),
      marca: marca.trim().toUpperCase(),
      modelo: modelo.toUpperCase(),
      anoFabricacao: parseInt(anoStr, 10) || 0,
      quantidade: Math.round(parseFloat(qtdStr) || 1)
    });

    lineCount++;

    if (batch.length >= BATCH_SIZE) {
      await SenatranMarcaModelo.bulkCreate(batch);
      console.log(`Processadas ${lineCount} linhas...`);
      batch = [];
    }
  }

  if (batch.length > 0) {
    await SenatranMarcaModelo.bulkCreate(batch);
  }

  console.log(`Importação concluída! Total de ${lineCount} registros inseridos.`);
  process.exit(0);
}

importSenatranData().catch((err) => {
  console.error("Erro no seed SENATRAN:", err);
  process.exit(1);
});
