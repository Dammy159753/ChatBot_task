from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

support_business = ["存房业务", "存房"]
 
def extract_item(item, dispatcher):
    """
     check if item supported, this func just for lack of train data.
     :param item: item in track, eg: "存房业务", "存房"
     :return:
    """
    if item is None:
        return None
    for name in support_business:
        if name in item:
            return name
        else:
            return name
    return None

class ActionSelect(Action):
    def name(self):
        return 'action_select'

    def run(self, dispatcher, tracker, domain):
        item = tracker.get_slot("item")
        item = extract_item(item)
        if item is None:
            dispatcher.utter_message("您好，我现在只能帮您办理存房业务哦！")
            dispatcher.utter_message("你可以这样问我：“我想办理存房业务”")
            return []

        time = tracker.get_slot("year_number")
        if time is None:
            dispatcher.utter_message("您需要存几年？")
            return []
