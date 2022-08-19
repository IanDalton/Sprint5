from generador_de_clases import generar_json as cliente
import sys
import webbrowser
from jinja2 import Environment, PackageLoader, select_autoescape


datos = cliente(sys.argv[1])

if type(datos) == 'dict':
    env = Environment(loader=PackageLoader("paquete"),autoescape=select_autoescape())
    template = env.get_template("template.html")
    with open("reporte.html", "w") as f:
        f.write(template.render(tps=datos))
    webbrowser.open('reporte.html')
