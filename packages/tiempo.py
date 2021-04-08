import time

class Cronometro:
    def __init__(self):
        self.starting_point = time.time()

    def tiempo(self):
        elapsed_time = time.time() - self.starting_point
        elapsed_time_int = int(elapsed_time)
        elapsed_time_minutes = int(elapsed_time_int / 60)
        elapsed_time_seconds = elapsed_time_int % 60
        print("Tiempo de Proceso = " + str(elapsed_time_minutes) + ' minutos con ' + str(elapsed_time_seconds) + ' segundos.')