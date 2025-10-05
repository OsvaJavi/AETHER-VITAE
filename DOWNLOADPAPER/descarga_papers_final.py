import os
import re
import time
import glob
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# === CONFIGURACIÓN ===
usuario = "jgalazka"
repositorio = "SB_publications"
archivo = "SB_publication_PMC.csv"

output_folder = r"C:\Users\ovcor\OneDrive\Desktop\x\papers"
os.makedirs(output_folder, exist_ok=True)

log_path = os.path.join(output_folder, "log_descarga.txt")

def log(mensaje):
    print(mensaje)
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} - {mensaje}\n")

log(f"⬇️ Descargando CSV desde https://raw.githubusercontent.com/{usuario}/{repositorio}/main/{archivo}...")

df = pd.read_csv(f"https://raw.githubusercontent.com/{usuario}/{repositorio}/main/{archivo}")
df.to_csv(os.path.join(output_folder, archivo), index=False)
log(f"✅ CSV guardado en {output_folder}")

columnas_con_links = [col for col in df.columns if df[col].astype(str).str.contains("http", case=False, na=False).any()]
if not columnas_con_links:
    log("⚠️ No se encontraron enlaces en el CSV.")
    exit()

columnas_titulo = [col for col in df.columns if "title" in col.lower()]
titulo_col = columnas_titulo[0] if columnas_titulo else None

urls = []
titulos = []
for index, row in df.iterrows():
    for col in columnas_con_links:
        valor = str(row[col])
        encontrados = re.findall(r'(https?://[^\s,]+)', valor)
        for url in encontrados:
            urls.append(url)
            titulos.append(str(row[titulo_col]) if titulo_col else f"Paper_{index+1}")

log(f"🌐 Se encontraron {len(urls)} enlaces.")

# === Configurar Selenium con Edge para descarga automática ===
edge_options = Options()
edge_options.add_argument("--headless")
prefs = {
    "download.default_directory": output_folder,
    "plugins.always_open_pdf_externally": True,
}
edge_options.add_experimental_option("prefs", prefs)

driver_path = r"C:\Users\ovcor\OneDrive\Desktop\x\edgedriver_win64\msedgedriver.exe"  # Cambia por tu ruta real
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

contador = 1
for url, titulo in zip(urls, titulos):

    log(f"\n🔍 Procesando enlace ({contador}): {url}")

    if "ncbi.nlm.nih.gov/pmc/articles/" in url:
        match = re.search(r"(PMC\d+)", url)
        if match:
            pmc_id = match.group(1)
            url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"
        else:
            log(f"⚠️ No se pudo extraer PMC ID de {url}")
            continue
    else:
        log(f"⚠️ Enlace no reconocido como PMC, saltando: {url}")
        continue

    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", titulo).strip().replace(" ", "_")
    if not titulo_limpio:
        titulo_limpio = f"Paper_{contador}"

    log(f"⬇️ Descargando: {url}")

    try:
        archivos_antes = set(glob.glob(os.path.join(output_folder, "*.pdf")))
        log(f"📂 Archivos antes de descarga: {archivos_antes}")

        driver.get(url)

        descargando = True
        while descargando:
            time.sleep(1)
            tmp_files = glob.glob(os.path.join(output_folder, "*.crdownload"))
            if not tmp_files:
                descargando = False

        archivos_despues = set(glob.glob(os.path.join(output_folder, "*.pdf")))
        log(f"📂 Archivos después de descarga: {archivos_despues}")

        nuevos_archivos = archivos_despues - archivos_antes
        log(f"🆕 Nuevos archivos detectados: {nuevos_archivos}")

        if nuevos_archivos:
            archivo_descargado = list(nuevos_archivos)[0]
            log(f"📄 Archivo detectado para renombrar: {archivo_descargado}")
            nuevo_nombre = os.path.join(output_folder, f"{titulo_limpio}.pdf")
            os.rename(archivo_descargado, nuevo_nombre)
            log(f"✅ Guardado como: {nuevo_nombre}")
        else:
            log(f"⚠️ No se detectó PDF descargado para {titulo_limpio}")

        contador += 1

    except Exception as e:
        log(f"⚠️ Error descargando {url}: {e}")

driver.quit()
log("\n🎉 Proceso completado.")
log(f"📄 Log guardado en {log_path}")
