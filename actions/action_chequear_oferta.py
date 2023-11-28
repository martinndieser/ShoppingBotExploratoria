from .prolog import prolog
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import joblib
import pandas as pd



path_arbol = "C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\actions\\arbol de desicion"
arbol = joblib.load(f"{path_arbol}\\arbol.pkl")




def hacer_prediccion_recomendacion(
	edad: int,
	genero: str,
	es_cliente_habitual: bool,
	categorias_de_interes: list,
	categorias: list,
	categoria_oferta: str,
	oferta_limitada: bool):


	es_cliente_habitual = '1' if es_cliente_habitual else '0'
	edad = eval(edad)
	genero_Masculino = '1' if genero == "Masculino" else '0'
	genero_Femenino = '1' if genero != "Masculino" else '0'
	categorias_de_interes = list(categorias_de_interes)

	oferta_limitada = '1' if oferta_limitada else '0'

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


	data = pd.DataFrame({
		'edad': [edad],
		'es_cliente_habitual': [es_cliente_habitual],
		'oferta_limitada': [oferta_limitada],
		**categorias_encoded,
		'genero_Masculino': genero_Masculino,
		'genero_Femenino': genero_Femenino,
		**categorias_promocion_encoded
	})

	y_pred = arbol.predict(data)

	return y_pred[0]

class ActionOferta(Action):

 	def name(self) -> Text:
 		return "action_chequear_oferta"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		edad = tracker.get_slot("edad")
 		genero = tracker.get_slot("genero")
 		es_cliente_habitual = tracker.get_slot("es_cliente_habitual")
 		categorias_de_interes = tracker.get_slot("categorias_de_interes")

 		categorias = prolog.consultar('categorias(Categorias).')[0]['Categorias']
 		promociones = prolog.consultar('promocion(Id, Categoria_Oferta, Descripcion, Banner).')

 		publicadas = []
 		for prom in promociones:

 			prediccion = hacer_prediccion_recomendacion(
					edad,
					genero,
					es_cliente_habitual,
					categorias_de_interes,
					categorias,
					prom['Categoria_Oferta'],
					prolog.consultar(f'oferta_limitada({prom["Id"]})')
			)
	 		if prediccion == 1:
	 			dispatcher.utter_message(f"OFERTA! {prom['Descripcion']} en la categoria de {prom['Categoria_Oferta']}")
	 			dispatcher.utter_message(prom['Banner'])
	 			publicadas.append(prom)
	 	
	 	if not publicadas:
	 		dispatcher.utter_message('No hay ninguna oferta disponible para tí por el momento.')

	 	return []