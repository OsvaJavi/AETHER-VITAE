import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# === CONFIGURACIÓN ===
usuario = "jgalazka"
repositorio = "SB_publications"
archivo = "SB_publication_PMC.csv"

output_folder = r"C:\Users\ovcor\OneDrive\Desktop\x"
os.makedirs(output_folder, exist_ok=True)

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
df = pd.read_csv(csv_path)

# Buscar columnas con enlaces
columnas_con_links = [col for col in df.columns if df[col].astype(str).str.contains("http", case=False, na=False).any()]
if not columnas_con_links:
    print("⚠️ No se encontraron enlaces en el CSV.")
    exit()

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

contador = 1
for url, titulo in zip(urls, titulos):
    extension = os.path.splitext(url.split("?")[0])[1]

    # Si no es un PDF directo, buscarlo en la página
    if not extension.lower() == ".pdf":
        print(f"🔍 Buscando PDF real en {url}...")
        try:
            r_page = requests.get(url, headers=headers, timeout=20)
            if r_page.status_code == 200:
                url_page = url
                soup = BeautifulSoup(r_page.content, "lxml")
                links = soup.find_all("a", href=True)
                pdf_links = [link['href'] for link in links if ".pdf" in link['href'].lower()]
                if pdf_links:
                    url = pdf_links[0]
                    if not url.startswith("http"):
                        if url.startswith("/"):
                            base = "https://www.ncbi.nlm.nih.gov"
                            url = base + url
                        else:
                            base = "/".join(url_page.split("/")[:3])
                            url = base + "/" + url
                    extension = ".pdf"
                else:
                    print(f"⚠️ No se encontró PDF en {url}")
                    continue
            else:
                print(f"⚠️ Error al acceder a {url}")
                continue
        except Exception as e:
            print(f"⚠️ Error analizando {url}: {e}")
            continue

    # Limpiar título
    titulo_limpio = re.sub(r'[\\/*?:"<>|]', "", titulo).strip().replace(" ", "_")
    if not titulo_limpio:
        titulo_limpio = f"Paper_{contador}"

    nombre_archivo = f"{contador}_{titulo_limpio}{extension}"
    destino = os.path.join(output_folder, nombre_archivo)

    print(f"⬇️ Descargando ({contador}): {url}")
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200 and "application/pdf" in r.headers.get("Content-Type", ""):
            with open(destino, "wb") as f:
                f.write(r.content)
            print(f"✅ Guardado como: {nombre_archivo}")
            contador += 1
        else:
            print(f"⚠️ No es un PDF válido: {url}")
    except Exception as e:
        print(f"⚠️ Error al descargar {url}: {e}")

print("\n🎉 Proceso completado.")
