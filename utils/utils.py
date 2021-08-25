import collections
import requests
from utils.envVars import *
import concurrent.futures
from tqdm import tqdm


def pega_ids_municipios(id_uf: int) -> list:
    """A partir do id da de uma UF retorna
    o id de  todos dos municípios dessa UF."""

    response_munic = requests.get(
        url=f'https://portalbnmp.cnj.jus.br/scaservice/api/municipios/por-uf/{id_uf}',
        headers=headers
    )
    munic_list = response_munic.json()
    ids_list = []
    for e in munic_list:
        ids_list.append(e['id'])
    return ids_list


def pega_ids_orgaos(id_munic: int) -> list:
    """A partir do id da de um município retorna
    o id de todos os Órgãos Expeditores desse município."""

    response_org = requests.get(
        url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/orgaos/municipio/{id_munic}',
        headers=headers
    )
    org_list = response_org.json()
    ids_list = []
    for e in org_list:
        ids_list.append(e['id'])
    return ids_list


def pega_conteudo_completo(linha: dict):
    """
    "Entra" em cada um dos mandados com o
    método GET para pegar mais informações
    e salva-nas em json/<id_mandado>.json
    """
    headers['user-agent'] = ua.random
    id_mandado = linha.get("id")
    id_tipo_peca = linha.get("idTipoPeca")

    response = requests.get(
        url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/certidaos/{id_mandado}/{id_tipo_peca}',
        headers=headers
    )
    if response.ok:
        response_dict = response.json()
        with open(f"json/{response_dict['id']}.json", 'wb') as outf:
            outf.write(response.content)
    else:
        print(f"Deu ruim! Status code: {response.status_code}")
        print("Você está olhando pro pega_conteudo_completo")


def flatten(d, parent_key='', sep='_'):
    """Planifica dicionários aninhados."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def post_obter_data(id_estado: int, id_municipio: int = "", id_orgao: int = "") -> str:
    """Tem como parâmetros os ids em questão.
    Retorna a variável data necessário para
    fazer uma requisição do tipo POST."""
    if not id_municipio and not id_orgao:
        # Só tem estado!
        # print(f"Acessando estado {id_estado}/27")
        return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(id_estado) + '}'
    elif not id_orgao:
        # Tem estado e id_municipio!
        # print(f"Acessando MUNICÍPIO({id_municipio})")
        return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'
    else:
        # Tem estado, municipio e orgao!
        # print(f"Acessando ÓRGÃO({id_orgao})")
        return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(id_orgao) + '},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'


def obter_post_pag1(id_estado: int, id_municipio: int = 0, id_orgao: int = 0) -> tuple:
    """Faz um POST request da primeira página para
    obter até 2.000 elementos. Retorna um dicionário
     e um int com o total de mandados daquele id."""
    params = (
        ('page', '0'),
        ('size', '2000'),
        ('sort', 'dataExpedicao,ASC'),
    )

    data = post_obter_data(id_estado, id_municipio, id_orgao)

    raw_data = obter_post(params, data)
    return raw_data, id_estado, id_municipio, id_orgao


def obter_post(params, data):
    """Faz uma requisição do tipo POST e retorna
    um JSON se ela for bem sucedida e um NoneType
    caso contrário"""
    response = requests.post(
        url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
        headers=headers,
        params=params,
        data=data
    )
    if response.ok:
        return response.json()
    else:
        print(f"Deu Ruim! POST request não bem sucedida. Status code:{response.status_code}")


def obter_post_poucos_mandados(response_pag1: tuple[dict, int, int, int]) -> list:
    """
    Obtém até 10.000 linhas de dados.
    Retorna uma lista de dicts
    :param response_pag1: raw_data, id_estado, id_municipio, id_orgao
    :return: list: lista de dicionários de mandados
    """
    raw_data, id_estado, id_municipio, id_orgao = response_pag1[0], response_pag1[1], response_pag1[2], response_pag1[3]
    data = post_obter_data(id_estado, id_municipio, id_orgao)
    all_mandados = list()
    all_mandados.extend(raw_data['content'])
    total_pages = raw_data['totalPages']
    total_elements = raw_data['numberOfElements']
    params = tuple((('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,ASC')) for x in range(1, 5))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        novos_mandados = executor.map(obter_post, params, tuple(data for _ in range(len(params))))
    for e in [x['content'] for x in novos_mandados]:
        all_mandados.extend(e)
    return all_mandados


def obter_post_expandido(response_pag1: tuple[dict, int, int, int]) -> list:
    """
    Aproveita-se da ordenação para extrapolar o
    limite de 10.000 linhas e alcaçar até o dobro disso.
    Retorna uma lista de dicts
    """
    raw_data, id_estado, id_municipio, id_orgao = response_pag1[0], response_pag1[1], response_pag1[2], response_pag1[3]
    data = post_obter_data(id_estado, id_municipio, id_orgao)
    all_mandados = list()
    all_mandados.extend(raw_data['content'])
    total_pages = raw_data['totalPages']
    total_elements = raw_data['numberOfElements']
    params = tuple((('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,ASC')) for x in range(1, 5))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        novos_mandados = executor.map(obter_post, params, tuple(data for _ in range(len(params))))
    for e in [x['content'] for x in novos_mandados]:
        all_mandados.extend(e)
    paginas_restantes = (total_elements - 10000) // 2000
    if paginas_restantes > 1:
        params = tuple(
            (('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,DESC')) for x in range(0, paginas_restantes))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            novos_mandados = executor.map(obter_post, params, tuple(data for _ in range(len(params))))
        for e in [x['content'] for x in novos_mandados]:
            all_mandados.extend(e)
    params = (('page', str(paginas_restantes + 1)), ('size', '2000'), ('sort', 'dataExpedicao,DESC'))
    ultima_pag = obter_post(params, data)
    all_mandados.extend([x for x in ultima_pag['content'] if x not in all_mandados])
    return all_mandados


def obter_post_forcabruta(id_estado: int, id_municipio: int, id_orgao: int) -> list:
    data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(id_orgao) + '},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'
    data = [data for _ in range(len(params_forca_bruta))]

    all_mandados = list()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        novos_mandados = executor.map(obter_post, params_forca_bruta, data)
    for lista_mandados in [x['content'] for x in novos_mandados if x]:
        all_mandados.extend([mandado for mandado in lista_mandados if mandado not in all_mandados])
    return all_mandados


def filtrar_resposta(lista_primeiras_paginas):
    poucos_mandados, medio_mandados, muitos_mandados = list(), list(), list()
    for mandados_dict in lista_primeiras_paginas:
        if mandados_dict[0]['totalElements'] <= 10000:
            poucos_mandados.append(mandados_dict)
        elif mandados_dict[0]['totalElements'] <= 20000:
            medio_mandados.append(mandados_dict)
        else:
            muitos_mandados.append(mandados_dict)
    return poucos_mandados, medio_mandados, muitos_mandados


def obter_informacoes_iniciais(id_estados: list, id_municipios: list = None, id_orgaos: list = None) -> tuple:
    """
    Faz um POST request de todas as primeiras páginas de todos os estados
    e filtra as respostas para cada devida categoria. Retorna um tuple
    :param id_estados: lista de ints, cada um é um id que pertence ao intervalo [1,27].
    :param id_municipios: lista de ints, cada um é um id.
    :param id_orgaos: lista de ints, cada um é um id.
    :return: tuple: poucos_mandados, medio_mandados, muitos_mandados
    """
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    print("Recuperando informações iniciais...")
    if not id_municipios and not id_orgaos:
        # Só tem estado!
        primeiras_paginas = list(tqdm(executor.map(obter_post_pag1, id_estados), total=len(id_estados)))
        return filtrar_resposta(primeiras_paginas)
    elif not id_orgaos:
        # Tem estado e id_municipio!
        primeiras_paginas = list(tqdm(executor.map(obter_post_pag1, id_municipios), total=len(id_municipios)))
        return filtrar_resposta(primeiras_paginas)
    else:
        # Tem estado, municipio e orgao!
        primeiras_paginas = list(tqdm(executor.map(obter_post_pag1, id_orgaos), total=len(id_orgaos)))
        return filtrar_resposta(primeiras_paginas)


def pegar_mandados_completos(poucos_mandados: list, medio_mandados) -> list:
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    print("Acessando estados com poucos mandados...")
    # Pega os JSONs das páginas que tem poucos mandados
    poucos_mandados_parseado = executor.map(obter_post_poucos_mandados, poucos_mandados)

    print("Acessando estados com mais mandados...")
    # Pega JSONs das páginas que tem um número médio de mandados
    medio_mandados_parseado = executor.map(obter_post_expandido, medio_mandados)

    # Adicionando listas e planificando all_mandados
    all_madados = [*poucos_mandados_parseado, *medio_mandados_parseado]
    all_madados = [item for sublist in all_madados for item in sublist]
    return all_madados


def salvar_jsons(lista_mandados: list):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
    print("Salvando JSONs...")
    list(tqdm(executor.map(pega_conteudo_completo, lista_mandados), total=len(lista_mandados)))
