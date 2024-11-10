--1) En qué meses del año los clientes solicitan más servicios de mensajería
--RealizacionServicioDiario

SELECT 
    fecha.month, 
    COUNT(*) AS cantidad_servicios
FROM
    public.hecho_realizacion_servicio_dia diario
JOIN 
    public.dim_fecha fecha ON diario.key_fecha = fecha.key_fecha
GROUP BY
    fecha.month
ORDER BY
    cantidad_servicios DESC;

--2) Cuáles son los días donde más solicitudes hay.
--RealizacionServicioDiario

SELECT 
    fecha.day_of_week, 
    COUNT(*) AS cantidad_servicios
FROM
    public.hecho_realizacion_servicio_dia diario
JOIN 
    public.dim_fecha fecha ON diario.key_fecha = fecha.key_fecha
GROUP BY
    fecha.day_of_week
ORDER BY
    cantidad_servicios DESC;

--3) A qué hora los mensajeros están más ocupados.
--RealizacionServicioHora

SELECT 
	hora.hour_24,
	SUM(horario.total_at_hour) as cantidad_servicios
FROM
	public.hecho_realizacion_servicio_hora horario
JOIN
	public.dim_hora hora ON horario.key_hora = hora.key_hora
GROUP BY
	hora.hour_24
ORDER BY
	cantidad_servicios DESC;

--4) Número de servicios solicitados por cliente y por mes
--RealizacionServicioDiario

SELECT 
    cliente.key_cliente,
    fecha.month,
    COUNT(*) AS cantidad_servicios
FROM 
    public.hecho_realizacion_servicio_dia servicio
JOIN 
    public.dim_cliente cliente ON servicio.key_cliente = cliente.key_cliente
JOIN 
    public.dim_fecha fecha ON servicio.key_fecha = fecha.key_fecha
GROUP BY 
    cliente.key_cliente,
    fecha.month
ORDER BY 
    cliente.key_cliente,
    fecha.month;

--5) Mensajeros más eficientes (Los que más servicios prestan)
--RealizacionServicioDiario
SELECT
   	accum.key_mensajero, 
    COUNT(*) AS cantidad_servicios
FROM
    public.hecho_servicio_accumulating_snapshot accum
GROUP BY
    accum.key_mensajero
ORDER BY
    cantidad_Servicios DESC;

--6) Cuáles son las sedes que más servicios solicitan por cada cliente.
--   RealizacionServicioDiario     

SELECT 
    cliente.key_cliente,
    ubicacion.key_ubicacion,
    COUNT(*) AS cantidad_servicios
FROM 
    public.hecho_realizacion_servicio_dia servicio
JOIN 
    public.dim_cliente cliente ON servicio.key_cliente = cliente.key_cliente
JOIN 
    public.dim_ubicacion ubicacion ON servicio.key_ubicacion = ubicacion.key_ubicacion
GROUP BY 
    cliente.key_cliente,
    ubicacion.key_ubicacion
ORDER BY 
    cliente.key_cliente,
    ubicacion.key_ubicacion;

--7) Cuál es el tiempo promedio de entrega desde que se solicita el servicio hasta que se cierra el caso.
--    Servicio_Acummulating_Snapshot

SELECT 
    AVG(
        EXTRACT(EPOCH FROM (
            make_timestamp(dim_fecha_closed.year, dim_fecha_closed.month, dim_fecha_closed.day, dim_hora_closed.hour_24, dim_hora_closed.minute, 0) - 
            make_timestamp(dim_fecha_started.year, dim_fecha_started.month, dim_fecha_started.day, dim_hora_started.hour_24, dim_hora_started.minute, 0)
        )) / 3600
    ) AS tiempo_promedio_entrega_horas
FROM 
    public.hecho_servicio_accumulating_snapshot hecho
JOIN 
    public.dim_fecha dim_fecha_started ON hecho.date_started = dim_fecha_started.key_fecha
JOIN 
    public.dim_hora dim_hora_started ON hecho.time_started = dim_hora_started.key_hora
JOIN 
    public.dim_fecha dim_fecha_closed ON hecho.date_closed = dim_fecha_closed.key_fecha
JOIN 
    public.dim_hora dim_hora_closed ON hecho.time_closed = dim_hora_closed.key_hora
WHERE 
    hecho.date_closed IS NOT NULL
    AND hecho.time_closed IS NOT NULL;

--8) Mostrar los tiempos de espera por cada fase del servicio: Iniciado, Con mensajero asignado,
--recogido en origen, Entregado en Destino, Cerrado. En que fase del servicio hay más demoras?
--    Servicio_Acummulating_Snapshot   

SELECT 
    'Iniciado a Asignado' AS fase,
    AVG(time_started_assigned_min) AS tiempo_promedio_minutos
FROM 
    public.hecho_servicio_accumulating_snapshot
UNION ALL
SELECT 
    'Asignado a Recogido' AS fase,
    AVG(time_assigned_collected_min) AS tiempo_promedio_minutos
FROM 
    public.hecho_servicio_accumulating_snapshot
UNION ALL
SELECT 
    'Recogido a Entregado' AS fase,
    AVG(time_collected_delivered_min) AS tiempo_promedio_minutos
FROM 
    public.hecho_servicio_accumulating_snapshot
UNION ALL
SELECT 
    'Entregado a Cerrado' AS fase,
    AVG(time_delivered_closed_min) AS tiempo_promedio_minutos
FROM 
    public.hecho_servicio_accumulating_snapshot
ORDER BY 
    tiempo_promedio_minutos DESC;


--9) Cuáles son las novedades que más se presentan durante la prestación del servicio?
--    NovedadesServicio

SELECT
	novedad.key_novedad,
	COUNT(*) as frecuencia_novedad
FROM
	public.hecho_novedad_servicio novedad
GROUP BY
	novedad.key_novedad
ORDER BY 
	frecuencia_novedad DESC;
