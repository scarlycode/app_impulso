import os
import psycopg2
import psycopg2.extras
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    """Crea y devuelve una nueva conexión a la base de datos."""
    return psycopg2.connect(DATABASE_URL)


# ---------- HÁBITOS ----------

def crear_habito(nombre, descripcion):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO habitos (nombre, descripcion) VALUES (%s, %s)",
        (nombre, descripcion)
    )
    conn.commit()
    cur.close()
    conn.close()


def obtener_habitos():
    """Devuelve todos los hábitos como lista de diccionarios."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM habitos ORDER BY fecha_creacion ASC")
    habitos = cur.fetchall()
    cur.close()
    conn.close()
    return habitos


def eliminar_habito(habito_id):
    """Elimina un hábito. Los registros se borran solos por ON DELETE CASCADE."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM habitos WHERE id = %s", (habito_id,))
    conn.commit()
    cur.close()
    conn.close()


# ---------- REGISTROS ----------

def marcar_habito_hoy(habito_id):
    """
    Inserta un registro para hoy. Si ya existe (mismo día),
    la restricción UNIQUE evita el duplicado silenciosamente.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO registros (habito_id, fecha) VALUES (%s, CURRENT_DATE)",
            (habito_id,)
        )
        conn.commit()
        resultado = True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        resultado = False
    finally:
        cur.close()
        conn.close()
    return resultado


def obtener_fechas_registro(habito_id):
    """Devuelve un set con todas las fechas registradas para un hábito."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT fecha FROM registros WHERE habito_id = %s",
        (habito_id,)
    )
    fechas = {row[0] for row in cur.fetchall()}
    cur.close()
    conn.close()
    return fechas


# ---------- LÓGICA DE RACHA ----------

def calcular_racha(habito_id):
    """
    Calcula la racha actual de días consecutivos hasta hoy.

    Reglas:
    - Si hoy está registrado, se cuenta hoy y se retrocede día por día
      mientras existan registros consecutivos.
    - Si hoy NO está registrado pero ayer sí, la racha sigue viva
      (el usuario aún puede completarla hoy), y se cuenta desde ayer.
    - Si ni hoy ni ayer están registrados, la racha es 0.
    """
    fechas = obtener_fechas_registro(habito_id)
    if not fechas:
        return 0

    hoy = date.today()
    ayer = hoy - timedelta(days=1)

    if hoy in fechas:
        cursor_fecha = hoy
    elif ayer in fechas:
        cursor_fecha = ayer
    else:
        return 0

    racha = 0
    while cursor_fecha in fechas:
        racha += 1
        cursor_fecha -= timedelta(days=1)

    return racha


def obtener_ultimos_7_dias(habito_id):
    """
    Devuelve una lista de 7 diccionarios (del más antiguo al más reciente),
    cada uno con la fecha y si fue cumplido o no.
    """
    fechas = obtener_fechas_registro(habito_id)
    hoy = date.today()

    dias = []
    for i in range(6, -1, -1):
        fecha_dia = hoy - timedelta(days=i)
        dias.append({
            "fecha": fecha_dia,
            "cumplido": fecha_dia in fechas
        })
    return dias