from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd

options = webdriver.FirefoxOptions()
options.add_argument("--headless") 
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Firefox(options=options)

url = "https://pad.minem.gob.pe/REINFO_WEB/Index.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")
table = soup.find('table', class_="gvRow")
rows = table.find_all('tr')

data = []

for row in rows:
    cells = row.find_all(['td'])
    cell_data = [cell.get_text(strip=True) for cell in cells]
    if cell_data:
        data.append(cell_data)

df = pd.DataFrame(data)

columnas_deseadas = df.columns[1:10]
df_filtrado = df[columnas_deseadas]

df_filtrado.to_csv('data.csv', index=False)
