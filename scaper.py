import requests
import lxml.html as html
import os
import datetime

# Creamos constantes

HOME_URL = 'https://www.larepublica.co/'

# XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
# solucion al error
XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p//text()'


# Creamos las funcioens para ejecutar el script.

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[1]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f"{today}/{title}.txt", "w", encoding="utf-8") as f:
                f.write(title)
                f.write("\n\n")
                f.write(summary)
                f.write("\n\n")
                for p in body:
                    f.write(p)
                    f.write("\n")
        else:
            raise ValueError(f"Error: {response.status_code}")
    except ValueError as ve:
        print(ve)

def parse_home():
     # Creamos un bloque try para manejar los errores. Y manejar los Status Code.
    try:
        response = requests.get(HOME_URL)
         # Aqui va la lógica para traer los links.
        if response.status_code == 200:
             # .content trae  el HTML que necesita ser traducido con un decode para que python lo entienda
            # en terminos de caracteres, me devuelve un string que noes más que el HTML crudo.
            home = response.content.decode('utf-8')
            # Tambien podemos usar el método text para parsear la respuesta a texto.
            # home = response.text
            # print(home)

            # En esta línea uso el parser para transformar el contentido
            # html a un archivo que sea de utilidad para las expresiones xpath
            parsed = html.fromstring(home)
              # En esta línea estoy usando el archivo parseado con la función xpath y le paso por parámetro mi constante
            # la cual almacena la expresión Xpath.
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)
            
            # obteniendo la fecha y pasandola a string
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)    
        else:
            #Elevamos el error para ser capturado en el try-except, too lo que sea un error.
            raise ValueError(f"Error: {response.status_code}")
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()