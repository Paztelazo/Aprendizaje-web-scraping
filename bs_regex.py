from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img',
    {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
for image in images: 
    print(image['src'])


#También podemos devolver los atributos de un elemento utilizando .attrs. 
# Por ejemplo, para devolver el atributo src de un elemento img, podemos usar image.attrs['src'].
    print(image.attrs['src'])