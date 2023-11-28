from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog

class ActionNombrarLocalesPorCategorias(Action):

 	def name(self) -> Text:
 		return "action_nombrar_locales_en_categoria"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		categoria = tracker.get_slot("categoria")
 		if not categoria:
 			respuesta = "No pude identificar a lo que te estas refiriendo, ¿Puedes decirlo de otra manera?"
 			dispatcher.utter_message(respuesta)
 			return []

 		categoria = categoria.lower()

 		consulta = f'locales_por_categoria("{categoria}", Locales).'
 		locales = prolog.consultar(consulta)
 		respuesta = ( 
			    f"Aca tienes los locales dentro de la categoria de {categoria}: \n" +
			    "\n".join(locales[0]['Locales'])
			) if locales else "No encontré ningún local en esa categoria\n"

 		dispatcher.utter_message(respuesta)
 		return []

