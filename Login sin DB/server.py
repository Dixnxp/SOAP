from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase 
from spyne.model.primitive import String, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import logging

# Configuración de logging (opcional)
logging.basicConfig(level=logging.INFO)
logging.getLogger('spyne.server.wsgi').setLevel(logging.DEBUG)

# --- SERVICIO ÚNICO: SIMULACIÓN DE LOGIN ---
class LoginService(ServiceBase): 
    """Servicio Web SOAP para simular un proceso de LOGIN."""
    
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "password123"

    # CORRECCIÓN: Quitamos 'ctx' para que coincida con los 2 'String' del decorador
    @srpc(String, String, _returns=Boolean)
    def validate_user(username, password): 
        """Valida un usuario y contraseña simulados."""
        
        if username == LoginService.VALID_USERNAME and password == LoginService.VALID_PASSWORD:
            print(f"LOGIN: Éxito para el usuario {username}")
            return True
        else:
            print(f"LOGIN: Fallido para el usuario {username}")
            return False

# Inicialización de la aplicación Spyne
application = Application([LoginService],
    tns='urn:servicio-login-spyne', 
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Configuración y ejecución del servidor
if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    host = '127.0.0.1'
    port = 8000
    server = make_server(host, port, wsgi_app)
    
    print("-" * 50)
    print(f"✅ SERVIDOR SOAP DE LOGIN INICIADO")
    print(f"   URL: http://{host}:{port}")
    print(f"   WSDL: http://{host}:{port}/?wsdl")
    print("-" * 50)
    
    server.serve_forever()



    ## EJEMPLO DE PETICIÓN SOAP ##
  #     <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="urn:servicio-login-spyne">
  #    <soap:Body>
  #          <tns:validate_user>
  #              <tns:username>admin</tns:username>
  #              <tns:password>password123</tns:password>
  #          </tns:validate_user>
  #      </soap:Body>
  #      </soap:Envelope>
    