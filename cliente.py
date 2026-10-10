import requests

BASE_URL = "http://localhost:5000"

def menu():
    while True:
        print("\n1. Registrarse\n2. Iniciar sesión\n3. Ver tareas\n4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            user = input("Usuario: ")
            pw = input("Contraseña: ")
            res = requests.post(f"{BASE_URL}/registro", json={"usuario": user, "contraseña": pw})
            print(res.json())

        elif opcion == "2":
            user = input("Usuario: ")
            pw = input("Contraseña: ")
            res = requests.post(f"{BASE_URL}/login", json={"usuario": user, "contraseña": pw})
            print(res.json())

        elif opcion == "3":
            res = requests.get(f"{BASE_URL}/tareas")
            print("Estado:", res.status_code)
            print("Contenido recibido:\n", res.text[:150], "...")

        elif opcion == "4":
            break

if __name__ == "__main__":
    menu()