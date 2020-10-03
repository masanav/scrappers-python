import requests
from requests import get
from bs4 import BeautifulSoup
import csv

class Curso:
  def __init__(self, titulo, autor, url, id, precio, fecha_extreno):
    self.titulo=titulo
    self.autor=autor
    self.url=url
    self.id=id
    self.precio=precio
    self.fecha_estreno=fecha_estreno
    
  def mostrar(self):
    print ("Título: "+self.titulo+"\nAutor: "+str(self.autor)+"\nUrl: "+self.url +"\nId: "+self.id+"\nPrecio: "+self.precio+"\nFecha estreno: "+self.fecha_estreno+"\n")
    

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}


counter = 1
lista_cursos=[]
max_pag=""
url_base = "https://www.domestika.org/es/courses/recent"

while(True):
  url = url_base+"?page="+str(counter)

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup (response.text, "html.parser")

  scripts = soup.findAll ("script")
  
  if (max_pag == ""):
    for item in scripts:
      cadena=str(item)
      if ("total_pages" in cadena):
        index = cadena.index("total_pages")
        longi_sobra=len("total_pages")+index
        max_pag=int(cadena[longi_sobra+2:longi_sobra+2+2])
        break

  cursos_div = soup.findAll('div', 'course-item__details')

  for item in cursos_div:
    titulo = item.h3.a.text.replace("\n","").strip()
    autores = item.p.text.replace("\n","").strip().replace("Un curso de ","").replace("Por ","")
    datos = item.h3.a
    url = datos['href']
    id = datos['data-track-gtm-id']
    precio = datos['data-track-gtm-price']
    fecha_estreno = item.find ('li', 'course-opening').text.strip().replace("\n","") if item.find ('li', 'course-opening') else "-"
    #print (fecha_estreno)
    lista_cursos.append (Curso(titulo, autores, url, id, precio, fecha_estreno))


  counter=counter+1

  if (int(max_pag) == counter):
    break

print ("Cursos listados: "+str(len(lista_cursos)))

with open('ListaCursosDomestika.csv', 'w', encoding="utf-8-sig", newline='') as file:
  writer = csv.writer(file)
  writer.writerow(["Titulo", "Autor", "Url", "Id", "Precio", "Fecha de publicación"])
  for item in lista_cursos:
    #item.mostrar()
    fila=[item.titulo+"\t"+item.autor+"\t"+item.url+"\t"+item.id+"\t"+item.precio+"\t"+item.fecha_estreno]
    writer.writerow(fila)
