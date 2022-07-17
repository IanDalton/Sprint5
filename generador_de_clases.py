import json


class Cliente():
    def __init__(self, json):
        self.nombre = json["nombre"]
        self.apellido = json["apellido"]
        self.numero = json["numero"]
        self.dni = json["dni"]
        self.direccion = self.Direccion(json["direccion"])
        if json["tipo"] == "CLASSIC":
            self.tipo = self.Classic()
        elif json["tipo"] == "GOLD":
            self.tipo = self.Gold()
        elif json["tipo"] == "BLACK":
            self.tipo = self.Black()

        self.razon = self.Razon(self.tipo)
        for transaccion in json["transacciones"]:
            self.razon.movimientos_de_cuenta(transaccion)

    class Direccion():
        def __init__(self, json):
            self.calle = json["calle"]
            self.numero = json["numero"]
            self.ciudad = json["ciudad"]
            self.provincia = json["provincia"]
            self.pais = json["pais"]

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

    class Razon():
        def __init__(self, datos):
            self.limite_extraccion_diario = datos.limites()[0]
            self.limite_transferencia_recibida = datos.limites()[1]
            self.saldo_en_cuenta = 0.0
            self.costo_transferencias = datos.limites()[2]
            self.saldo_descubierto_disponible = datos.limites()[3]
            self.limite_chequeras = datos.limites()[4]
            self.limite_creditos = datos.limites()[5]
            self.movimientos = []
            self.tarjetas = 0
            self.chequeras = 0

        def movimientos_de_cuenta(self,trans):
            self.saldo_en_cuenta = trans["saldoEnCuenta"]
            self.tarjetas = trans["totalTarjetasDeCreditoActualmente"]
            self.chequeras = trans["totalChequerasActualmente"]
            self.saldo_en_cuenta = trans["saldoEnCuenta"]

            if trans["tipo"] == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                self.movimientos.append(self.RazonRetiroEfectivo(trans))
                self.limite_extraccion_diario = trans["cupoDiarioRestante"]
            elif trans["tipo"] == "ALTA_TARJETA_CREDITO":
                self.movimientos.append(self.RazonAltaTarjetaCredito(trans))
            elif trans["tipo"] == "ALTA_CHEQUERA":
                self.movimientos.append(self.RazonAltaChequera(trans))
            elif trans["tipo"] == "COMPRAR_DOLAR":
                self.movimientos.append(self.RazonCompraDolar(trans))
            elif trans["tipo"] == "TRANSFERENCIA_ENVIADA":
                self.movimientos.append(self.RazonTransferenciaEnviada(trans))
            elif trans["tipo"] == "TRANSFERENCIA_RECIBIDA":
                self.movimientos.append(self.RazonTransferenciaRecibida(trans))
                self.limite_transferencia_recibida -= trans["monto"]

        class RazonAltaChequera():
            def __init__(self, trans):
                self.estado = trans["estado"]
                self.cuenta_nro = trans["cuentaNumero"]
                self.fecha = trans["fecha"]

        class RazonAltaTarjetaCredito():
            def __init__(self, trans):
                self.estado = trans["estado"]
                self.cuenta_nro = trans["cuentaNumero"]
                self.fecha = trans["fecha"]

        class RazonCompraDolar():
            def __init__(self, trans):
                self.estado = trans["estado"]
                self.cuenta_nro = trans["cuentaNumero"]
                self.monto = trans["monto"]
                self.fecha = trans["fecha"]

        class RazonRetiroEfectivo():
            def __init__(self, trans):
                self.estado = trans["estado"]
                self.cuenta_nro = trans["cuentaNumero"]
                self.monto = trans["monto"]
                self.fecha = trans["fecha"]

        class RazonTransferenciaEnviada():
            def __init__(self, trans):
                self.estado = trans["estado"]
                self.cuenta_nro = trans["cuentaNumero"]
                self.monto = trans["monto"]
                self.fecha = trans["fecha"]

        class RazonTransferenciaRecibida():
            def __init__(self, trans):
                self.estado = trans["estado"]
                self.cuenta_nro = trans["cuentaNumero"]
                self.monto = trans["monto"]
                self.fecha = trans["fecha"]


archivo = "eventos_black.json"
with open(archivo) as f:
    datos = json.load(f)
usuario = Cliente(datos)

print(usuario.razon.limite_creditos)
