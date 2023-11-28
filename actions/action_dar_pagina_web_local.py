from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog

class ActionDarPaginaWeb(Action):

 	def name(self) -> Text:
 		return "action_dar_pagina_web_local"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		local = tracker.get_slot("local")
 		local = local.lower() if local else None
 		consulta = f'pagina_web("{local}", Link).'
 		link = prolog.consultar(consulta)
 		

 		if not link:
 			dispatcher.utter_message("No pude identificar a que local te estas refiriendo, ¿Puedes decirlo de otra manera?")
 			return []

 		dispatcher.utter_message(f"El link a la página web del local {local} es {link[0]['Link']}\n")
 		return []


