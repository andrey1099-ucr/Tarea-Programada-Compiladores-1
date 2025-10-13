# Comentario de prueba
class Carro:
    def __init__(self, color, motor):
        self.color = color
        self.motor = motor

    def encender(self):
        if not self.motor.activo:
            self.motor.arrancar()
            print("Motor encendido")

def main():
    carro = Carro("rojo", Motor())
    carro.encender()

# Variables y expresiones
x = 10
y = 20.5
z = x * (y + 3) / 2 - 5

# Operadores lógicos y comparaciones
if x > 5 and y <= 30 or not z == 0:
    print("Condición verdadera")

# Acceso a métodos y atributos anidados
self.motor.aceite.nivel = 100
obj.metodo1().metodo2(3).propiedad

# Listas, diccionarios y strings
lista = [1, 2, 3]
dic = {"llave": "valor", "numero": 123}
texto = "Hola Mundo"
