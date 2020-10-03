import requests
import json
import csv
import codecs

class Curso:
  def __init__(self, titulo, autor, url, carpeta):
    self.titulo=titulo
    self.autor=autor
    self.url=url
    self.carpeta=carpeta
    
  def mostrar(self):
    print ("Título: "+self.titulo+"\nAutor: "+str(self.autor)+"\nPlataforma: Udemy\nUrl: "+self.url+"\nCarpeta: "+self.carpeta+"\n")
    

access_token = "TU ACCESS TOKEN"

headers = {
    'authorization': 'Bearer ' + access_token ,
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}

course_dict = {}
counter = 1
copia = []

while(1):
  params = (
    ('ordering', '-last_accessed'),
    ('page', str(counter)),
    ('page_size', '100'),
  )

  response = requests.get('https://www.udemy.com/api-2.0/users/me/subscribed-courses/', headers=headers, params=params)
  json_data = json.loads(response.text)

  if "results" in json_data:
      for data in json_data['results']:
        #print (data.keys())
        
        course_dict.update({data['title']:"https://www.udemy.com"+data['url']}) 
        autores=""
        for i in data['visible_instructors']:
          aut=(i['title']).strip()
          if (aut.find('Dr. ')>-1):
            aut=aut.partition('Dr. ')[2]
          if (aut.find('Ing. ')>-1):
            aut=aut.partition('Ing. ')[2]
          if (aut.find('Lic. ')>-1):
            aut=aut.partition('Lic. ')[2]
          if (aut.find(' |')>-1):
            aut=aut.partition(' |')[0]
          if (aut.find(' ,')>-1):
            aut=aut.split(', ','2')
            aut=aut[0]+aut[1]
          if (len(aut)>29):
            aut=aut[:30]
            
          if autores=="":
            autores=aut.strip()
          else:
            autores=autores+", "+aut.strip()

        copia.append (Curso(data['title'].strip(), autores, "https://www.udemy.com"+data['url'], data['published_title'].strip()))
        
  counter+=1  
  if not "results" in json_data:
   break


with codecs.open('ListaCursosUdemy.csv', 'w', encoding="utf-8-sig") as file:
  writer = csv.writer(file)  
  for item in copia:
    item.mostrar()
    fila=[item.titulo+"\t"+item.autor+"\t"+"Udemy"+"\t"+item.url+"\t"+item.carpeta]
    writer.writerow(fila)