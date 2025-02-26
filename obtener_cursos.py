import csv
import json 
import requests
from bs4 import BeautifulSoup
import os

def obtener_cursos() -> list:
    cursos: list = []
    with open("data/cursos.csv", "r", encoding="utf-8") as f:
        dato = csv.reader(f,delimiter=",")
        for i in dato:
            cursos.append(i)
    return cursos

#print(obtener_cursos())

def generar_horarios_curso(nombre_curso: str, url: str) -> dict:
    print("generando")
    cursos: dict = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    print(nombre_curso, url)
    tabla_cursos = soup.find_all("tr")
    limite: int = len(tabla_cursos)
    indice: int = 0
    while indice < limite:
        if tabla_cursos[indice].find_all("td")[0].text.isnumeric():
            elementos = tabla_cursos[indice].find_all("td")
            #print(elementos[1].text)
            cursos[elementos[1].text] = {
                "nombre": f"{elementos[2].text} grupo {elementos[1].text[-2]}",
                "LU": [],
                "MA": [],
                "MI": [],
                "JU": [],
                "VI": [],
                "SA": []
            }
            indice+=2
            #print(indice, limite)
            #print(tabla_cursos[indice].find_all("td")[0].text.isnumeric())
            while (indice < limite) and not(tabla_cursos[indice].find_all("td")[0].text.isnumeric()):
                dia = tabla_cursos[indice].find_all("td")[1].text
                hora = tabla_cursos[indice].find_all("td")[2].text
                hora = hora[1:]
                hora: str = hora[:len(hora)-1]
                hora = hora.split("-")
                #print(dia, hora)
                for h in range(int(hora[0]), int(hora[1])):
                    cursos[elementos[1].text][dia].append(h)
                #cursos[elementos[1].text][dia].append(hora)
                indice += 1
            #break

        indice += 1
    return cursos

def generar_horarios_general() -> dict:
    carrera_url = obtener_cursos()
    carreras: dict = {}
    for nombre, url in carrera_url:
        print(nombre)
        try:
            carreras[nombre] = generar_horarios_curso(nombre, url)
        except:
            print(f"Error en {nombre}")
    direccion = os.path.join("data", "carreras_cursos.json")
    with open(direccion, "w", encoding="utf-8") as f:
        json.dump(carreras, f)
    


    

generar_horarios_general()