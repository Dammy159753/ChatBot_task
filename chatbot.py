# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from rasa_core.actions import Action
from rasa_core.agent import Agent
#from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)

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
        for i in range(3):
            if time is None:
                dispatcher.utter_message("您需要存几年？")
                return []
            i += 1
            if i == 2:
                dispatcher.utter_message("对不起请重新办理！")

def train_dialogue(domain_file="data/mobile_domain.yml",
                   model_path="projects/dialogue",
                   training_data_file="data/mobile_story.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()])
    
    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data,
        epochs=200,
        batch_size=16,
        augmentation_factor=50,
        validation_split=0.2
    )

    agent.persist(model_path)
    return agent

def train_nlu():
    from rasa_nlu.converters import load_data
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Trainer

    training_data = load_data("data/ccb_nlu_data.json")
    trainer = Trainer(RasaNLUConfig("mobile_nlu_model_config.json"))
    trainer.train(training_data)
    model_directory = trainer.persist("models/", project_name="ivr", fixed_model_name="demo")

    return model_directory

"""
def run_chatbot_online(input_channel=ConsoleInputChannel(),
                      interpreter=RasaNLUInterpreter("projects/ccb_chatbot/ccb_chatbot_demo"),
                      domain_file="data/CCB_domain.yml",
                      training_data_file="data/CCB_story.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=interpreter)

    training_data = agent.load_data(training_data_file)
    agent.train_online(training_data,
                       input_channel='cmdline',
                       batch_size=16,
                       epochs=200,
                       max_training_samples=300)

    return agent
"""

def run(serve_forever=True):
    agent = Agent.load("projects/dialogue",
                       interpreter=RasaNLUInterpreter("projects/ccb_chatbot/ccb_chatbot_demo"))

    #if serve_forever:
    #    agent.handle_channel(ConsoleInputChannel())
    return agent
	
#if __name__ == "__main__":
def main():
    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser(
        description="starts the bot")

    parser.add_argument(
        "task",
        choices=["train-nlu", "train-dialogue", "run", "online_train"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()
    elif task == "online_train":
        run_chatbot_online()
    else:
        warnings.warn("Need to pass either 'train-nlu', 'train-dialogue' or "
                      "'run' to use the script.")
        exit(1)
