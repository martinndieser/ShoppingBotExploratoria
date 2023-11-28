from .prolog import prolog
from tensorflow import keras
import joblib
import numpy as np

from sklearn.preprocessing import LabelEncoder

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

path_experiencias = "C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\actions\\modelo recomendaciones"
model = keras.models.load_model(f'{path_experiencias}\\model.h5')

label_encoder_local = joblib.load(f'{path_experiencias}\\label_encoder_local.pkl')
label_encoder_producto = joblib.load(f'{path_experiencias}\\label_encoder_producto.pkl')



class ActionEsRecomendable(Action):

 	def name(self) -> Text:
 		return "action_es_recomendable"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		producto = tracker.get_slot("producto")
 		local = tracker.get_slot("local")

 		if not (producto and local):
 			dispatcher.utter_message("No pude identificar a lo que te estas refiriendo, ¿Puedes decirlo de otra manera?")
 			return []

 		producto = producto.lower()
 		local = local.lower()

 		# preguntamos la categoria del local
 		# para asi evaluar si el mismo vende el producto por el cual nos esta preguntando
 		categoria = prolog.consultar(f'local("{local}", Categoria).')
 		if (not categoria):
 			dispatcher.utter_message("El local que ingresaste no es un local válido ó se escribe de otra manera.")
 			return []

 		# chequeamos que la categoria del producto sea la indicada
 		categoria_indicada = prolog.consultar(f'producto("{producto}", Categoria).')

 		if (not categoria_indicada):
 			dispatcher.utter_message('El producto por el que estas preguntando no existe.')
 			return []

 		if (categoria_indicada[0]['Categoria'] != categoria):
 			dispatcher.utter_message(f"El producto por el que estas preguntando no corresponde a la categoria de productos disponibles en la que trabaja el local {local}")
 			return []
 		
 		producto_encoded = label_encoder_producto.transform([producto])
 		local_encoded = label_encoder_local.transform([local])

 		sample = np.array([[[producto_encoded][0], [local_encoded][0]]])
 		prediction = model.predict(sample)
 		
 		if prediction == 0.5:
 			dispatcher.utter_message("No es una buena, ni mala elección.")
 		elif prediction > 0.5:
 			dispatcher.utter_message(f"De acuerdo a clientes anteriores la compra de {producto} en {local} que buscas hacer es una buena elección")
 		else:
 			dispatcher.utter_message(f"De acuerdo a clientes anteriores la compra de {producto} en {local} que buscas hacer no es una muy buena elección")

 		return []

