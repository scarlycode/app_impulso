CREATE TABLE habitos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

CREATE TABLE registros (
    id SERIAL PRIMARY KEY,
    habito_id INTEGER NOT NULL REFERENCES habitos(id) ON DELETE CASCADE,
    fecha DATE DEFAULT CURRENT_DATE,
    UNIQUE (habito_id, fecha)
);