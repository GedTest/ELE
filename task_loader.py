from components import Resistor, Diode, PowerSupply, Switch
import json
import pygame
pygame.init()


with open("data_schemes.json", "r") as components_file:
   data = json.load(components_file)

def load_scheme(task,all_components):
    if all_components != None:
        all_components.clear()

    for key in data[task]:
        # make exception for true_false_circuit
        # level that needs level_answer
        if "level_answer" in key:
            continue
        
        if key["type"] == "Diode":
            all_components.append(Diode(key["name"], key["value"], key["left"],
                            key["top"], key["radius"], key["is_invisible"], key["is_choosable"]))
        if key["type"] == "Resistor":
            all_components.append(Resistor(key["name"], key["value"], key["left"],
                                    key["top"], key["is_vertical"], key["is_invisible"], key["is_choosable"]))
        if key["type"] == "Switch":
            all_components.append(Switch(key["name"], key["left"], key["top"], key["radius"],
                                    key["mode_on"], key["is_invisible"], key["is_choosable"]))
        if key["type"] == "PowerSupply":
            all_components.append(PowerSupply(key["name"], key["value"], key["left"], key["top"],  key["is_invisible"], key["is_choosable"]))


def get_level_answer(task):
    for key in data[task]:
        if "level_answer" in key:
            return key["level_answer"]