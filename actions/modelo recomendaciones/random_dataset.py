import csv
import random

# Configuración
min_valoracion = 1.0
max_valoracion = 10.0

productos_por_categorias = {
    "accesorios": ["collar", "lentes", "anillo", "pesas", "pelota", "raqueta", "cartera", "cinturón", "lámpara"],
    "deporte": ["pesas", "pelota", "raqueta"],
    "gastronomía": ["hamburguesa", "comida", "snacks"],
    "hogar": ["sábanas", "mueble", "lámpara"],
    "hombre": ["boxer", "remera polo", "kit de afeitado", "pantalón chino", "jean"],
    "marroquinería": ["cartera", "cinturón", "cuero"],
    "mujer": ["vestido", "bolso", "tacos", "remera", "mueble", "lámpara"],
    "mujer/hombre": ["vestido", "bolso", "tacos", "remera", "boxer", "remera polo", "kit de afeitado", "cartera", "cinturón", "cuero"],
    "niños/teens": ["ropa para niño"],
    "servicios": ["pagar servicios", "masaje", "reparación"],
    "tecnología": ["celular", "auricular", "laptop"],
    "varios": ["juego de mesa"]
}



locales = [
    {
      "local": "+ visión",
      "categoria": "accesorios"
    },
    {
      "local": "47 street",
      "categoria": "niños/teens"
    },
    {
      "local": "a.y. not dead",
      "categoria": "mujer/hombre"
    },
    {
      "local": "adriana costantini",
      "categoria": "mujer"
    },
    {
      "local": "akiabara",
      "categoria": "mujer"
    },
    {
      "local": "almundo.com",
      "categoria": "varios"
    },
    {
      "local": "alvarado",
      "categoria": "gastronomía"
    },
    {
      "local": "allô martinez",
      "categoria": "mujer"
    },
    {
      "local": "arredo",
      "categoria": "hogar"
    },
    {
      "local": "awada",
      "categoria": "mujer"
    },
    {
      "local": "ayres",
      "categoria": "mujer"
    },
    {
      "local": "beneida",
      "categoria": "mujer"
    },
    {
      "local": "bensimon",
      "categoria": "hombre"
    },
    {
      "local": "besha",
      "categoria": "marroquinería"
    },
    {
      "local": "broer",
      "categoria": "niños/teens"
    },
    {
      "local": "cala",
      "categoria": "mujer"
    },
    {
      "local": "caro cuore",
      "categoria": "mujer"
    },
    {
      "local": "centro rossi",
      "categoria": "servicios"
    },
    {
      "local": "ceremony",
      "categoria": "mujer/hombre"
    },
    {
      "local": "columbia",
      "categoria": "deporte"
    },
    {
      "local": "como quieres",
      "categoria": "niños/teens"
    },
    {
      "local": "complot",
      "categoria": "mujer"
    },
    {
      "local": "crêperie",
      "categoria": "gastronomía"
    },
    {
      "local": "cheeky",
      "categoria": "niños/teens"
    },
    {
      "local": "definit",
      "categoria": "servicios"
    },
    {
      "local": "delsey",
      "categoria": "varios"
    },
    {
      "local": "desiderata",
      "categoria": "mujer"
    },
    {
      "local": "elepants",
      "categoria": "mujer/hombre"
    },
    {
      "local": "estancias",
      "categoria": "mujer"
    },
    {
      "local": "eyelit",
      "categoria": "hombre"
    },
    {
      "local": "forever 21",
      "categoria": "mujer"
    },
    {
      "local": "giro didactico",
      "categoria": "niños/teens"
    },
    {
      "local": "grabatto",
      "categoria": "varios"
    },
    {
      "local": "grimoldi",
      "categoria": "marroquinería"
    },
    {
      "local": "grisino",
      "categoria": "niños/teens"
    },
    {
      "local": "havanna",
      "categoria": "gastronomía"
    },
    {
      "local": "home collection",
      "categoria": "hogar"
    },
    {
      "local": "india style",
      "categoria": "mujer"
    },
    {
      "local": "isadora",
      "categoria": "accesorios"
    },
    {
      "local": "juleriaque",
      "categoria": "varios"
    },
    {
      "local": "kosiuko",
      "categoria": "mujer/hombre"
    },
    {
      "local": "la martina",
      "categoria": "mujer/hombre"
    },
    {
      "local": "lacoste",
      "categoria": "mujer/hombre"
    },
    {
      "local": "las pepas",
      "categoria": "mujer"
    },
    {
      "local": "le pain quotidien",
      "categoria": "gastronomía"
    },
    {
      "local": "levi's",
      "categoria": "mujer/hombre"
    },
    {
      "local": "little akkiabara",
      "categoria": "niños/teens"
    },
    {
      "local": "maría cher",
      "categoria": "mujer"
    },
    {
      "local": "maría rivolta",
      "categoria": "accesorios"
    },
    {
      "local": "markova",
      "categoria": "mujer"
    },
    {
      "local": "mccafé",
      "categoria": "gastronomía"
    },
    {
      "local": "mcdonald's",
      "categoria": "gastronomía"
    },
    {
      "local": "mimo & co.",
      "categoria": "niños/teens"
    },
    {
      "local": "mishka",
      "categoria": "marroquinería"
    },
    {
      "local": "morph",
      "categoria": "hogar"
    },
    {
      "local": "mostaza",
      "categoria": "gastronomía"
    },
    {
      "local": "naíma",
      "categoria": "mujer"
    },
    {
      "local": "nespresso",
      "categoria": "varios"
    },
    {
      "local": "okko kitchen",
      "categoria": "hogar"
    },
    {
      "local": "oneclick",
      "categoria": "tecnología"
    },
    {
      "local": "opi wella",
      "categoria": "varios"
    },
    {
      "local": "osito azul",
      "categoria": "niños/teens"
    },
    {
      "local": "oxford polo club",
      "categoria": "hombre"
    },
    {
      "local": "pago fácil - western union",
      "categoria": "servicios"
    },
    {
      "local": "pandora",
      "categoria": "accesorios"
    },
    {
      "local": "paula cahen d'anvers",
      "categoria": "mujer"
    },
    {
      "local": "pelukids",
      "categoria": "servicios"
    },
    {
      "local": "penguin",
      "categoria": "hombre"
    },
    {
      "local": "portsaid",
      "categoria": "mujer"
    },
    {
      "local": "prototype",
      "categoria": "hombre"
    },
    {
      "local": "prüne",
      "categoria": "marroquinería"
    },
    {
      "local": "ramira",
      "categoria": "accesorios"
    },
    {
      "local": "rapsodia",
      "categoria": "mujer"
    },
    {
      "local": "rever pass",
      "categoria": "hombre"
    },
    {
      "local": "rochas",
      "categoria": "hombre"
    },
    {
      "local": "samsung",
      "categoria": "tecnología"
    },
    {
      "local": "selú",
      "categoria": "mujer"
    },
    {
      "local": "simmons",
      "categoria": "hogar"
    },
    {
      "local": "sweet",
      "categoria": "mujer"
    },
    {
      "local": "tienda líder",
      "categoria": "accesorios"
    },
    {
      "local": "tucci",
      "categoria": "mujer"
    },
    {
      "local": "valtik care & beauty",
      "categoria": "servicios"
    },
    {
      "local": "wanama",
      "categoria": "mujer"
    },
    {
      "local": "xl extra large",
      "categoria": "marroquinería"
    },
    {
      "local": "yenny",
      "categoria": "varios"
    },
    {
      "local": "zwass",
      "categoria": "marroquinería"
    }
  ]


with open('dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Local', 'Producto', 'Valoración']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for local in locales:
        nombre_local = local['local']
        categoria = local['categoria']
        productos_posibles = productos_por_categorias[categoria]

        for i in range(random.randint(1,5)):
            prob_mala_compra = 0.1
            if ((1/random.randint(1,10)) == prob_mala_compra):
                prod = random.choice(productos_posibles)
                valoracion = 0
                writer.writerow({'Local': nombre_local, 'Producto': prod, 'Valoración': valoracion})
            elif ((1/random.randint(1,10)) == 0.2):
                prod = random.choice(productos_posibles)
                valoracion = 0.5
                writer.writerow({'Local': nombre_local, 'Producto': prod, 'Valoración': valoracion})
            else:
                prod = random.choice(productos_posibles)
                valoracion = 1
                writer.writerow({'Local': nombre_local, 'Producto': prod, 'Valoración': valoracion})
    #for local in locales:
    #    for i in range(random.randint(1,3)):
    #        compra = random.choice(compras)
    #        valoracion = random.randint(min_valoracion, max_valoracion)
    #        writer.writerow({'Local': local, 'Producto': compra, 'Valoración': valoracion})
