import sqlite3

conn = sqlite3.connect("empresa_simple.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS departamento(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT
    )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS empleado(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    salario REAL,
    departamento_id INTEGER,
    FOREIGN KEY (departamento_id) REFERENCES departamento (id)
    )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS proyecto(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    departamento_id INTEGER,
    FOREIGN KEY (departamento_id) REFERENCES departamento (id)
    )
''')

conn.commit()

cursor.executemany('''
INSERT INTO departamento (nombre) VALUES (?)
''', [("Recursos Humanos",), ("Marketing",), ("Aerodinamica",)
])

cursor.executemany('''
INSERT INTO empleado (nombre, salario, departamento_id) VALUES (?, ?, ?)
''', [
    ("Gabriel Ojeda", 100000, 1),
    ("Ana Silva", 60000, 2),
    ("Luis Torres", 55000, 3),
    ("Luciano Alamino", 50000, 3),
])

cursor.executemany('''
INSERT INTO proyecto (nombre, departamento_id) VALUES (?, ?)
''', [
    ("Proyecto A", 1),
    ("Proyecto B", 2),
    ("Proyecto C", 3)
])


#1
cursor.execute('''
SELECT nombre FROM empleado WHERE salario > (
    SELECT AVG(salario) FROM empleado
);
''')
print("Empleados que cobran mas que el salario promedio: ")
for fila in cursor.fetchall():
    print(fila)

#2
cursor.execute('''
SELECT nombre
FROM empleado
WHERE departamento_id = (
    SELECT departamento_id
    FROM empleado
    WHERE nombre = 'Luis Torres'
)
AND nombre <> 'Luis Torres'
''')

print("Compitas de luisillo el pillo: ")
for fila in cursor.fetchall():
    print(fila)

#3
cursor.execute('''
SELECT nombre
FROM empleado
WHERE departamento_id IS NULL;
''')
print("Empleados al re pedo: ")
for fila in cursor.fetchall():
    print(fila)


#4
cursor.execute('''
SELECT d.nombre AS departamento, e.nombre AS empleado, e.salario
FROM departamento d
JOIN empleado e ON d.id = e.departamento_id
WHERE e.salario > (
    SELECT AVG(salario) FROM empleado
)
''')

print("\nDepartamentos y empleados con salario superior al promedio general:")
for fila in cursor.fetchall():
    print(f"Departamento: {fila[0]} - Empleado: {fila[1]} - Salario: ${fila[2]:,.2f}")


#5
cursor.execute('''
SELECT e.nombre, d.nombre AS departamento, e.salario
FROM empleado e
JOIN departamento d ON e.departamento_id = d.id
WHERE e.salario = (
    SELECT MAX(salario)
    FROM empleado
    WHERE departamento_id = e.departamento_id
)
''')

print("\nEmpleado con mayor salario en cada departamento:")
for fila in cursor.fetchall():
    print(f"Empleado: {fila[0]} - Departamento: {fila[1]} - Salario: ${fila[2]:,.2f}")


#6
cursor.execute('''
SELECT e.nombre, e.salario, d.nombre AS departamento, p.nombre AS proyecto
FROM empleado e
JOIN departamento d ON e.departamento_id = d.id
JOIN proyecto p ON d.id = p.departamento_id
WHERE e.salario > (
    SELECT AVG(salario) FROM empleado
)
''')

print("Empleados que cobran más que el promedio global y están en proyectos: ")
for fila in cursor.fetchall():
    print(f"Empleado: {fila[0]} - Salario: ${fila[1]:,.2f} - Departamento: {fila[2]} - Proyecto: {fila[3]}")


#7
cursor.execute('''
SELECT p.nombre
FROM proyecto p
JOIN departamento d ON p.departamento_id = d.id
JOIN empleado e ON e.departamento_id = d.id
WHERE e.salario = (SELECT MAX(salario) FROM empleado)
''')
print("Proyecto con el empleado con el mayor salario: ")
for fila in cursor.fetchall():
    print(fila)

#8
cursor.execute('''
UPDATE empleado SET salario =  salario * 1.1
WHERE salario < (
    SELECT AVG(salario) FROM empleado
);
''')


#9
cursor.execute('''
DELETE FROM proyecto
WHERE departamento_id IN (
    SELECT departamento_id
    FROM empleado
    WHERE salario < (SELECT AVG(salario) FROM empleado)
);
''')