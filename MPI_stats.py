from mpi4py import MPI
import numpy as np
import sys
import logging

def logger_conf(rank): #se crea un logger para cada proceso, asi se evitan los prints, de manera que solo el proceso 0 muestra mensajes
    logging.basicConfig(
        level=logging.INFO if rank == 0 else logging.WARNING,
        format=f'[Process {rank}] %(message)s'
    )
    return logging.getLogger(f'Process_{rank}')

class Dist_Stats: #manejo del calcylo
    def __init__(self, total_size):
        self.comm = MPI.COMM_WORLD # se crea un comunicador glogal
        self.rank = self.comm.Get_rank() # se utuliza el rango del proceso 0 / actual
        self.size = self.comm.Get_size() # se obtiene el numero de procesos
        self.logger = logger_conf(self.rank) # inicia el logger

        self.N = self.comm.bcast(total_size if self.rank == 0 else None, root=0)
        if self.N % self.size != 0: #validacion para que el el tamaño sea divisible entre el número de procesos
            if self.rank == 0:
                raise ValueError(f"Size {self.N} is not divisible by {self.size} processes.")
            else:
                sys.exit(1)

        self.subarray = np.empty(self.N // self.size, dtype=np.float64) # subarreglo local vacío para cada proceso

    def data_dist(self): # se hace una distribucion de datos del momento 0 a todos los demas procesos
        data = None
        if self.rank == 0:
            data = np.random.uniform(0, 100, self.N).astype(np.float64)
        self.comm.Scatter(data, self.subarray, root=0)

    def local_stats_calc(self): #calcula stats locales sobre cada proceso
        return {
            'min': np.min(self.subarray),
            'max': np.max(self.subarray),
            'avg': np.mean(self.subarray)
        }

    def stats_reduce(self, local): # pasa de resultados con valores globales a locales por medio de MPI
        global_min = self.comm.reduce(local['min'], op=MPI.MIN, root=0)
        global_max = self.comm.reduce(local['max'], op=MPI.MAX, root=0)
        avg_sum = self.comm.reduce(local['avg'], op=MPI.SUM, root=0)

        if self.rank == 0:
            global_avg = avg_sum / self.size
            return global_min, global_max, global_avg
        return None, None, None

    def results(self, min_val, max_val, avg_val): #calcula promedios globales
        self.logger.info("\n=== Estadísticas Globales ===")
        self.logger.info(f"Mínimo:   {min_val:.2f}")
        self.logger.info(f"Máximo:   {max_val:.2f}")
        self.logger.info(f"Promedio: {avg_val:.2f}")

def pars_agrs(): #parsea los argumentos de entrada
    if len(sys.argv) != 2:
        print("Uso: python MPI_stats.py <total_size>")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
        if N <= 0:
            raise ValueError
        return N
    except ValueError:
        print("Error: el tamaño debe ser un entero positivo.")
        sys.exit(1)

def main():
    rank = MPI.COMM_WORLD.Get_rank()
    N = pars_agrs() if rank == 0 else None

    try:
        programa = Dist_Stats(N)
    except ValueError as e:
        if rank == 0:
            logger = logger_conf(rank)
            logger.error(str(e))
        sys.exit(1)

    programa.data_dist()
    local_stats = programa.local_stats_calc()
    min_g, max_g, avg_g = programa.stats_reduce(local_stats)

    if programa.rank == 0:
        programa.results(min_g, max_g, avg_g)

if __name__ == "__main__":
    main()
