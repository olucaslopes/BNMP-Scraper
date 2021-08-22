from utils.utils import *
import time

inicio = time.time()

id_estados = [n for n in range(1, 3)]
poucos_mandados, medio_mandados, muitos_mandados = obter_informacoes_iniciais(id_estados)

mandados_completos = pegar_mandados_completos(poucos_mandados, medio_mandados)

salvar_jsons(mandados_completos)

print(f"Tempo total de execução: {(time.time()-inicio):.2f} segundos.")
