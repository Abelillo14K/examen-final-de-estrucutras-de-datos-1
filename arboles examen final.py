import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx

# clase para los estudiantes donde se maneja un estudiante con ID, nombre, edad y carrera
class Estudiante:
    def __init__(self, id, nombre, edad, carrera):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera


class Nodo:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierdo = None
        self.derecho = None


# se implementa el arbol Binario de Búsqueda (ABB)
class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        if self.raiz is None:
            self.raiz = Nodo(estudiante)
        else:
            self._insertar_recursivo(self.raiz, estudiante)

    def _insertar_recursivo(self, nodo, estudiante):
        if estudiante.id < nodo.estudiante.id:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(estudiante)
            else:
                self._insertar_recursivo(nodo.izquierdo, estudiante)
        elif estudiante.id > nodo.estudiante.id:
            if nodo.derecho is None:
                nodo.derecho = Nodo(estudiante)
            else:
                self._insertar_recursivo(nodo.derecho, estudiante)

    def buscar(self, estudiante_id):
        return self._buscar_recursivo(self.raiz, estudiante_id)

    def _buscar_recursivo(self, nodo, estudiante_id):
        if nodo is None or nodo.estudiante.id == estudiante_id:
            return nodo
        if estudiante_id < nodo.estudiante.id:
            return self._buscar_recursivo(nodo.izquierdo, estudiante_id)
        else:
            return self._buscar_recursivo(nodo.derecho, estudiante_id)

    def eliminar(self, estudiante_id):
        self.raiz = self._eliminar_recursivo(self.raiz, estudiante_id)

    def _eliminar_recursivo(self, nodo, estudiante_id):
        if nodo is None:
            return nodo
        if estudiante_id < nodo.estudiante.id:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, estudiante_id)
        elif estudiante_id > nodo.estudiante.id:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, estudiante_id)
        else:
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            temp = self._min_nodo(nodo.derecho)
            nodo.estudiante = temp.estudiante
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.estudiante.id)
        return nodo

    def _min_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def recorrido_in_order(self):
        estudiantes = []
        self._recorrido_in_order_recursivo(self.raiz, estudiantes)
        return estudiantes

    def _recorrido_in_order_recursivo(self, nodo, estudiantes):
        if nodo:
            self._recorrido_in_order_recursivo(nodo.izquierdo, estudiantes)
            estudiantes.append(nodo.estudiante)
            self._recorrido_in_order_recursivo(nodo.derecho, estudiantes)


# aqui se va a dibujar el arbol
def dibujar_arbol(arbol):
    if arbol.raiz is None:
        return

    G = nx.DiGraph()

    def agregar_aristas(nodo):
        if nodo.izquierdo:
            G.add_edge(nodo.estudiante.id, nodo.izquierdo.estudiante.id)
            agregar_aristas(nodo.izquierdo)
        if nodo.derecho:
            G.add_edge(nodo.estudiante.id, nodo.derecho.estudiante.id)
            agregar_aristas(nodo.derecho)

    agregar_aristas(arbol.raiz)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=False)
    plt.show()


# guardado de estudiantes
def guardar_estudiantes_en_archivo(estudiantes, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for estudiante in estudiantes:
            archivo.write(f"ID: {estudiante.id}, Nombre: {estudiante.nombre}, Edad: {estudiante.edad}, Carrera: {estudiante.carrera}\n")


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Estudiantes - ABB")
        self.abb = ArbolBinarioBusqueda()

        self.lbl_id = tk.Label(root, text="ID")
        self.lbl_id.grid(row=0, column=0)
        self.ent_id = tk.Entry(root)
        self.ent_id.grid(row=0, column=1)

        self.lbl_nombre = tk.Label(root, text="Nombre")
        self.lbl_nombre.grid(row=1, column=0)
        self.ent_nombre = tk.Entry(root)
        self.ent_nombre.grid(row=1, column=1)

        self.lbl_edad = tk.Label(root, text="Edad")
        self.lbl_edad.grid(row=2, column=0)
        self.ent_edad = tk.Entry(root)
        self.ent_edad.grid(row=2, column=1)

        self.lbl_carrera = tk.Label(root, text="Carrera")
        self.lbl_carrera.grid(row=3, column=0)
        self.ent_carrera = tk.Entry(root)
        self.ent_carrera.grid(row=3, column=1)

        self.btn_agregar = tk.Button(root, text="Agregar Estudiante", command=self.agregar_estudiante)
        self.btn_agregar.grid(row=4, column=0, columnspan=2)

        self.btn_buscar = tk.Button(root, text="Buscar Estudiante", command=self.buscar_estudiante)
        self.btn_buscar.grid(row=5, column=0, columnspan=2)

        self.btn_eliminar = tk.Button(root, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        self.btn_eliminar.grid(row=6, column=0, columnspan=2)

        self.btn_listar = tk.Button(root, text="Listar Estudiantes", command=self.listar_estudiantes)
        self.btn_listar.grid(row=7, column=0, columnspan=2)

        self.btn_dibujar = tk.Button(root, text="Dibujar Árbol", command=self.dibujar_arbol)
        self.btn_dibujar.grid(row=8, column=0, columnspan=2)

        self.btn_guardar = tk.Button(root, text="Guardar en Archivo", command=self.guardar_en_archivo)
        self.btn_guardar.grid(row=9, column=0, columnspan=2)

    def agregar_estudiante(self):
        try:
            id = int(self.ent_id.get())
            nombre = self.ent_nombre.get()
            edad = int(self.ent_edad.get())
            carrera = self.ent_carrera.get()
            estudiante = Estudiante(id, nombre, edad, carrera)
            self.abb.insertar(estudiante)
            messagebox.showinfo("Exito", "Estudiante agregado correctamete.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese datos validos.")

    def buscar_estudiante(self):
        try:
            id = int(self.ent_id.get())
            resultado = self.abb.buscar(id)
            if resultado:
                estudiante = resultado.estudiante
                messagebox.showinfo("Estudiante encontrado", f"ID: {estudiante.id}\nNombre: {estudiante.nombre}\nEdad: {estudiante.edad}\nCarrera: {estudiante.carrera}")
            else:
                messagebox.showinfo("No encontrado", "Estudiante no encontrado.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID valido.")

    def eliminar_estudiante(self):
        try:
            id = int(self.ent_id.get())
            self.abb.eliminar(id)
            messagebox.showinfo("Exito", "Estudiante eliminado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID valido.")

    def listar_estudiantes(self):
        estudiantes = self.abb.recorrido_in_order()
        lista = "\n".join([f"ID: {est.id}, Nombre: {est.nombre}, Edad: {est.edad}, Carrera: {est.carrera}" for est in estudiantes])
        messagebox.showinfo("Lista de Estudiantes", lista)

    def dibujar_arbol(self):
        dibujar_arbol(self.abb)

    def guardar_en_archivo(self):
        estudiantes = self.abb.recorrido_in_order()
        guardar_estudiantes_en_archivo(estudiantes, "estudiantes.txt")
        messagebox.showinfo("Exito", "Estudiantes guardados en estudiantes.txt")


if __name__ == "__main__":
    root = tk.Tk()
    interfaz = Interfaz(root)
    root.mainloop()
