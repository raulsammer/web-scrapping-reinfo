from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = webdriver.FirefoxOptions()
options.add_argument("--headless") 
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Firefox(options=options)

# URL y encabezados para la solicitud
url = "https://www.machinefinder.com/ww/es-PE/mf/all-countries"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

# Realizar la solicitud y parsear el HTML
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

linksAndCounts = {}
linksAndCounts25 = {}

"""# Extraer enlaces y conteos
subList = soup.find_all("div", class_="build-kinds")

for div in subList:
    links = div.find_all('a')
    counts = div.find_all("span", class_="count")
    
    for link, count in zip(links, counts):
        href = link.get('href')
        textCount = count.text
        linksAndCounts[href] = int(textCount)

# Mover valores mayores a 25 a otro diccionario
for href, count in list(linksAndCounts.items()):
    if count > 25:
        linksAndCounts25[href] = count  
        del linksAndCounts[href]  

linksMaquinas = []

# Extraer enlaces de máquinas
for i in list(linksAndCounts.keys()):
    pageMaq = requests.get("https://www.machinefinder.com" + i)
    soupMaq = BeautifulSoup(pageMaq.text, "html.parser")
    
    divs = soupMaq.find_all("div")  # Encuentra todos los divs

    for div in divs:
        a_tag = div.find("a")  # Busca el primer <a> dentro del div
        if a_tag and "/ww/es-PE/machines/" in a_tag['href']:  # Verifica si el href contiene la parte deseada
            full_link = "https://www.machinefinder.com" + a_tag['href']  # Concatenar la base de la URL
            linksMaquinas.append(full_link)  # Agregar el enlace a la lista

# Eliminar duplicados y crear una nueva lista de enlaces únicos
unique_links_list = list(set(linksMaquinas))"""

# Iterar sobre cada enlace en la lista única
"""for i in unique_links_list:
    try:
        driver.get(i)  # Navegar a la URL
        time.sleep(2)  # Esperar un momento para que la página se cargue completamente

        html_content = driver.page_source  # Obtener el contenido HTML de la página

        # Analizar el contenido con Beautiful Soup
        soupXD = BeautifulSoup(html_content, "html.parser")

        # Imprimir el contenido o extraer datos específicos
        print(f"Éxito al procesar: {i}")
        #print(soupXD.prettify())  # Usar prettify() para una mejor visualización

    except Exception as e:
        print(f"Error al procesar {i}: {e}")  # Imprimir el error y continuar con el siguiente enlace

# Cerrar el navegador después de procesar todos los enlaces
driver.quit()"""

driver.get("https://www.machinefinder.com/ww/es-PE/machines/10536593")  # Navegar a la URL
#time.sleep(2) 
html_content = driver.page_source  
# Analizar el contenido con Beautiful Soup
soupXD = BeautifulSoup(html_content, "html.parser")
time.sleep(2)
# Imprimir el contenido o extraer datos específicos
titlesMaq = []
vendedoresMaquina = []
precios = []
ubicacionesVentaPais = []
horometros = []
ubicacionesVentaCiudad = []
marcasFabricante = []
añosFabricacion = []
linksWebSiteMaquina = []
modeloMaquina = []

titlesMaqs = soupXD.title.string 
titlesMaq.append(titlesMaqs.split('|')[0].strip())

# Encontrar todas las filas de información
rows = soupXD.find_all('div', class_='mf-ip-row')
#print("ROWSSSSSSSSSSSSSSSS", rows)
# Iterar sobre cada fila y extraer los datos
for row in rows:
    label_div = row.find('div', class_='mf-ip-lbl')
    value_div = row.find('div', class_='mf-ip-val')

    # Verificar si ambos elementos se encontraron
    if label_div and value_div:
        label = label_div.get_text(strip=True) 
        value = value_div.get_text(strip=True) 

        # Agregar a las listas según el label
        if label == "Modelo":
            modeloMaquina.append(value)
        elif label == "Marca":
            marcasFabricante.append(value)
        elif label == "Año de fabricación":
            añosFabricacion.append(value)

print("Modelos:", modeloMaquina)
print("Marcas:", marcasFabricante)
print("año: ", añosFabricacion)
    
# Extraer ciudad y país
ciudad = []
pais = []


value_div = soupXD.find('div', class_='mf-ip-val comma-between')
if value_div:
    city_state_span = value_div.find('span', attrs={'ng-if': '$ctrl.machine.dealer.city_state'})
    if city_state_span:
        ciudad.append(city_state_span.get_text(strip=True))

    country_span = value_div.find('span', attrs={'ng-if': '$ctrl.machine.dealer.country'})
    if country_span:
        pais.append(country_span.get_text(strip=True))

print("Ciudad:", ciudad)
print("País:", pais)


title = soupXD.title
finalTitle=title.string
titlesMaq.append(finalTitle.split('|')[0].strip())
print(titlesMaq) 
driver.quit() 