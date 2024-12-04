--1) En qué meses del año los clientes solicitan más servicios de mensajería
--RealizacionServicioDiario
SELECT 
    df.month_name AS mes,   
    SUM(hrs.total_at_day) AS total_servicios
FROM 
    hecho_realizacion_servicio_dia hrs
JOIN 
    dim_fecha df
ON 
    hrs.key_fecha = df.key_fecha
GROUP BY 
    df.month, df.month_name
ORDER BY 
    total_servicios DESC;

--2) Cuáles son los días donde más solicitudes hay.
--RealizacionServicioDiario

SELECT 
	dim_fecha.day_of_week,
	SUM(diario.total_at_day) as total_servicios
FROM
	hecho_realizacion_servicio_dia diario
JOIN 
	dim_fecha
ON 
	diario.key_fecha = dim_fecha.key_fecha
GROUP BY
	dim_fecha.day_of_week
ORDER BY 
	total_servicios DESC;    

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
    dc.name AS cliente,
    df.month_name AS mes,
    SUM(hrs.total_at_day) AS total_servicios
FROM 
    hecho_realizacion_servicio_dia hrs
JOIN 
    dim_cliente dc
ON 
    hrs.key_cliente = dc.key_cliente
JOIN 
    dim_fecha df
ON 
    hrs.key_fecha = df.key_fecha
GROUP BY 
    dc.name, df.month, df.month_name
ORDER BY 
    total_Servicios desc;

--5) Mensajeros más eficientes (Los que más servicios prestan)
--RealizacionServicioDiario
SELECT
	dm.full_name as nombre_mensajero,	
	dm.key_mensajero as key,
    COUNT(*) AS total_servicios
FROM
    public.hecho_servicio_accumulating_snapshot accum
JOIN
	dim_mensajero dm
ON
	accum.key_mensajero = dm.key_mensajero
GROUP BY
    dm.full_name,
	dm.key_mensajero
ORDER BY
    total_Servicios DESC;

--6) Cuáles son las sedes que más servicios solicitan por cada cliente.
--   RealizacionServicioDiario     

SELECT
	dc.name as nombre_cliente,
	dc.key_cliente as key_cliente,
	du.city as ciudad,
	du.department as departamento,
    du.key_ubicacion as key_ubicacion,
    SUM(servicio.total_at_day) AS total_servicios
FROM 
    public.hecho_realizacion_servicio_dia servicio
JOIN 
    public.dim_cliente dc ON servicio.key_cliente = dc.key_cliente
JOIN 
    public.dim_ubicacion du ON servicio.key_ubicacion = du.key_ubicacion
GROUP BY 
	dc.name, dc.key_cliente, du.city, du.department, du.key_ubicacion
ORDER BY 
	nombre cliente, total_servicios desc;

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
    dn.type AS novedad,
    COUNT(hns.key_hecho_novedad_servicio) AS total_ocurrencias
FROM 
    hecho_novedad_servicio hns
JOIN 
    dim_novedad dn
ON 
    hns.key_novedad = dn.key_novedad
GROUP BY 
    dn.type
ORDER BY 
    total_ocurrencias DESC;

