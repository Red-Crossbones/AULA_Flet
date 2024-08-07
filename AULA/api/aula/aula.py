import psycopg2


class Aula():
    def __init__(self, conn: psycopg2.connect):
        self.conn: psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_aulas(self):
        self.cursor.execute('SELECT * FROM aula')
        columns = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": columns,
            "rows": rows
        }
        return data
    
    def get_aulas_edificios(self):
        self.cursor.execute('select au.id_aula, ed.nombre, au.nombre from aula au inner join edificio ed on (ed.id = au.id_edificio)')
        columns = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": columns,
            "rows": rows
        }
        return data

    def get_aula(self, id):
        self.cursor.callproc("get_aula", [id])
        columns = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": columns,
            "rows": rows
        }
        return data
    
    def get_aula_edificio(self, id):
        self.cursor.callproc("get_aula_edificio", [id])
        columns = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": columns,
            "rows": rows
        }
        return data

    def insert_aula(self, edificio, nombre, capacidad):
        self.cursor.callproc("insert_aula", [edificio, nombre, capacidad])
        self.conn.commit()

    def update_aula(self, id, nombre=None, edificio=None, capacidad=None):
        try:
            self.cursor.callproc(
                "update_aula", [id, nombre, edificio, capacidad])
            self.conn.commit()
        except Exception as e:
            print(f"Error al actualizar aula: {e}")
            self.conn.rollback()

    def delete_aula(self, id):
        try:
            self.cursor.callproc("delete_aula", [id])
            self.conn.commit()
        except Exception as e:
            print(f"Error al eliminar aula: {e}")
            self.conn.rollback()
