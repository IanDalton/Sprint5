import json
from funciones_generadas import verificador_de_archivos as verificador
from jinja2 import Environment, PackageLoader, select_autoescape


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
            self.limite_extraccion_diario_restante = self.limite_extraccion_diario
            self.limite_transferencia_recibida = datos.limites()[1]
            self.limite_trans_restante = self.limite_transferencia_recibida
            self.saldo_en_cuenta = 0.0
            self.costo_transferencias = datos.limites()[2]
            self.saldo_descubierto_disponible = datos.limites()[3]
            self.limite_chequeras = datos.limites()[4]
            self.limite_chequeras_restante = self.limite_chequeras
            self.limite_creditos = datos.limites()[5]
            self.limite_creditos_restante = self.limite_creditos
            self.movimientos = []
            self.tarjetas = 0
            self.chequeras = 0

        def movimientos_de_cuenta(self,trans):
            self.saldo_en_cuenta = trans["saldoEnCuenta"]
            self.tarjetas = trans["totalTarjetasDeCreditoActualmente"]
            self.chequeras = trans["totalChequerasActualmente"]
            self.saldo_en_cuenta = trans["saldoEnCuenta"]
            self.limite_creditos_restante = self.limite_creditos - trans["totalTarjetasDeCreditoActualmente"]
            self.limite_chequeras_restante = self.limite_chequeras - trans["totalChequerasActualmente"]

            if trans["tipo"] == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                self.movimientos.append(self.RazonRetiroEfectivo(trans))
                self.limite_extraccion_diario_restante = trans["cupoDiarioRestante"]
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
                if trans["estado"] == "ACEPTADA":
                    self.limite_trans_restante -= trans["monto"]

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


def generar_clase(archivo):
    with open(archivo) as f:
        datos = json.load(f)
    errores = verificador(datos)
    if len(errores) > 0:
        print("Los siguientes elementos estan mal escritos o faltan en el archivo enviado",errores)
        return errores
    usuario = Cliente(datos)
    return usuario


with open("eventos_black.json") as f: 
    datos = json.load(f)
env = Environment(loader=PackageLoader("paquete"), autoescape=select_autoescape())
template = env.get_template("template.html")
with open("reporte.html", "w") as f:
    f.write(template.render(tps=datos))

