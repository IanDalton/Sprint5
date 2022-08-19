import json
from funciones_generadas import validador_TPS as verificador


class Cliente:
    def __init__(self,json):
        if json["tipo"] == "CLASSIC":
            self.tipo = self.Classic()
        elif json["tipo"] == "GOLD":
            self.tipo = self.Gold()
        elif json["tipo"] == "BLACK":
            self.tipo = self.Black()

    class Classic():
        def limites(self): return 10000,150000,0.01,0,0,0    # Max ret diario, Max trans, Comision, Descubierto, Max Chequeras, Max Credito
        def puede_crear_chequera(self): return True
        def puede_crear_tarjeta_credito(self): return False
        def puede_comprar_dolar(self): return False

    class Gold():
        def limites(self): return 20000,500000,0,10000,1,1   # Max ret diario, Max trans, Comision, Descubierto, Max Chequeras, Max Credito
        def puede_crear_chequera(self): return True
        def puede_crear_tarjeta_credito(self): return True
        def puede_comprar_dolar(self): return True

    class Black():
        def limites(self): return 10000,500000,0.01,10000,2,5    # Max ret diario, Max trans, Comision, Descubierto, Max Chequeras, Max Credito
        def puede_crear_chequera(self): return True
        def puede_crear_tarjeta_credito(self): return True
        def puede_comprar_dolar(self): return True


def RazonRetiroEfectivo(json,usuario):
    if json["monto"] > json["cupoDiarioRestante"]:
        json["razon"] = "El monto excede al limite permitido"


def RazonAltaTarjetaCredito(json,usuario):
    if json["totalTarjetasDeCreditoActualmente"] >= usuario.tipo.limites()[5]:
        json["razon"] = f"Excede el limite de {usuario.tipo.limites()[5]}"


def RazonAltaChequera(json,usuario):
    if json["totalChequerasActualmente"] >= usuario.tipo.limites()[4]:
        json["razon"] = f"Excede el limite de {usuario.tipo.limites()[4]}"


def RazonCompraDolar(json,usuario):
    if not usuario.tipo.puede_comprar_dolar():
        json["razon"] = "El usuario no puede comprar dolares"
    elif json["monto"] > json["cupoDiarioRestante"]:
        json["razon"] = "El monto excede al limite permitido"


def RazonTransferenciaEnviada(json,usuario):
    if json["monto"] > json["cupoDiarioRestante"]:
        json["razon"] = "El monto excede al limite permitido"


def RazonTransferenciaRecibida(json,usuario):
    if json["monto"] > json["cupoDiarioRestante"]:
        json["razon"] = "El monto excede al limite permitido"


def generar_json(archivo):
    with open(archivo) as f:
        datos = json.load(f)
    errores = verificador(datos)
    if errores:
        print("El archivo enviado esta mal formulado")
        return errores
    usuario = Cliente(datos)
    for trans in datos["transacciones"]:
        if trans["estado"] == "RECHAZADA":
            if trans["tipo"] == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                RazonRetiroEfectivo(trans,usuario)
            elif trans["tipo"] == "ALTA_TARJETA_CREDITO":
                RazonAltaTarjetaCredito(trans,usuario)
            elif trans["tipo"] == "ALTA_CHEQUERA":
                RazonAltaChequera(trans,usuario)
            elif trans["tipo"] == "COMPRA_DOLAR":
                RazonCompraDolar(trans,usuario)
            elif trans["tipo"] == "TRANSFERENCIA_ENVIADA":
                RazonTransferenciaEnviada(trans,usuario)
            elif trans["tipo"] == "TRANSFERENCIA_RECIBIDA":
                RazonTransferenciaRecibida(trans,usuario)
            else:
                print(trans["tipo"])
    
    return datos

