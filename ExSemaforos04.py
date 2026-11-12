import multiprocessing
import time
import random

chegada: int = 0
sema_pista = None
sema_carros = None

def init(c, sem_pista, sem_carros):
    global chegada, sema_pista, sema_carros
    chegada = c
    sema_pista = sem_pista
    sema_carros = sem_carros

def n_carros(id, carros, voltas):
    
    with sema_pista:
        carros_andando(id, carros, voltas)

def carros_andando(id, carros, voltas):
    global chegada, sema_carros
    tempo: float = 0.0
    total_voltas: int = 3
    
    with sema_carros[id - 1]:
        for i in range(len(carros)):        
            while voltas < total_voltas:
                voltas += 1
                tempo = random.randint(6000, 12000)
                tempo = tempo / 1000
                time.sleep(tempo)
                print(f"O carro #{carros[i]} completou a volta {voltas} em {tempo:.2f} segundos.")
            chegada.value += 1
            print(f"O carro #{carros[i]} terminou a corrida em {chegada.value}º lugar.")
                
                
                
def main():
    params: int = [(0,0,0)]*7
    voltas: int = 0
    semaforo_pista = None
    semaforo_carros = None
    pos_chegada: int = 0
    
    pos_chegada = multiprocessing.Value('i', 0)
    
    cont: int = 0
    for i in range(7):
        carros: int = [0]*2
        for j in range(2):
            cont += 1
            carros[j] = cont
        params[i] = (i + 1, carros, voltas)
    with multiprocessing.Manager() as manager:
        semaforo_pista = manager.Semaphore(5)
        semaforo_carros = [manager.Semaphore(1) for i in range(7)]
        with multiprocessing.Pool(processes=14, initializer=init, initargs=(pos_chegada, semaforo_pista, semaforo_carros)) as threads:
            threads.starmap(n_carros, params)

if __name__ == '__main__':
    main() 