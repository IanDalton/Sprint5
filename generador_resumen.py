from generador_de_clases import generar_clase as cliente
import sys

usuario = cliente(sys.argv[1])

print(usuario.razon.costo_transferencias)
