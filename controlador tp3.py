from controller import Robot

AVANZAR = "Avanzar"
RETROCEDER = "Retroceder"
GIRAR = "Girar"

robot = Robot()
timestep = int(robot.getBasicTimeStep())

#Sensores 
sensor_adelante = robot.getDevice('ps0')  
sensor_izquierdo = robot.getDevice('ps5')  
sensor_derecho = robot.getDevice('ps2')  

sensor_adelante.enable(timestep)
sensor_izquierdo.enable(timestep)
sensor_derecho.enable(timestep)

#Giroscopo 
giroscopio = robot.getDevice('gyro')
giroscopio.enable(timestep)

#Motores
motor_izquierdo = robot.getDevice('left wheel motor')
motor_derecho = robot.getDevice('right wheel motor')

motor_izquierdo.setPosition(float('inf'))
motor_derecho.setPosition(float('inf'))


estado_actual = AVANZAR
velocidad_base = 3.0
velocidad_maxima = 6.28
umbral_proximidad = 150

# Funciones
def leer_sensores():
    return sensor_adelante.getValue(), sensor_izquierdo.getValue(), sensor_derecho.getValue()

def imprimir_telemetria(frontal, izquierdo, derecho):
    print(f"Telemetría: Frontal={frontal:.2f}, Izquierdo={izquierdo:.2f}, Derecho={derecho:.2f}")

def establecer_velocidades(vel_izquierda, vel_derecha):
    motor_izquierdo.setVelocity(vel_izquierda)
    motor_derecho.setVelocity(vel_derecha)

def girar(direccion, angulo_deseado):
    velocidad_giro = 2.0 if direccion == "izquierda" else -2.0
    establecer_velocidades(velocidad_giro, -velocidad_giro)

    angulo_acumulado = 0.0
    while robot.step(timestep) != -1:
        delta_angulo = giroscopio.getValues()[2] * (timestep / 1000.0)  
        angulo_acumulado += abs(delta_angulo)

        if angulo_acumulado >= angulo_deseado:
            break

    establecer_velocidades(0.0, 0.0)

# Cuerpo principal del codogo
while robot.step(timestep) != -1:

    frontal, izquierdo, derecho = leer_sensores()
    imprimir_telemetria(frontal, izquierdo, derecho)

    if frontal > umbral_proximidad:
        estado_actual = RETROCEDER
    elif izquierdo > umbral_proximidad:
        estado_actual = GIRAR
    elif derecho > umbral_proximidad:
        estado_actual = GIRAR
    else:
        estado_actual = AVANZAR

    if estado_actual == AVANZAR:
        print("Estado: Avanzar")
        establecer_velocidades(velocidad_base, velocidad_base)

    elif estado_actual == RETROCEDER:
        print("Estado: Retroceder")
        establecer_velocidades(-velocidad_base, -velocidad_base)
        robot.step(500)  
        estado_actual = GIRAR  

    elif estado_actual == GIRAR:
        print("Estado: Girar")
        if izquierdo > derecho:
            girar("derecha", 1.57) 
        else:
            girar("izquierda", 1.57)  
        estado_actual = AVANZAR
