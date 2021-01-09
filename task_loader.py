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
