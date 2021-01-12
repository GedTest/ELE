from Components import Resistor, Diode, PowerSupply, Switch

def load_scheme(task,components):
    if components != None:
        components.clear()

    for key in task:
        if key["type"] == "Diode":
            components.append(Diode(key["name"], key["value"], key["left"],
                                    key["top"], key["radius"], key["is_invisible"], key["is_choosable"]))
        if key["type"] == "Resistor":
            components.append(Resistor(key["name"], key["value"], key["left"],
                                    key["top"], key["is_vertical"], key["is_invisible"], key["is_choosable"]))
        if key["type"] == "Switch":
            components.append(Switch(key["name"], key["left"], key["top"], key["radius"],
                                    key["mode_on"], key["is_invisible"], key["is_choosable"]))
        if key["type"] == "PowerSupply":
            components.append(PowerSupply(key["name"], key["value"], key["left"], key["top"],  key["is_invisible"], key["is_choosable"]))


"""
with open("data_build_circuit.json", "r") as components_file:
    data = json.load(components_file)

components = []
for key in data.keys():
    if key != "level_answer":
        if data[key]["type"] == "Diode":
            components.append(Diode(data[key]["name"], data[key]["value"], data[key]["left"],
                                    data[key]["top"], data[key]["radius"]))
        if data[key]["type"] == "Resistor":
            components.append(Resistor(data[key]["name"], data[key]["value"], data[key]["left"],
                                    data[key]["top"], data[key]["is_vertical"], data[key]["is_invisible"]))
        if data[key]["type"] == "Switch":
            components.append(Switch(data[key]["name"], data[key]["left"], data[key]["top"], data[key]["radius"],
                                    data[key]["mode_on"]))
        if data[key]["type"] == "PowerSupply":
            components.append(PowerSupply(data[key]["name"], data[key]["value"], data[key]["left"], data[key]["top"]))
    else:
        level_answer = data[key]
"""        