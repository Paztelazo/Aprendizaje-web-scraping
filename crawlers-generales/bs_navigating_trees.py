from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(), "html.parser")

img_list= bs.find('table', {'id': 'giftList'})

#for child in img_list.children:
#    print(child)


#Este código imprime todos los elementos hijos del elemento con el id "giftList" en la página web.
#Incluyendo los elementos de texto y los elementos de etiqueta.

#sibilings: son los elementos que están al mismo nivel jerárquico que el elemento actual.
#for sibling in img_list.tr.next_siblings:
#    print(sibling)

#También hay función previous_sibling y next_sibling, que devuelve el elemento hermano anterior y siguiente al elemento actual.

print(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
#Tambien hay una función parent, que devuelve el elemento padre del elemento actual. En este caso, se está buscando el elemento padre del elemento img con el src '../img/gifts/img1.jpg', y luego se está obteniendo el texto del elemento hermano anterior a ese elemento padre.
#Se usa usualmente cuando se quiere obtener información relacionada con un elemento específico en la página web, 
# como el nombre del regalo en este caso.




