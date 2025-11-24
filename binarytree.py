#samir andrés quintana verona
#grupo 55
#turbo antioquia
#ingeniería de sistemas
import tkinter as tk
from tkinter import messagebox
import datetime

# ----------------- Clase Nodo -----------------
# Esta clase representa cada caja del árbol donde guardamos un número
class Nodo:
    def __init__(self, valor):
        self.valor = valor  # El número que guardamos
        self.izq = None  # Aquí va el hijo de la izquierda (números menores)
        self.der = None  # Aquí va el hijo de la derecha (números mayores)

# ----------------- Clase Árbol Binario -----------------
# Esta clase es como el "administrador" del árbol, controla todo
class ArbolBinario:
    def __init__(self):
        self.raiz = None  # Empezamos sin ningún nodo el árbol está vacío
        self.max_niveles = 4  # Solo permitims 4 pisos en nuestro árbol

    # Esta función agrega un nuevo número al arbol
    def insertar(self, valor):
        # Primero verificamos que sea un numero entero
        if not isinstance(valor, int):
            raise ValueError("Debe ingresar un número entero.")
        # Si el árbol está vacio, este será el primer nodo
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            # Si ya hay números, buscamos dónde ponerlo
            self._insertar_rec(self.raiz, valor, 1)

    # Esta función busca el lugar correcto para insertar el número
    def _insertar_rec(self, nodo, valor, nivel):
        # Verificamos que no pasemos de 4 niveles de profundidad
        if nivel >= self.max_niveles:
            raise ValueError("No se permite ingresar nodos con más de 4 niveles.")
        # Si el número es menor va a la izquierda
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar_rec(nodo.izq, valor, nivel + 1)
        # Si el número es mayor, va a la derecha
        elif valor > nodo.valor:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar_rec(nodo.der, valor, nivel + 1)
        # Si el número ya existe, no lo agregamos
        else:
            raise ValueError("El nodo ya existe en el árbol.")

    # Esta funci0n busca si un número existe en el árbol
    def buscar(self, valor):
        return self._buscar_rec(self.raiz, valor)

    # Busca el número de forma recursiva (preguntando en cada nodo)
    def _buscar_rec(self, nodo, valor):
        # Si llegamos a un espacio vacío, el número no está
        if nodo is None:
            return False
        # ¡Lo encontramos!
        if nodo.valor == valor:
            return True
        # Seguimos buscando a la izquierda
        elif valor < nodo.valor:
            return self._buscar_rec(nodo.izq, valor)
        # Seguimos buscando a la derecha
        else:
            return self._buscar_rec(nodo.der, valor)

    # Recorrido Preorden: primero la raíz, luego izquierda, luego derecha
    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo:
            resultado.append(str(nodo.valor))  # Primero visitamos el nodo actual
            self._preorden_rec(nodo.izq, resultado)  # Luego el lado izquierdo
            self._preorden_rec(nodo.der, resultado)  # Finalmente el lado derecho

    # Recorrido Inorden: izquierda, raíz, derecha (muestra los números ordenados)
    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo:
            self._inorden_rec(nodo.izq, resultado)  # Primero el lado izquierdo
            resultado.append(str(nodo.valor))  # Luego visitamos el nodo actual
            self._inorden_rec(nodo.der, resultado)  # Finalmente el lado derecho

    # Recorrido Posorden: izquierda, derecha, raíz
    def posorden(self):
        resultado = []
        self._posorden_rec(self.raiz, resultado)
        return resultado

    def _posorden_rec(self, nodo, resultado):
        if nodo:
            self._posorden_rec(nodo.izq, resultado)  # Primero el lado izquierdo
            self._posorden_rec(nodo.der, resultado)  # Luego el lado derecho
            resultado.append(str(nodo.valor))  # Finalmente visitamos el nodo actual

    # Borra todo el árbol, lo deja vacío
    def limpiar(self):
        self.raiz = None


# ----------------- Interfaz Gráfica del Árbol -----------------
# Esta clase crea la ventana donde vemos y controlamos el árbol
class InterfazArbol:
    def __init__(self, master):
        self.master = master  # La ventana principal
        self.master.title("Árbol Binario de Búsqueda")
        self.master.geometry("900x500")  # Tamaño de la ventana
        self.arbol = ArbolBinario()  # Creamos nuestro árbol

        # ------- Frame superior (entrada + botones) -------
        # Aquí ponemos la caja de texto y los botones
        frame_top = tk.Frame(master)
        frame_top.pack(pady=10)

        # Caja donde escribimos el número
        self.entry_valor = tk.Entry(frame_top, width=10)
        self.entry_valor.grid(row=0, column=0, padx=5)

        # Botón para agregar un número al árbol
        btn_agregar = tk.Button(frame_top, text="Agregar Nodo", command=self.agregar_nodo)
        btn_agregar.grid(row=0, column=1, padx=5)

        # Botón para buscar un número en el árbol
        btn_buscar = tk.Button(frame_top, text="Buscar Nodo", command=self.buscar_nodo)
        btn_buscar.grid(row=0, column=2, padx=5)

        # Botón para borrar todo el árbol
        btn_limpiar = tk.Button(frame_top, text="Limpiar", command=self.confirmar_limpiar)
        btn_limpiar.grid(row=0, column=3, padx=5)

        # Botón para cerrar la aplicación
        btn_salir = tk.Button(frame_top, text="Salir", command=self.confirmar_salir)
        btn_salir.grid(row=0, column=4, padx=5)

        # ------- Canvas para el árbol -------
        # Esta es el área blanca donde dibujamos el árbol
        self.canvas = tk.Canvas(master, bg="white", width=850, height=300, relief="solid", borderwidth=1)
        self.canvas.pack(pady=10)

        # ------- Frame inferior (recorridos) -------
        # Aquí mostramos los tres tipos de recorridos del árbol
        frame_bottom = tk.Frame(master)
        frame_bottom.pack()

        # Caja que muestra el recorrido Preorden
        tk.Label(frame_bottom, text="Preorden").grid(row=0, column=0, padx=5)
        self.preorden_txt = tk.Entry(frame_bottom, width=20)
        self.preorden_txt.grid(row=0, column=1, padx=5)

        # Caja que muestra el recorrido Inorden
        tk.Label(frame_bottom, text="Inorden").grid(row=0, column=2, padx=5)
        self.inorden_txt = tk.Entry(frame_bottom, width=20)
        self.inorden_txt.grid(row=0, column=3, padx=5)

        # Caja que muestra el recorrido Posorden
        tk.Label(frame_bottom, text="Posorden").grid(row=0, column=4, padx=5)
        self.posorden_txt = tk.Entry(frame_bottom, width=20)
        self.posorden_txt.grid(row=0, column=5, padx=5)

    # ------- Funciones -------
    # Función que se ejecuta cuando presionamos "Agregar Nodo"
    def agregar_nodo(self):
        try:
            valor = int(self.entry_valor.get())  # Tomamos el número que escribió el usuario
            self.arbol.insertar(valor)  # Lo agregamos al árbol
            self.entry_valor.delete(0, tk.END)  # Borramos la caja de texto
            self.dibujar_arbol()  # Dibujamos el árbol actualizado
            self.actualizar_recorridos()  # Actualizamos los recorridos
        except ValueError as e:
            # Si algo sale mal, mostramos un mensaje de error
            messagebox.showerror("Error", str(e))

    # Función que se ejecuta cuando presionamos "Buscar Nodo"
    def buscar_nodo(self):
        try:
            valor = int(self.entry_valor.get())  # Tomamos el número a buscar
            if self.arbol.buscar(valor):
                # Si lo encontramos, mostramos un mensaje y lo resaltamos
                messagebox.showinfo("Resultado", f"El nodo {valor} SÍ existe en el árbol.")
                self.dibujar_arbol(highlight=valor)
            else:
                # Si no existe, mostramos un mensaje diferente
                messagebox.showinfo("Resultado", f"El nodo {valor} NO existe en el árbol.")
                self.dibujar_arbol()
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero.")

    # Pregunta si realmente queremos borrar todo antes de hacerlo
    def confirmar_limpiar(self):
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar todo el árbol?"):
            self.limpiar()

    # Pregunta si realmente queremos salir antes de cerrar
    def confirmar_salir(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.master.destroy()

    # Borra todo: el árbol y las cajas de texto
    def limpiar(self):
        self.arbol.limpiar()  # Limpiamos el árbol
        self.canvas.delete("all")  # Borramos todo del área de dibujo
        self.preorden_txt.delete(0, tk.END)  # Limpiamos la caja de preorden
        self.inorden_txt.delete(0, tk.END)  # Limpiamos la caja de inorden
        self.posorden_txt.delete(0, tk.END)  # Limpiamos la caja de posorden

    # Dibuja el árbol completo en el canvas
    def dibujar_arbol(self, highlight=None):
        self.canvas.delete("all")  # Primero borramos cualquier dibujo anterior
        if not self.arbol.raiz:
            return  # Si el árbol está vacío, no hay nada que dibujar
        # Comenzamos a dibujar desde la raíz, en el centro superior
        self._dibujar_nodo(self.arbol.raiz, 450, 40, 200, highlight)

    # Dibuja un nodo individual y sus conexiones
    def _dibujar_nodo(self, nodo, x, y, dx, highlight):
        # Si tiene hijo izquierdo, dibujamos la línea y el hijo
        if nodo.izq:
            self.canvas.create_line(x, y, x - dx, y + 60)
            self._dibujar_nodo(nodo.izq, x - dx, y + 60, dx / 2, highlight)
        # Si tiene hijo derecho, dibujamos la línea y el hijo
        if nodo.der:
            self.canvas.create_line(x, y, x + dx, y + 60)
            self._dibujar_nodo(nodo.der, x + dx, y + 60, dx / 2, highlight)

        # Elegimos el color: amarillo si es el nodo buscado, azul si no
        color = "yellow" if highlight == nodo.valor else "#5DADE2"
        borde = "red" if highlight == nodo.valor else "black"

        # Dibujamos el círculo del nodo
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline=borde, width=2)
        # Escribimos el número dentro del círculo
        self.canvas.create_text(x, y, text=str(nodo.valor), font=("Arial", 10, "bold"))

    # Actualiza las cajas de texto con los recorridos del árbol
    def actualizar_recorridos(self):
        # Actualizamos el recorrido Preorden
        self.preorden_txt.delete(0, tk.END)
        self.preorden_txt.insert(0, " - ".join(self.arbol.preorden()))

        # Actualizamos el recorrido Inorden
        self.inorden_txt.delete(0, tk.END)
        self.inorden_txt.insert(0, " - ".join(self.arbol.inorden()))

        # Actualizamos el recorrido Posorden
        self.posorden_txt.delete(0, tk.END)
        self.posorden_txt.insert(0, " - ".join(self.arbol.posorden()))


# ----------------- Ventana de Inicio -----------------
# Esta función crea la primera ventana que vemos, donde pedimos contraseña
def ventana_inicio():
    inicio = tk.Tk()
    inicio.title("Fase4_SamirQuintana")
    inicio.geometry("350x220")
    inicio.resizable(False, False)  # No permitimos cambiar el tamaño

    # Mostramos información de la aplicación
    tk.Label(inicio, text="Aplicación:", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(inicio, text="Árboles Binarios", font=("Arial", 10)).pack()
    tk.Label(inicio, text="Estudiante: Samir Andrés Quintana Verona", font=("Arial", 9)).pack(pady=3)
    # Mostramos la fecha actual
    tk.Label(inicio, text=f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')}", font=("Arial", 9)).pack(pady=3)

    # Pedimos la contraseña
    tk.Label(inicio, text="Contraseña:", font=("Arial", 10)).pack(pady=5)
    password_entry = tk.Entry(inicio, show="*", width=25)  # El "*" oculta lo que escribimos
    password_entry.pack()

    # Función que verifica si la contraseña es correcta
    def verificar_contraseña():
        if password_entry.get() == "UNAD":
            # Si es correcta, cerramos esta ventana y abrimos la del árbol
            inicio.destroy()
            root = tk.Tk()
            InterfazArbol(root)
            root.mainloop()
        else:
            # Si es incorrecta, mostramos un mensaje de error
            messagebox.showerror("Error", "Contraseña incorrecta. Inténtalo de nuevo.")

    # Botón para intentar ingresar
    tk.Button(inicio, text="Ingresar", command=verificar_contraseña, width=10).pack(pady=10)

    inicio.mainloop()  # Mantenemos la ventana abierta


# ----------------- Ejecutar la aplicación -----------------
# Aquí empieza todo: mostramos la ventana de inicio
ventana_inicio()