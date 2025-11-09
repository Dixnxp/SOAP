from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.primitive import Double
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne import ServiceBase
from spyne import*

from wsgiref.simple_server import make_server
import logging

# Configuración de logging (opcional, ayuda a ver la actividad del servidor)
logging.basicConfig(level=logging.INFO)
logging.getLogger('spyne.server.wsgi').setLevel(logging.DEBUG)

# Definición de la lógica del servicio
class ConversionService(ServiceBase):
    """Servicio Web SOAP para la conversión de temperaturas."""

    # Conversión Celsius a Fahrenheit (C -> F)
    @srpc(Double, _returns=Double)
    def CelsiusToFahrenheit(celsius):
        """Convierte temperatura de Celsius a Fahrenheit."""
        return (celsius * 9/5) + 32

    # Conversión Fahrenheit a Celsius (F -> C)
    @srpc(Double, _returns=Double)
    def FahrenheitToCelsius(fahrenheit):
        """Convierte temperatura de Fahrenheit a Celsius."""
        resultado = (fahrenheit - 32) * 5/9
        return round(resultado, 2)

    # Conversión Fahrenheit a Kelvin (F -> K)
    @srpc(Double, _returns=Double)
    def FahrenheitToKelvin(fahrenheit):
        """Convierte temperatura de Fahrenheit a Kelvin."""
        # Primero a Celsius, luego a Kelvin
        celsius = (fahrenheit - 32) * 5/9
        return celsius + 273.15

# Inicialización de la aplicación Spyne
application = Application([ConversionService],
    #tns='urn:conversion-temp-service',  # Target Namespace (identificador único del servicio)
    tns='urn:SERVICIO_DE_CONVERSION',  # Target Namespace (identificador único del servicio)
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Configuración del servidor WSGI (para ejecutar Spyne)
if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    host = '127.0.0.1'
    port = 8000
    server = make_server(host, port, wsgi_app)
    
    print("-" * 50)
    print(f"SERVIDOR SOAP DE CONVERSIÓN INICIADO :)")
    print(f"   URL: http://{host}:{port}")
    print(f"   WSDL: http://{host}:{port}/?wsdl")
    print("-" * 50)
    
    # Inicia el servidor y espera peticiones
    server.serve_forever()