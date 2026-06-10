import time
import math
import random
import statistics
import threading
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(500_000)

TIMEOUT = 300  
RUNS = 3
SEED = 42

SIZES = [1000, 10000, 100000]

def bubble_sort(arr):
    a = arr.copy()
    trocas = 0
    n = len(a)

    for i in range(n):
        trocou = False

        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                trocas += 1
                trocou = True

        if not trocou:
            break

    return a, trocas

def merge_sort(arr):

    moves = [0]

    def merge(esq, dir):
        resultado = []

        i = 0
        j = 0

        while i < len(esq) and j < len(dir):

            if esq[i] <= dir[j]:
                resultado.append(esq[i])
                i += 1
            else:
                resultado.append(dir[j])
                j += 1

            moves[0] += 1

        while i < len(esq):
            resultado.append(esq[i])
            i += 1
            moves[0] += 1

        while j < len(dir):
            resultado.append(dir[j])
            j += 1
            moves[0] += 1

        return resultado

    def ordenar(vetor):

        if len(vetor) <= 1:
            return vetor

        meio = len(vetor) // 2

        esquerda = ordenar(vetor[:meio])
        direita = ordenar(vetor[meio:])

        return merge(esquerda, direita)

    ordenado = ordenar(arr.copy())

    return ordenado, moves[0]

def quick_sort(arr):

    a = arr.copy()

    trocas = [0]

    def particiona(inicio, fim):

        pivo = a[fim]
        i = inicio - 1

        for j in range(inicio, fim):

            if a[j] <= pivo:
                i += 1

                a[i], a[j] = a[j], a[i]
                trocas[0] += 1

        a[i + 1], a[fim] = a[fim], a[i + 1]
        trocas[0] += 1

        return i + 1

    def ordenar(inicio, fim):

        if inicio < fim:

            p = particiona(inicio, fim)

            ordenar(inicio, p - 1)
            ordenar(p + 1, fim)

    ordenar(0, len(a) - 1)

    return a, trocas[0]

def run_with_timeout(funcao, vetor, timeout):

    resultado = {}

    def worker():

        inicio = time.perf_counter()

        saida = funcao(vetor)

        fim = time.perf_counter()

        resultado["saida"] = saida
        resultado["tempo"] = fim - inicio

    thread = threading.Thread(target=worker)

    thread.start()

    thread.join(timeout)

    if thread.is_alive():
        return None, timeout

    return resultado["saida"], resultado["tempo"]

algoritmos = [
    ("Bubble Sort", bubble_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort)
]

random.seed(SEED)

vetores = {
    tamanho: random.sample(range(tamanho * 10), tamanho)
    for tamanho in SIZES
}

resultados = {}

for nome, algoritmo in algoritmos:

    print("\n" + "=" * 70)
    print(nome)
    print("=" * 70)

    resultados[nome] = []

    for tamanho in SIZES:

        vetor_original = vetores[tamanho]

        tempos = []
        operacoes = []

        interrompido = False

        for execucao in range(RUNS):

            retorno, tempo = run_with_timeout(
                algoritmo,
                vetor_original,
                TIMEOUT
            )

            if retorno is None:

                print(
                    f"{tamanho:,} elementos -> "
                    f"interrompido após {TIMEOUT}s"
                )

                interrompido = True
                break

            _, ops = retorno

            tempos.append(tempo)
            operacoes.append(ops)

        if interrompido:

            resultados[nome].append({
                "tamanho": tamanho,
                "media": None
            })

            continue

        media = statistics.mean(tempos)
        desvio = statistics.stdev(tempos)
        media_ops = statistics.mean(operacoes)

        resultados[nome].append({
            "tamanho": tamanho,
            "media": media
        })

        print(f"\nTamanho: {tamanho:,}")
        print(f"Execução 1: {tempos[0]:.6f} s")
        print(f"Execução 2: {tempos[1]:.6f} s")
        print(f"Execução 3: {tempos[2]:.6f} s")
        print(f"Tempo médio: {media:.6f} s")
        print(f"Desvio padrão: {desvio:.6f} s")
        print(f"Trocas/Movimentações: {int(media_ops):,}")

plt.figure(figsize=(10, 6))

for nome in resultados:

    x = []
    y = []

    for item in resultados[nome]:

        if item["media"] is not None:
            x.append(item["tamanho"])
            y.append(item["media"])

    plt.plot(
        x,
        y,
        marker="o",
        linewidth=2,
        label=nome
    )

plt.title("Tempo Médio de Execução dos Algoritmos")
plt.xlabel("Tamanho do Vetor")
plt.ylabel("Tempo Médio (s)")
plt.grid(True)
plt.legend()

plt.show()