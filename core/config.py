import os
from dotenv import load_dotenv


env_path = os.path.join('' ".env")
load_dotenv(env_path)


class Settings:
    """
        Clase para obtener variables de entorno
        Estas pueden contener informacion sensible y no deben estar contenidas
        en el codigo fuente
    """
   
    ID_SPREADSHEET = os.getenv("ID_SPREADSHEET")
    FILE_SECRET_KEY_GCP = os.getenv("FILE_SECRET_KEY_GCP")
    

settings = Settings()
