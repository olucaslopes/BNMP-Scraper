from utils.utils import *
import time

inicio = time.time()

id_estados = [n for n in range(1, 28)]

print("Acessando ESTADOS.")
poucos_mandados, medio_mandados, muitos_mandados = obter_informacoes_iniciais(id_estados)

mandados_completos = pegar_mandados_completos(poucos_mandados, medio_mandados)

salvar_jsons(mandados_completos)

print("Acessando camada mais profunda...")
print("Acessando MUNICÍPIOS.")

id_estados, id_municipios = obter_informacoes_municicipios(muitos_mandados)
poucos_mandados, medio_mandados, muitos_mandados = obter_informacoes_iniciais(id_estados, id_municipios)

mandados_completos = pegar_mandados_completos(poucos_mandados, medio_mandados)

salvar_jsons(mandados_completos)

print("Acessando camada mais profunda...")
print("Acessando ÓRGÃOS EXPEDITORES.")

id_estados, id_municipios, id_orgaos = obter_informacoes_orgaos(muitos_mandados)
poucos_mandados, medio_mandados, muitos_mandados = obter_informacoes_iniciais(id_estados, id_municipios, id_orgaos)

mandados_completos = pegar_mandados_completos(poucos_mandados, medio_mandados)

salvar_jsons(mandados_completos)

print("Acessando camada final.")
print("Acessando dados por FORÇA BRUTA")

mandados_finais = list()
for mandados_orgao in muitos_mandados:
    mandados_finais.extend(obter_post_forcabruta(mandados_orgao[1], mandados_orgao[2], mandados_orgao[3]))

salvar_jsons(mandados_finais)

print(f"Tempo total de execução: {(time.time()-inicio):.2f} segundos.")
