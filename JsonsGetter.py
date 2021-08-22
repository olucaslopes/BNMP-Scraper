from utils.utils import *
import concurrent.futures
import time
from tqdm import tqdm

inicio = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    print("Recuperando informações iniciais...")
    # Faz um POST request de todas as primeiras páginas de todos os estados
    id_estados = [n for n in range(1, 28)]
    primeiras_paginas = list(tqdm(executor.map(obter_post_pag1, id_estados), total=len(id_estados)))

    # Filtra as respostas para cada devida categoria
    poucos_mandados, medio_mandados, muitos_mandados = filtrar_resposta(primeiras_paginas)


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    print("Acessando estados com poucos mandados...")
    # Pega os JSONs das páginas que tem poucos mandados
    poucos_mandados_parseado = executor.map(obter_post_poucos_mandados, poucos_mandados)

    print("Acessando estados com mais mandados...")
    # Pega JSONs das páginas que tem um número médio de mandados
    medio_mandados_parseado = executor.map(obter_post_expandido, medio_mandados)

    # Adicionando listas e planificando all_mandados
    all_madados = [*poucos_mandados_parseado, *medio_mandados_parseado]
    all_madados = [item for sublist in all_madados for item in sublist]

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    print("Salvando JSONs...")
    list(tqdm(executor.map(pega_conteudo_completo, all_madados), total=len(all_madados)))

print(f"Tempo total de execução: {(time.time()-inicio):.2f} segundos.")
