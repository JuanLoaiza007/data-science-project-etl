# Tutorial rápido de manejo de copias de seguridad

> [!WARNING]  
> En esta seccion se encuenta el dump de la base de datos partida en dos archivos .7z. Recuerde extraerlo.

## 1. Crear una copia de seguridad

Utiliza `pg_dump` para generar un backup de la base de datos:

```bash
pg_dump -U <user_name> -W -F <format_name> <database_name> -f <file_name>
```

- **U**: Usuario (ej., postgres)
- **W**: Solicita contraseña
- **F**: Formato del archivo (tar, custom, plain)
- **f**: Nombre del archivo de salida

## 2. Restaurar una copia de seguridad

Utiliza `pg_restore` para restaurar la base de datos:

```bash
pg_restore -U <user_name> -W -d <database_name> --no-owner <file_name>
```

- **--no-owner**: Crea la base de datos sin el propietario original.

> [!WARNING]  
> Para alojar la copia ya debe existir una base de datos vacia en `database_name`, el nombre puede ser cualquiera.

### Ejemplo

```bash
pg_restore -U postgres -W -d rapidos-y-furiosos --no-owner bd-OLTP
```
