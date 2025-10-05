import os
import re
import requests
import pandas as pd

# === CONFIGURACIÓN ===
usuario = "jgalazka"
repositorio = "SB_publications"
archivo = "SB_publication_PMC.csv"

output_folder = r"C:\Users\ovcor\OneDrive\Desktop\x"
os.makedirs(output_folder, exist_ok=True)

# URL raw correcta
url_csv = f"https://raw.githubusercontent.com/{usuario}/{repositorio}/main/{archivo}"
csv_path = os.path.join(output_folder, archivo)

headers = {"User-Agent": "Mozilla/5.0"}

print(f"⬇️ Descargando CSV desde {url_csv}...")
resp = requests.get(url_csv, headers=headers)
if resp.status_code != 200:
    print(f"❌ Error {resp.status_code} al descargar el CSV.")
    exit()

with open(csv_path, "wb") as f:
    f.write(resp.content)
print(f"✅ CSV guardado en {csv_path}")

# === LEER CSV ===
print("📖 Leyendo el archivo CSV...")
df = pd.read_csv(csv_path)

# Buscar columnas con enlaces
columnas_con_links = [col for col in df.columns if df[col].astype(str).str.contains("http", case=False, na=False).any()]
if not columnas_con_links:
    print("⚠️ No se encontraron enlaces en el CSV.")
    exit()

print(f"🔍 Columnas con enlaces encontradas: {columnas_con_links}")

# Buscar columna con título
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

print(f"🌐 Se encontraron {len(urls)} enlaces.")

# === DESCARGAR ARCHIVOS CON NOMBRE POR TÍTULO ===
for idx, (url, titulo) in enumerate(zip(urls, titulos), start=1):
    extension = os.path.splitext(url.split("?")[0])[1]
    if not extension:
        extension = ".pdf"

    # Limpiar título para que sea válido como nombre de archivo
    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", titulo).strip().replace(" ", "_")
    if not titulo_limpio:
        titulo_limpio = f"Paper_{idx}"

    nombre_archivo = f"{idx}_{titulo_limpio}{extension}"
    destino = os.path.join(output_folder, nombre_archivo)

    print(f"⬇️ Descargando ({idx}): {url}")
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            with open(destino, "wb") as f:
                f.write(r.content)
            print(f"✅ Guardado como: {nombre_archivo}")
        else:
            print(f"⚠️ Error {r.status_code} con {url}")
    except Exception as e:
        print(f"⚠️ Error al descargar {url}: {e}")

print("\n🎉 Proceso completado.")
