from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuración del controlador Firefox
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Descomenta si deseas ejecutar en modo headless
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Firefox(options=options)

url = "https://pad.minem.gob.pe/REINFO_WEB/Index.aspx"
driver.get(url)

def sacaData():
    soup = BeautifulSoup(driver.page_source, "html.parser")  # Obtiene el contenido actualizado
    table = soup.find('table', class_="gvRow")
    
    if table is None:
        print("No se encontró la tabla.")
        return

    rows = table.find_all('tr')
    data = []

    for row in rows:
        cells = row.find_all(['td'])
        cell_data = [cell.get_text(strip=True) for cell in cells]
        if cell_data:
            data.append(cell_data)

    # Imprimir los datos extraídos para depuración
    print(f"Datos extraídos: {data}")

    df = pd.DataFrame(data)

    # Imprimir el DataFrame para ver cuántas columnas hay
    print(f"DataFrame antes del filtrado:\n{df}")

    # Asegúrate de que las columnas deseadas existan antes de filtrarlas
    if df.shape[1] >= 10:  # Cambiado a >= para permitir al menos 10 columnas
        columnas_deseadas = df.columns[1:10]
        df_filtrado = df[columnas_deseadas]
        df_filtrado.to_csv('data.csv', index=False, mode='a', header=not pd.io.common.file_exists('data.csv'))
    else:
        print("No hay suficientes columnas para filtrar.")

# SACA num page
def numPage():
    soup = BeautifulSoup(driver.page_source, "html.parser")  # Obtiene el contenido actualizado
    numTotalPages = soup.find("span", class_="pag_cssP", id="lblhasta")
    
    if numTotalPages:
        return int(numTotalPages.text.strip())
    
    return 0  # Retorna 0 si no se encuentra el elemento

def clickNextButton():
    nextPage = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='ImgBtnSiguiente']"))
    )
    nextPage.click()

# Obtiene el número total de páginas
actualPage = numPage()

for i in range(actualPage):
    sacaData()  # Extrae los datos de la página actual
    
    if i < actualPage - 1:  # Evita hacer clic en "Siguiente" en la última página
        clickNextButton()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ImgBtnSiguiente']")))  # Espera a que el botón esté disponible

# Cierra el controlador al final
driver.quit()