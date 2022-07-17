def verificador_de_archivos(json):
    variables = ["numero","nombre","apellido","dni","tipo","transacciones","direccion"]
    dir = ["calle","numero","ciudad","provincia","pais"]
    tipos = ["RETIRO_EFECTIVO_CAJERO_AUTOMATICO","ALTA_TARJETA_CREDITO","ALTA_CHEQUERA","COMPRAR_DOLAR","TRANSFERENCIA_ENVIADA","TRANSFERENCIA_RECIBIDA"]
    for item in json:
        for i in range(len(variables)):  # Hago el ciclo hasta que encuentre uno igual, lo elimino de la lista y vuelvo a empezar
            if item == variables[i]:
                variables.pop(i)
                break
        if item == "direccion":
            for datos in json[item]:
                for i in range(len(dir)):  # Hago el ciclo hasta que encuentre uno igual, lo elimino de la lista y vuelvo a empezar
                    if datos == dir[i]:
                        dir.pop(i)
                        break
        if item == "transacciones":
            for i in range(len(json[item])):
                trans = ["estado","totalChequerasActualmente","totalTarjetasDeCreditoActualmente","tipo","cuentaNumero","cupoDiarioRestante","numero","saldoEnCuenta","monto","fecha"]
                for datos in json[item][i]:
                    for i in range(len(trans)):
                        if datos == trans[i]:
                            trans.pop(i)
                            break
                    if (datos == "tipo") and (json[item][i][datos] not in tipos) :
                        return ["No existe",json[item][i][datos]]
                if len(trans) > 0:
                    return [item,i,trans]

    if len(variables) > 0 :
        return variables
    elif len(dir) > 0 :
        return dir
    else:
        return []
