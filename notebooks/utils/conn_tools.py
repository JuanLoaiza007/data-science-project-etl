import yaml


def readConfig(configFile: str) -> dict:
    """
    Función para leer el archivo de configuración

    Args:
        configFile (str): Ruta al archivo de configuración

    Returns:
        dict: Configuración del archivo de configuración
    """
    with open(configFile, "r") as file:
        return yaml.safe_load(file)


def generateConnUrl(config: dict) -> str:
    """
    Función para generar la url de conexión a la base de datos
    usando la configuración

    Args:
        config (dict): Configuración del archivo de configuración

    Returns:
        str: Url de conexión a la base de datos
    """

    dialect = config["dialect"]
    username = config["username"]
    password = config["password"]
    host = config["host"]
    port = config["port"]
    database = config["database"]

    return f"{dialect}://{username}:{password}@{host}:{port}/{database}"
