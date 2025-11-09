from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase 
from spyne.model.primitive import String, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import logging

# --- Dependencias de SQLAlchemy y MySQL ---
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import String as DbString

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('spyne.server.wsgi').setLevel(logging.DEBUG)

# --- CONFIGURACIÓN DE LA BASE DE DATOS MYSQL ---
DB_USER = "root"
DB_PASS = "DIAMONDCHAIR44" # ¡Cámbialo!
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "soap_login_db"

# Cadena de conexión para MySQL con PyMySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

try:
    engine = create_engine(DATABASE_URL)
    # Intenta hacer una conexión de prueba para verificar que el driver y la URL son correctos
    engine.connect()
    print("Conexión con MySQL exitosa.")
except Exception as e:
    print(f"ERROR DE CONEXIÓN A MYSQL: Verifica credenciales y que MySQL esté corriendo.")
    print(e)
    exit() # Sale si no se puede conectar

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definición del Modelo
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(DbString(50), unique=True, nullable=False)
    password = Column(DbString(255), nullable=False)

# --- SERVICIO DE LOGIN ---
class LoginService(ServiceBase): 
    """Servicio Web SOAP para login usando MySQL."""

    @srpc(String, String, _returns=Boolean)
    def validate_user(username, password): 
        """Consulta la base de datos MySQL para validar las credenciales."""
        
        db = SessionLocal() # Abre una nueva sesión de DB
        try:
            # Buscar usuario
            user = db.query(User).filter_by(username=username).first()

            # Validar
            if user and user.password == password:
                print(f"LOGIN DB (MySQL): Éxito para {username}")
                return True
            else:
                print(f"LOGIN DB (MySQL): Fallido para {username}")
                return False
        
        finally:
            db.close() # Cierra la sesión

# Inicialización de la aplicación Spyne
application = Application([LoginService],
    tns='urn:servicio-login-mysql', # Nuevo namespace
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
    print(f"✅ SERVIDOR SOAP DE LOGIN (MYSQL) INICIADO")
    print(f"   WSDL: http://{host}:{port}/?wsdl")
    print("-" * 50)
    
    server.serve_forever()

#    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="urn:servicio-login-mysql">
#   <soap:Body>
#      <tns:validate_user>
#         <tns:username>admin_mysql</tns:username>
#         <tns:password>mysqlpass123</tns:password>
#      </tns:validate_user>
#   </soap:Body>
#</soap:Envelope>