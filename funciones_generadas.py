import json
import jsonschema
from jsonschema import validate

with open("main.json") as f:
    main = json.load(f)


with open("transacciones.json") as f:
    transacciones = json.load(f)


def validador_TPS(json):
    if validador_json(json, main):
        for transaccion in json["transacciones"]:
            if not validador_json(transaccion,transacciones):
                return True
        return False
    else:
        return True


def validador_json(json, comparacion):
    try:
        validate(instance=json,schema=comparacion)
    except jsonschema.exceptions.ValidationError:
        return False
    return True

