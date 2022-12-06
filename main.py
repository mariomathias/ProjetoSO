import random
from time import time
from threading import Thread, Semaphore, current_thread
from dataclasses import dataclass

semaforo = Semaphore(2)

@dataclass #Facilita a escrita para os atributos nas classes
class Nodo:
    dado: int = 0
    proximo: any = None
    def __repr__(self):
        if self.proximo == None:
            return f'{self.dado}'
        return f'{self.dado}, {self.proximo.__repr__()}'

@dataclass
class Fila:
    primeiro: Nodo = None
    ultimo: Nodo = None
    def __repr__(self):
        return "[" + str(self.primeiro) + "]"

    def insere_final(self, novo_dado):
        novo_nodo = Nodo(novo_dado)

        if self.primeiro == None:
            self.primeiro = novo_nodo
            self.ultimo = novo_nodo
        else:
            self.ultimo.proximo = novo_nodo
            self.ultimo = novo_nodo

    def insere_inicio(self, novo_dado):
        novo_nodo = Nodo(novo_dado)

        if self.primeiro == None:
            self.primeiro = novo_nodo
            self.ultimo = novo_nodo
        else:
            novo_nodo.proximo = self.primeiro
            self.primeiro = novo_nodo

    def remove(self):
        assert self.primeiro != None, "Impossível remover elemento de fila vazia."
        num = self.primeiro.dado
        self.primeiro = self.primeiro.proximo
        return num
    
    def imprimir(self):
        aux = self.primeiro
        while aux != None:
            print(str(aux.dado) , end=' ')
            aux = aux.proximo
        print("")

fila = Fila()
print("Fila vazia: ", fila)

N_INSERCOINS = 10
N_THREADS = 2

def remover(fila: Fila):
    for i in range(N_INSERCOINS):
        semaforo.acquire()
        n = fila.remove()
        rn = random.randint(0,9)
        fila.insere_final(rn)
        print(f"{current_thread().name}: removeu {n}, adicionou {rn} -> " + str(fila))
        semaforo.release()

for i in range(10):
    num = random.randint(0,9)
    fila.insere_inicio(num)

threads = [Thread(target=remover, args= [fila]) for i in range(N_THREADS)]

start = time()
for t in threads:
    t.start()
for t in threads:
    t.join()
end = time()

print(f"{N_INSERCOINS*N_THREADS} inserções foram feitas em {end-start}s")
print(f"Quantidade de inserções por segundo: {int((N_INSERCOINS*N_THREADS)/(end-start))}")
