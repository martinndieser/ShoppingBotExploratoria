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



class ActionMejoresLocalesParaProducto(Action):

 	def name(self) -> Text:
 		return "action_dar_mejores_locales_para_determinado_producto"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		producto = tracker.get_slot("producto")

 		if not producto:
 			dispatcher.utter_message("No pude identificar al producto que te estas refiriendo, ¿Puedes decirlo de otra manera?")
 			return []

 		producto = producto.lower()

 		# preguntamos la categoria del local
 		# para asi evaluar si el mismo vende el producto por el cual nos esta preguntando
 		categoria = prolog.consultar(f'producto("{producto}",Categoria).')

 		if (not categoria):
 			dispatcher.utter_message("El producto que ingresaste no se encuentra registrado en el sistema como lo escribiste")
 			return []

 		locales = prolog.consultar(f'local(Local,"{categoria[0]["Categoria"]}").')
 		if not locales:
 			dispatcher.utter_message("El producto que ingresaste no es vendido por ningún local actualmente")
 			return [] 			


 		predictions = {} 

 		for local in locales:
 			local = local['Local']
 			producto_encoded = label_encoder_producto.transform([producto])
 			local_encoded = label_encoder_local.transform([local])
 			sample = np.array([[[producto_encoded][0], [local_encoded][0]]])
 			prediction = model.predict(sample)
 			predictions.update({prediction[0][0]: local})
 		
 		respuesta = f"Para comprar el {producto}, los locales que tienen las mejores calificaciones de acuerdo a pasados clientes son:\n"
 		predictions_keys = list(predictions.keys())
 		# lo ordenamos descendientemente
 		predictions_keys.sort(reverse=True)
 		for pred_key in predictions_keys:
 			respuesta += "- " + predictions[pred_key] + "\n"

 		dispatcher.utter_message(respuesta)

 		return []