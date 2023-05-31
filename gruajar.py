import tkinter as tk
import serial
import time
import matplotlib.pyplot as plt
import threading


import threading
#import PIL.Image





# Configuración de la interfaz de usuario
raiz = tk.Tk()
raiz.title =  ("GRUA JAR")
raiz.geometry("600x400")






s1 = tk.Scale(raiz, from_=0, to=180, orient=tk.HORIZONTAL, label="Servo Eje X", background="#7FFFD4" )
s2 = tk.Scale(raiz, from_=0, to=180, orient=tk.HORIZONTAL, label="Servo Eje Y", background="#F5F5DC")

s1.pack()
s2.pack()


# Conexión con Arduino
arduino = serial.Serial('COM4', 9600)

time.sleep(2)  # Espera a que Arduino se reinicie

# Función para enviar los valores de los sliders a Arduino
def send_to_arduino():
    s1_val = s1.get()
    s2_val = s2.get()
    
    arduino.write(bytes(str(s1_val) + "," + str(s2_val) + "," + "\n", 'utf-8'))



# Función para actualizar la posición de los servos
def update_servos():
    send_to_arduino()
    raiz.after(100, update_servos)

# Función para cerrar la conexión con Arduino cuando se cierra la ventana
def on_closing():
    arduino.close()
    raiz.destroy()

raiz.protocol("WM_DELETE_WINDOW", on_closing)
raiz.after(100, update_servos)

x_data = []
y_data = []

plt.ion()

fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Distancia (cm)')
ax.set_title('Distancia del objeto')

while True:
    try:
        distance = float(arduino.readline().decode().strip())
        x_data.append(len(x_data)*0.5)
        y_data.append(distance)
        line.set_xdata(x_data)
        line.set_ydata(y_data)
        ax.relim()
        ax.set_ylim({0,30})
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
    except KeyboardInterrupt:
        break

arduino.close()

# Bucle principal de la interfaz de usuario

raiz.mainloop()


