import os
import subprocess
import sys

env_name = "venv"
requirements_file = "requirements.txt"


def main():
    print(
        "\nIniciando instalación y configuración del proyecto.\nEspere por favor...\n"
    )

    check_requirements_file()
    create_virtual_env()
    install_dependencies()
    init_postgres_config()

    print(
        "\n\nProceso completado."
        + "\n\nADVERTENCIAS:\n"
        + "1. Recuerde completar los datos de conexión de las bases de datos en config/"
        + "2. Recuerde activar el entorno virtual desde su editor de código."
        + "\n"
    )


def check_requirements_file():
    if not os.path.exists(requirements_file):
        print(f"El archivo {requirements_file} no existe.\n")
        sys.exit(1)


def create_virtual_env():
    print("Creando entorno virtual...\n")
    subprocess.check_call([sys.executable, "-m", "venv", env_name])


def generate_python_executable():
    return (
        os.path.join(env_name, "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "python")
    )


def install_dependencies():
    python_executable = generate_python_executable()
    python_path = (
        subprocess.check_output(
            [python_executable, "-c", "import sys; print(sys.executable)"]
        )
        .decode()
        .strip()
    )

    print(
        f"Usando: {python_executable}\nRuta completa: {python_path}\nInstalando dependencias de Python desde {requirements_file}...\n"
    )
    subprocess.check_call(
        [
            python_executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
        ],
        stderr=subprocess.STDOUT,
    )
    subprocess.check_call(
        [python_executable, "-m", "pip", "install", "-r", requirements_file],
        stderr=subprocess.STDOUT,
    )


def init_postgres_config():
    repo_url = "https://github.com/JuanLoaiza007/config-postgres-yaml-template.git"
    target_dir = "config"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    try:
        subprocess.check_call(["git", "clone", repo_url, target_dir])
        print(
            f"El archivo de configuración se ha creado en: {os.path.abspath(target_dir)}"
        )
    except subprocess.CalledProcessError as e:
        print(f"Error al clonar el archivo de configuración: {e}")


if __name__ == "__main__":
    main()
