from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog



class ActionDarNumeroDeTelefono(Action):

 	def name(self) -> Text:
 		return "action_dar_numero_de_telefono"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		local = tracker.get_slot("local")
 		if not local:
 			respuesta = "No pude identificar a lo que te estas refiriendo, ¿Puedes decirlo de otra manera?"
 			dispatcher.utter_message(respuesta)
 			return []
 		
 		local = local.lower()
 		consulta = f'telefono("{local}", Telefono).'
 		telefono = prolog.consultar(consulta)
 		
 		respuesta = ( 
			    f"El telefono de {local} es {telefono[0]['Telefono']}\n"
			) if telefono else f"No encontre ningún teléfono para {local}\n"

 		dispatcher.utter_message(respuesta)
 		return []



