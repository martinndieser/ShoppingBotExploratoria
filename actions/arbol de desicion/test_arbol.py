import pandas as pd
import joblib



path = "C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\actions\\arbol de desicion"
arbol = joblib.load(f"{path}\\arbol.pkl")


categorias = [
		"accesorios",
		"deporte",
		"gastronomía",
		"hogar",
		"hombre",
		"marroquinería",
		"mujer",
		"mujer/hombre",
		"niños/teens",
		"servicios",
		"tecnología",
		"varios"
	]

categoria_oferta = "varios"
oferta_limitada = True
es_cliente_habitual = False


oferta_limitada = '1' if oferta_limitada else '0'
es_cliente_habitual = '1' if es_cliente_habitual else '0'

edad = eval("19")
genero = "Masculino"
genero_Masculino = '1' if genero == "Masculino" else '0'
genero_Femenino = '1' if genero != "Masculino" else '0'

categorias_de_interes = eval("['deporte', 'mujer']") # lo interpreta python en una lista



def generar_categorias_hot_encoding(categorias, interes, nombre_prefijo=''):
	categorias_encoded = {}
	for cat in categorias:
		if cat in interes:
			categorias_encoded.update({f'{nombre_prefijo}{cat}': [1]})
		else:
			categorias_encoded.update({f'{nombre_prefijo}{cat}': [0]})
	return categorias_encoded


categorias_encoded = generar_categorias_hot_encoding(categorias, categorias_de_interes)
categorias_promocion_encoded = generar_categorias_hot_encoding(categorias, [categoria_oferta], nombre_prefijo='categoria_promocion_')



#print(categorias_promocion_encoded)

data = pd.DataFrame({
		'edad': [edad],
		'es_cliente_habitual': [es_cliente_habitual],
		'oferta_limitada': [oferta_limitada],
		**categorias_encoded,
		'genero_Masculino': genero_Masculino,
		'genero_Femenino': genero_Femenino,
		**categorias_promocion_encoded
	})


print(data)

y_pred = arbol.predict(data)
print(y_pred)