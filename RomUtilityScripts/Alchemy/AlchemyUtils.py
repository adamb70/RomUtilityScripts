def build_stats(effects):
    stats = {}
    if type(effects) == str:
        # Only list of effect names, use default val and time
        effects = [(eff, 5, 30) for eff in effects]

    for eff, val, time in effects:
        if "Health" in eff:
            stat = "Health"
        elif "Stamina" in eff:
            stat = "Stamina"
        elif "Food" in eff:
            stat = "Food"
        elif "Thirst" in eff:
            stat = "Thirst"
        elif "Poison" in eff:
            stat = "Poison"
        elif "Mood" in eff:
            stat = "Mood"
        elif "Fury" in eff:
            stat = "Fury"
        else:
            continue
        try:
            val = int(val)
        except ValueError:  # val can not be converted to int, so set a default
            val = 12345

        if eff.startswith("Anti"):
            val = -int(val)
        stats[stat] = (int(val), time)
    return stats
