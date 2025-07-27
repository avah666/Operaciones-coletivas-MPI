from mpi4py import MPI
import numpy as np
import sys
import logging

def setup_logger(rank): # se configura el sistema de logger para agilizar el proceso de errores
    logging.basicConfig(
        level=logging.INFO if rank == 0 else logging.WARNING,
        format='[Process %(name)s] %(message)s'
    )
    return logging.getLogger(str(rank))

def measure_latency(comm, msg, iterations, logger): #la funcion se encar de medio la latencia entre el envio y el recibimiento de mensajes entre procesos
    start = MPI.Wtime() # se inicia el tiempo
    for _ in range(iterations):
        comm.Send([msg, MPI.BYTE], dest=1, tag=0) # mensaje al proceso 1
        comm.Recv([msg, MPI.BYTE], source=1, tag=1) # respuesta del proceso 1
    end = MPI.Wtime() # se guarda el tiempo final

    total = end - start # calculo de timpo total para los msjs
    round_trip = (total / iterations) * 1e6 #latencia total
    one_way = round_trip / 2 # la tencia por viaje unidireccional

    logger.info(f"Sent {iterations} messages of {msg.nbytes} byte(s).") # loggers de informacion sobre las estadisticas de latencia
    logger.info(f"Round-trip latency: {round_trip:.2f} µs")
    logger.info(f"One-way latency: {one_way:.2f} µs")

def respond(comm, msg, iterations): # configuracion de estadisticas de latencia para el proceso 0
    for _ in range(iterations):
        comm.Recv([msg, MPI.BYTE], source=0, tag=0)
        comm.Send([msg, MPI.BYTE], dest=0, tag=1)

def main(): # de esta funcion sale la respuesta de todo el programa
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    logger = setup_logger(rank)

    if size != 2: #warning ya que el programa solo debe ejecutarse con 2 procesos
        if rank == 0:
            logger.error("This program requires exactly 2 processes.")
        sys.exit(1)
    #se obtiene el numero de iteraciones 
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    msg = np.zeros(1, dtype='b')

    if rank == 0:
        measure_latency(comm, msg, iterations, logger)
    else:
        respond(comm, msg, iterations)

if __name__ == "__main__":
    main()
