from bs4 import BeautifulSoup
import requests
import json
import os

def listar_cursos(url = "http://ccomputo.unsaac.edu.pe/?op=catalog"):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    elementos = []
    for center in soup.find_all("tr"):
        if (len(center.find_all('a'))!= 0):
            elementos.append(['http://ccomputo.unsaac.edu.pe/' + center.find_all('a')[0]['href']])

    for i in range(len(elementos)):
        data = soup.find_all('tr')[i+1]
        data = data.find_all('td')[1]
        elementos[i].insert(0,data.text)
    
    return elementos


def guardar_datos(elemento: list, nombre: str):
    direccion = f"data/{nombre}.csv"
    f = open(direccion, "w", encoding="utf-8")
    for i in elemento:
        f.write(f"{i[0]},{i[1]}\n")
    

guardar_datos(listar_cursos(),"cursos")