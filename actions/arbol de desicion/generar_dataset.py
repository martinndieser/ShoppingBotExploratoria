import random
# que se tienen en cuenta para generar este dataset:
# se adapto esta medida para entrenar el arbol de desición
# dado a la gran cantidad de categorias que existen



# si es un comprador habitual y la oferta es por un tiempo limitado
# entonces se busca que se la recomiende

# si el producto que se esta recomendando este entre
# las categorias de interes, se le debe recomendar

# si el producto no esta en las categorias de interes

# además se agrego la posibilidad de agrupar categorias "similares"
# para brindar una mayor cantidad de ofertas al comprador

categorias_y_productos = {
		"accesorios": ['collar','lentes','anillos'],
		"deporte": ['pesas','pelota','raqueta'],
		"gastronomía": ['hamburguesa','comida','snacks'],
		"hogar": ['savanas','mueble','lámpara'],
		"hombre": ['boxer','remera polo','kit de afeitado'],
		"marroquinería": ['cartera','cinturon','cuero'],
		"mujer": ['vestido','bolso','tacos'],
		"mujer/hombre": ['remera','jean','pantalon chino'],
		"niños/teens": ['mochila', 'ropa para niño', 'juego de mesa'],
		"servicios": ['pagar servicios', 'masaje', 'reparación'],
		"tecnología": ['celular','tecnología','laptop'],
		"varios": ['termo','cuaderno']
	}


filas = []
x = 0


categorias = list(categorias_y_productos.keys())
#print(categorias)
prob_oferta_limitada = 0.75
prob_comprador_habitual = 0.25

generos = ["Masculino", "Femenino"]


categorias_que_no_le_interesan_por_genero = {
	"Masculino": ['mujer', 'hogar', 'accesorios', 'marroquinería', 'niños/teens'],
	"Femenino": ['hombre', 'tecnología', 'gastronomía'],
} # son datos totalmente arbitrarios para que el árbol pueda podar

categorias_que_no_le_interesan_a_rango_etario = {
	(14,25): ['hogar', 'marroquinería', 'servicios', 'varios'],
	(25, 60): [],
	(60, 81): ['accesorios', 'gastronomía', 'varios', 'servicios']
} # son datos totalmente arbitrarios para que el árbol pueda podar


MIN_EDAD = 14
MAX_EDAD = 80


def obtener_categorias_adicionales(categoria_a_incluir, categorias, edad, genero):
	categorias_copia = categorias.copy()
	categorias_de_interes = {categoria_a_incluir: 1}
	categorias_copia.remove(categoria_a_incluir)

	for rango in categorias_que_no_le_interesan_a_rango_etario:
		#print(rango, rango[0], rango[1],(rango[0] <= edad),(edad < rango[1]), edad)
		if (rango[0] <= edad) and (edad < rango[1]):
			no_le_gustan = categorias_que_no_le_interesan_a_rango_etario[rango]
			break

	for no in no_le_gustan:
		categorias_de_interes[no] = 0
		categorias_copia.remove(no)


	i = 0
	max_i = random.randint(0,len(categorias_copia)-1)
	for i in range(max_i):
		categoria_adicional = categorias_copia[int(random.random() * len(categorias_copia))]
		categorias_de_interes.update({categoria_adicional:1})
		categorias_copia.remove(categoria_adicional)

	for cat in categorias_copia:
		categorias_de_interes.update({cat: 0})
	return categorias_de_interes


# primero generamos los datos de donde si hay que recomendarle
for i in range(150):
	for categoria in categorias_y_productos:
		edad = random.randint(MIN_EDAD, MAX_EDAD)
		genero = random.choice(generos)
		#
		if categoria in categorias_que_no_le_interesan_por_genero[genero]:
			continue

		for rango in categorias_que_no_le_interesan_a_rango_etario:
			#print(rango, (rango[0] <= edad) and (edad < rango[1]), edad)
			if (rango[0] <= edad) and (edad < rango[1]):
				no_le_gustan = categorias_que_no_le_interesan_a_rango_etario[rango]
				break

		if categoria in no_le_gustan:
			continue

		x += 1
		categorias_de_interes = obtener_categorias_adicionales(categoria, categorias, edad, genero)
		categoria_promocion = random.choice([cat for cat in categorias_de_interes if categorias_de_interes[cat]])
		#print(categorias_de_interes)
		es_cliente_habitual = 1 if random.random() < prob_comprador_habitual else 0
		oferta_limitada = 1 if random.random() < prob_oferta_limitada else 0
		recomendar = 1
		filas.append([x, edad, genero, recomendar, es_cliente_habitual, categoria_promocion, oferta_limitada, categorias_de_interes])

y = x
print('Datos donde recomendar=1: ' + str(x))

# generamos los datos donde no hay que recomendar
for i in range(1600):
	categoria = random.choice(categorias)
	edad = random.randint(MIN_EDAD, MAX_EDAD)
	genero = random.choice(generos)
	#
	if categoria in categorias_que_no_le_interesan_por_genero[genero]:
		continue

	for rango in categorias_que_no_le_interesan_a_rango_etario:
		#print(rango, (rango[0] <= edad) and (edad < rango[1]), edad)
		if (rango[0] <= edad) and (edad < rango[1]):
			no_le_gustan = categorias_que_no_le_interesan_a_rango_etario[rango]
			break

	if categoria in no_le_gustan:
		continue

	x += 1
	categorias_de_interes = obtener_categorias_adicionales(categoria, categorias, edad, genero)
	categoria_sin_interes = random.choice([cat for cat in categorias_de_interes if not categorias_de_interes[cat]])

	es_cliente_habitual = 1 if random.random() < prob_comprador_habitual else 0
	oferta_limitada = 1 if random.random() < prob_oferta_limitada else 0
	if es_cliente_habitual and oferta_limitada:
		recomendar = 1
	else:
		recomendar = 0
	filas.append([x, edad, genero, recomendar, es_cliente_habitual, categoria_sin_interes, oferta_limitada, categorias_de_interes])

print('Datos donde recomendar=0: ' + str(x-y))

random.shuffle(filas)

# generamos el header_del_csv
nom_col_categorias = categorias
header_csv = [
	"id",
	"edad",
	"genero",
	"recomendar",
	"es_cliente_habitual",
	'categoria_promocion',
	'oferta_limitada',
	*nom_col_categorias
]

delimitador = ','
with open('dataset.csv', 'w', encoding='utf-8') as f:
	f.write(f'{delimitador}'.join(header_csv))	
	f.write('\n')
	for fil in filas:
		for j in range(len(fil)-1):
			f.write(f'{fil[j]}{delimitador}')

		# esto corresponde a categoria de intereses
		texto = ""
		for cat in categorias:
			print(fil[len(fil)-1])
			texto += f'{fil[len(fil)-1][cat]}{delimitador}'
			# mapeamos cada resultado con el correspondiente
			#f.write(f'{fil[len(fil)-1]}\n')
		# limpiamos la última coma
		texto = texto[:-1:]
		f.write(texto)
		f.write('\n')

