import collections
import requests


def write_id(id_list: list) -> None:
    """
    :type id_list: list
    """
    with open('ids_list.py', 'w', newline='', encoding="utf-8") as pyfile:
        pyfile.write("ids_list = [")
        for id in id_list:
            pyfile.write(str(id) + ", ")
        pyfile.write("]")


def parse_municipios(id_uf: int, headers: dict) -> list:
    """A partir do id da de uma UF retorna
    o id de  todos dos municípios dessa UF."""

    response_munic = requests.get('https://portalbnmp.cnj.jus.br/scaservice/api/municipios/por-uf/' + str(id_uf),
                                  headers=headers)
    munic_list = response_munic.json()
    ids_list = []
    for e in munic_list:
        ids_list.append(e['id'])
    return ids_list


def parse_orgao(id_munic: int, headers: dict) -> list:
    """A partir do id da de um município retorna
    o id de todos os Órgãos Expeditores desse município."""

    response_org = requests.get('https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/orgaos/municipio/' + str(id_munic),
                                headers=headers)
    org_list = response_org.json()
    ids_list = []
    for e in org_list:
        ids_list.append(e['id'])
    return ids_list


def pega_conteudo_completo(linha: dict, headers: dict):
    id_mandado = linha.get("id")
    id_tipo_peca = linha.get("idTipoPeca")

    response = requests.get(
        url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/certidaos/{id_mandado}/{id_tipo_peca}',
        headers=headers
    ).json()
    return flatten(response)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
