DATA_D2 = {
"R51669e3825": r"""
def __init__(self):
    defaults = {
        "secondsRemaining": 10.0,
        "lastTick": 0,
        "isPaused": False,
        "isRunning": False,
        "keepGoing": True,
    }
    for name, value in defaults.items():
        setattr(self, name, value)
""",
"R3713a963cf": r"""
def json_scan(json_obj, key):
    result = None
    for element in json_obj:
        if str(element) == key:
            result = json_obj[element]
        else:
            value = json_obj[element]
            if type(value) == DictType:
                result = json_scan(value, key)
            elif type(value) == ListType:
                result = json_scan(element, key)
    return result
"""
}
