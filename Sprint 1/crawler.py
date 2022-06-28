import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

url = "https://nuforc.org/webreports/ndxevent.html"
urlbase = "https://nuforc.org/webreports/"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

lista_dfs = []
# i = 0 
for link in soup.find_all('a'):
    if 'https://www.nuforc.org' not in link.get('href'):
        mes, ano = link.text.split('/')  # separa mês e ano da string
        if mes.isnumeric() and ano.isnumeric():  # verifica se os campos correspondem a numeros e faz filtro por data
            if date(year=int(ano), month=int(mes), day=1) >= date(1997, 9, 1) and date(year=int(ano), month=int(mes), day=1) < date(2017, 9, 1):
                soup_table = requests.get(urlbase + link.get('href'))  # acessa dados das tabelas de cada data
                print(mes,ano)
                lista_dfs.append(pd.read_html(soup_table.text)[0])  # salva na lista de dataframes
                # i+=1
                # if i == 10:
                #     break

df = pd.concat(lista_dfs)
df = df[::-1]  # inverte ordem do dataframe para ficar os mais antigos primeiro 1997 -> 2017

df.to_csv("ovnis.csv", index=False)