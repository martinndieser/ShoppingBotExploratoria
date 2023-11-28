from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog


class ActionDarUbicacionDeLocal(Action):

 	def name(self) -> Text:
 		return "action_dar_ubicacion_de_local"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		local = tracker.get_slot("local")
 		if not local:
 			respuesta = "No pude identificar a lo que te estas refiriendo, ¿Puedes decirlo de otra manera?"
 			dispatcher.utter_message(respuesta)
 			return []
 		
 		local = local.lower()
 		consulta = f'nivel("{local}", Nivel).'
 		#print(prolog.consultar(consulta))
 		nivel = prolog.consultar(consulta)
 		
 		respuesta = ( 
			    f"{local} se encuentra en {nivel[0]['Nivel']} del shopping\n"
			) if nivel else f"No tengo información de donde se encuentra el local {local}\n"

 		dispatcher.utter_message(respuesta)
 		return []



