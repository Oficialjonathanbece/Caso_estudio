import pickle as pkl
#Clases sin heredar 
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.cantidad = 1

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

class Prestamo:
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario

class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
        self.prestamos = []


# Listas de libros, usuarios y préstamos
libros = []
usuarios = []
prestamos = []

def cargar_datos():
    #Global permite una modificacion en variables directamente
    global libros, usuarios, prestamos
    try:
        #carga los datos de la biblioteca
        with open('datos_biblioteca.pkl', 'rb') as f:
            datos = pkl.load(f)
            libros = datos.get('libros', [])
            usuarios = datos.get('usuarios', [])
            prestamos = datos.get('prestamos', [])
            #Excepecion en caso de no existir el archivo
    except FileNotFoundError:
        libros = []
        usuarios = []
        prestamos = []

def guardar_datos():
    datos = {
        'libros': libros,
        'usuarios': usuarios,
        'prestamos': prestamos
    }
    with open('datos_biblioteca.pkl', 'wb') as f:
        pkl.dump(datos, f)

def registrar(nombre):
    #registro de usuarios
    usuarios.append(nombre)
    print(f'Usuario "{nombre}" registrado correctamente.')
    guardar_datos()

def agregar_libro(titulo, autor):
    #ietra sobre cada libro en la lista de libros
    for libro in libros:
        #Verificacion de coincidencia
        if libro['titulo'] == titulo and libro['autor'] == autor:
            #incrementa la cantidad en caso de existir el libro
            libro['cantidad'] += 1
            print(f'El libro "{titulo}" de {autor} ya existe en la lista. Se aumentó la cantidad disponible.')
            guardar_datos()
            return
    nuevo_libro = {'titulo': titulo, 'autor': autor, 'cantidad': 1}
    libros.append(nuevo_libro)
    print(f'Se ha agregado el libro "{titulo}" de {autor} a la lista.')
    guardar_datos()

def mostrar_libros():
    #Busca exitencia de libros 
    if not libros:
        print('La biblioteca está vacía')
        return
    print('Lista de libros en la biblioteca:')
    #Disponibilidad del libro 
    for libro in libros:
        disponibilidad = 'disponible' if libro['cantidad'] > 0 else 'no disponible'
        print(f'- Título: {libro["titulo"]}, Autor: {libro["autor"]}, Disponibilidad: {disponibilidad}')

def prestar_libro(titulo, usuario):
    for libro in libros:
        #verificar el titulo del libro, y busca coincidencia con el que se quiere prestar
        if libro['titulo'] == titulo:
            #busca al menos 1 copia de libro 
            if libro['cantidad'] > 0:
                #verifica si cumple la condicion de estar registrado
                if usuario in usuarios:
                    #Si todas las condiciones son true reduce la cantidad 
                    libro['cantidad'] -= 1
                    #registro de prestamo 
                    prestamos.append({"usuario": usuario, "libro": titulo})
                    print(f'El libro "{titulo}" ha sido prestado a {usuario}.')
                    guardar_datos()
                    return
                else:
                    print(f'El usuario "{usuario}" no está registrado.')
                    return
            else:
                print(f'El libro "{titulo}" no está disponible.')
                return
    print(f'El libro "{titulo}" no existe en la biblioteca.')

def mostrar_usuarios():
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    print("Lista de usuarios registrados:")
    for usuario in usuarios:
        print(f'- {usuario}')

def mostrar_libros_prestados(usuario):
    #verifica si el usuario asociado al prestamo coincide con el usurio insertado 
    libros_prestados = [prestamo["libro"] for prestamo in prestamos if prestamo["usuario"] == usuario]
    #verifica si la lista contiene elementos 
    if libros_prestados:
        print(f"Libros prestados a {usuario}:")
        for libro in libros_prestados:
            print(f"- {libro}")
    else:
        print(f"No hay libros prestados a {usuario}.")

def devolver_libro(titulo, usuario):
    for prestamo in prestamos:
        #verifica el registro del prestamo 
        if prestamo['usuario'] == usuario and prestamo['libro'] == titulo:
            #Se elimina de la lista de prestamos
            prestamos.remove(prestamo)
            for libro in libros:
                #se verifica la coincidencia del titulo del libro en devolucion
                if libro['titulo'] == titulo:
                    libro['cantidad'] += 1
                    print(f'Libro "{titulo}" devuelto por {usuario}.')
                    guardar_datos()
                    return
    print(f'El libro "{titulo}" no está prestado a {usuario}.')

def menu():
    cargar_datos()
    while True:
        print("\n--- Menú de Biblioteca ---")
        print("1. Registrar usuario")
        print("2. Agregar libro")
        print("3. Mostrar libros")
        print("4. Prestar libro")
        print("5. Mostrar usuarios")
        print("6. Mostrar libros prestados")
        print("7. Devolver libro")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del usuario: ")
            registrar(nombre)
        elif opcion == '2':
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            agregar_libro(titulo, autor)
        elif opcion == '3':
            mostrar_libros()
        elif opcion == '4':
            titulo = input("Ingrese el título del libro: ")
            usuario = input("Ingrese el nombre del usuario: ")
            prestar_libro(titulo, usuario)
        elif opcion == '5':
            mostrar_usuarios()
        elif opcion == '6':
            usuario = input("Ingrese el nombre del usuario: ")
            mostrar_libros_prestados(usuario)
        elif opcion == '7':
            titulo = input("Ingrese el título del libro: ")
            usuario = input("Ingrese el nombre del usuario: ")
            devolver_libro(titulo, usuario)
        elif opcion == '8':
            guardar_datos()
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, por favor seleccione una opción del menú.")

if __name__ == "__main__":
    menu()