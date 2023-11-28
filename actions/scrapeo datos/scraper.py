import requests
import re
import json

host = "elsolarshopping.com.ar"
categories = {}


# la tienda que se llama Levi's se traduce a Levi"s y produce errores


session = requests.Session()
session.verify = False

class Shop:
  def __repr__(self):
    return f'name={self.name} category={self.category} shopping_location={self.shopping_location} phone={self.phone} web_link={self.web_link}'
  
  def __init__(self, name, category, shopping_location=None, phone=None, web_link=None):
    self.name = name
    self.category = category
    self.shopping_location = shopping_location
    self.phone = phone
    self.web_link = web_link

  def dict(self):
    return {
      'name': self.name,
      'category': self.category,
      'shopping_location': self.shopping_location,
      'phone': self.phone,
      'web_link': self.web_link
    }


def create_url(host, endpoint):
  return f'https://{host}/{endpoint}'


def get_shops_categories() -> dict:
  options = [
    'accesorios/10',
    'deporte/8',
    'gastronom-a/5',
    'hogar/6',
    'hombre/2',
    'marroquiner-a/9',
    'mujer/1',
    'mujer-hombre/3',
    'ni-os-teens/4',
    'servicios/7',
    'tecnolog-a/11',
    'varios/12'
  ]

  categories = {}

  for option in options:
    response = session.get(create_url(host, f'locales/{option}'))
    category_name = re.search(r'selected>(.*)<\/option>', response.text).group(1)
    categories[category_name] = re.findall(r'h2>\s+<h1>(.+)<\/h1>', response.text)
  return categories

def get_category_by_shop_name(shop_name):
  global categories
  if not categories:
    categories = get_shops_categories()
  
  for category in categories:
    for shop in categories[category]:
      if (shop_name == shop):
        return category
  return None

def get_urls():
  endpoint = "locales"
  response = session.get(create_url(host, endpoint))
  endpoints = re.findall(r'<a href="(local\/.*)">', response.text)
  return endpoints



def get_details_for_shop(endpoint):
  response = session.get(create_url(host, endpoint)).text
  name = re.search(r'<div class="d2">(.*)<\/div', response).group(1).strip()
  shopping_location = re.search(r't1">Nivel<\/div>(.*)<\/div>', response).group(1).strip()
  phone = re.search(r'fono<\/div>(.*)<\/div>', response).group(1).strip()
  web_link = re.search(r'Web<\/div><a href="https{0,1}://(.*)" target="_blank', response).group(1).strip()
  return Shop(name=name, category= get_category_by_shop_name(name),shopping_location=shopping_location, phone=phone, web_link=web_link)


def scrape_info():
  endpoints = get_urls()
  for endpoint in endpoints:
    shop = get_details_for_shop(endpoint)
  shops = [get_details_for_shop(endpoint).dict() for endpoint in endpoints]

  with open('shops.json', 'w') as f:
    json.dump(shops, f, indent=4)


def shop_to_prolog_sentences(shop):
  if not shop.name:
    return ""
  name_sentence = f'local("{shop.name}","{shop.category}").' if shop.category else None
  location_sentence = f'nivel("{shop.name}","{shop.shopping_location}").' if shop.shopping_location else None
  phone_sentence = f'telefono("{shop.name}","{shop.phone}").' if shop.phone else None
  web_link_sentence = f'pagina_web("{shop.name}","{shop.web_link}").' if shop.web_link else None

  return {
    'local':name_sentence,
    'nivel':location_sentence,
    'telefono':phone_sentence,
    'pagina_web': web_link_sentence
    }


def categories_to_prolog():
  global categories
  if not categories:
    categories = get_shops_categories()

  return [f'categoria("{category}").' for category in categories]

def make_prolog_sentences():
  with open('shops.json', 'r') as f:
    shops = json.load(f)

  prolog_prog = ""

  facts_structure = {
    'local': [],
    'nivel': [],
    'telefono': [],
    'pagina_web': []
  }

  for shop in shops:
    sentences = shop_to_prolog_sentences(Shop(
          shop['name'],
          shop['category'],
          shop['shopping_location'],
          shop['phone'],
          shop['web_link']
      )
    )

    for sentence in sentences:
      if sentences[sentence]:
        facts_structure[sentence].append(sentences[sentence])

  prolog_prog = ""
  for key in facts_structure:
    prolog_prog += "\n".join(facts_structure[key])
    prolog_prog += "\n"

  prolog_prog += "\n".join(categories_to_prolog())
  print(prolog_prog)


if __name__ == '__main__':
  make_prolog_sentences()