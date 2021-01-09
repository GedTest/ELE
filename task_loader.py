from components import Resistor, Diode, PowerSupply, Switch


def load_scheme(task, all_components):
    if all_components is not None:
        all_components.clear()

    for key in task:
        if "level_answer" in key:
            print(key["level_answer"])
            return key["level_answer"]

        if key["type"] == "Diode":
            all_components.append(Diode(key["name"], key["value"], key["left"],
                                        key["top"], key["radius"]))
        if key["type"] == "Resistor":
            all_components.append(Resistor(key["name"], key["value"], key["left"],
                                           key["top"], key["is_vertical"], key["is_invisible"]))
        if key["type"] == "Switch":
            all_components.append(Switch(key["name"], key["left"], key["top"], key["radius"],
                                         key["mode_on"]))
        if key["type"] == "PowerSupply":
            all_components.append(PowerSupply(key["name"], key["value"], key["left"], key["top"]))

    return
