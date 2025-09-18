import random
import string

def generar_contraseña(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))

if __name__ == "__main__":
    print("generador de contraseñas")
    longitud = int(input("Longitud de la contraseña: "))
    print("Tu contraseña es:", generar_contraseña(longitud))