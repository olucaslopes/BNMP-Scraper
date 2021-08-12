import time
import requests
import csv
from fake_useragent import UserAgent


start_time = time.time()


def write_id(id_list):
    """
    :type id_list: list
    """
    with open('ids_list.py', 'w', newline='', encoding="utf-8") as pyfile:
        pyfile.write("ids_list = [")
        for id in id_list:
            pyfile.write(str(id) + ", ")
        pyfile.write("]")


def parse_municipios(lista_municipios) -> list:
    """A partir do id da de umaUF retorna
    o id de  todos dos municípios dessa UF."""

    response_munic = requests.get('https://portalbnmp.cnj.jus.br/scaservice/api/municipios/por-uf/' + str(lista_municipios),
                                  headers=headers)
    munic_list = response_munic.json()
    ids_list = []
    for e in munic_list:
        ids_list.append(e['id'])
    return ids_list


def parse_orgao(id_munic) -> list:
    """A partir do id da de um município retorna
    o id de todos os Órgãos Expeditores desse município."""

    response_org = requests.get('https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/orgaos/municipio/' + str(id_munic),
                                headers=headers)
    org_list = response_org.json()
    ids_list = []
    for e in org_list:
        ids_list.append(e['id'])
    return ids_list


fieldnames = ['id',
              'numeroPeca',
              'numeroProcesso',
              'nomePessoa',
              'alcunha',
              'descricaoStatus',
              'dataExpedicao',
              'nomeOrgao',
              'descricaoPeca',
              'idTipoPeca',
              'nomeMae',
              'nomePai',
              'descricaoSexo',
              'descricaoProfissao',
              'dataNascimento',
              'numeroPecaAnterior',
              'numeroPecaFormatado',
              'dataNascimentoFormatada',
              'dataExpedicaoFormatada']

ua = UserAgent()
cookie = 'portalbnmp=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJndWVzdF9wb3J0YWxibm1wIiwiYXV0aCI6IlJPTEVfQU5PTllNT1VTIiwiZXhwIjoxNjI4NTYwMzQxfQ.kkLHa_3zIT5Tq1aW2xhrTa8XshGRdKjlFrNj4APgizxbxfZZjRaLFvvNnzHKGq2PYjhCcGrRWENiJ3Hi0k8KtA'
headers = {
    'authority': 'portalbnmp.cnj.jus.br',
    'accept': 'application/json',
    'user-agent': ua.random,
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://portalbnmp.cnj.jus.br',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://portalbnmp.cnj.jus.br/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': cookie,
}

with open('data_BNMP_POST.tsv', 'w', newline='\n', encoding="utf-8") as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

ids_list = []

erros = 0
for id_estado in range(1, 28):
    page_number = 0
    last_page = 1
    while page_number < last_page:
        params = (
            ('page', str(page_number)),
            ('size', '2000'),
            ('sort', ''),
        )

        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(id_estado) + '}'

        print(f"Acessando estado {id_estado}/27, página {page_number+1}/{last_page}")

        inicio_acesso = time.time()
        response = requests.post(
            url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
            headers=headers,
            params=params,
            data=data
        )
        fim_acesso = time.time()

        if response.status_code == 200:
            inicio_parse = time.time()
            row_data = response.json()

            last_page = row_data['totalPages']
            if last_page < 6:
                with open('data_BNMP_POST.tsv', 'a+', newline='\n', encoding="utf-8") as tsvfile:
                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                    for e in row_data["content"]:
                        writer.writerow(e)
                        ids_list.append(e["id"])

                fim_parse = time.time()

                print(f"Tempo para acesso e parse: {fim_parse - inicio_acesso:.2f} segundos.")
                print(f"Acesso: {fim_acesso - inicio_acesso:.2f} segundos.")
                print(f"Parse: {fim_parse - inicio_parse:.2f} segundos.")

                page_number += 1
            else:
                id_municipios = parse_municipios(id_estado)
                tot_municipios = len(id_municipios)
                munic_cont = 0
                for id_municipio in id_municipios:
                    page_number = 0
                    last_page = 1
                    munic_cont += 1
                    tot_orgaos = None
                    org_cont = 0
                    while page_number < last_page and not (org_cont == tot_orgaos):
                        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'

                        params = (
                            ('page', str(page_number)),
                            ('size', '2000'),
                            ('sort', ''),
                        )

                        print(f"Acessando MUNICÍPIO({id_municipio}) {munic_cont}/{tot_municipios}, página {page_number + 1}/{last_page}")
                        inicio_acesso = time.time()
                        response_munic = requests.post(
                            url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
                            headers=headers,
                            params=params,
                            data=data
                        )
                        fim_acesso = time.time()
                        if response_munic.status_code == 200:
                            inicio_parse = time.time()
                            raw_data_munic = response_munic.json()

                            last_page = raw_data_munic['totalPages']

                            if last_page < 6:
                                with open('data_BNMP_POST.tsv', 'a+', newline='\n', encoding="utf-8") as tsvfile:
                                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                                    for e in raw_data_munic["content"]:
                                        writer.writerow(e)
                                        ids_list.append(e["id"])
                                fim_parse = time.time()

                                print(f"Tempo para acesso e parse: {fim_parse - inicio_acesso:.2f} segundos.")
                                print(f"Acesso: {fim_acesso - inicio_acesso:.2f} segundos.")
                                print(f"Parse: {fim_parse - inicio_parse:.2f} segundos.")

                                page_number += 1
                            else:
                                id_orgaos = parse_orgao(id_municipio)
                                tot_orgaos = len(id_orgaos)
                                for id_orgao in id_orgaos:
                                    page_number = 0
                                    last_page = 1
                                    org_cont += 1
                                    while page_number < last_page:
                                        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(
                                            id_orgao) + '},"idEstado":' + str(id_estado) + ',"idMunicipio":' + str(
                                            id_municipio) + '}'

                                        print(
                                            f"Acessando ÓRGÃO({id_orgao}) {org_cont}/{tot_orgaos}, página {page_number + 1}/{last_page}")

                                        params = (
                                            ('page', str(page_number)),
                                            ('size', '2000'),
                                            ('sort', ''),
                                        )

                                        inicio_acesso = time.time()
                                        response_org = requests.post(
                                            url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
                                            headers=headers,
                                            params=params,
                                            data=data
                                        )
                                        fim_acesso = time.time()

                                        if response_org.status_code == 200:
                                            inicio_parse = time.time()
                                            raw_data_org = response_org.json()

                                            last_page = raw_data_org['totalPages']

                                            if last_page > 0:
                                                with open('data_BNMP_POST.tsv', 'a+', newline='\n',
                                                          encoding="utf-8") as tsvfile:
                                                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames,
                                                                            delimiter='\t')
                                                    for e in raw_data_org["content"]:
                                                        writer.writerow(e)
                                                        ids_list.append(e["id"])
                                            fim_parse = time.time()

                                            print(
                                                f"Tempo para acesso e parse: {fim_parse - inicio_acesso:.2f} segundos.")
                                            print(f"Acesso: {fim_acesso - inicio_acesso:.2f} segundos.")
                                            print(f"Parse: {fim_parse - inicio_parse:.2f} segundos.")

                                            page_number += 1
                                        else:
                                            print(f"Deu ruim! Status code: {response_org.status_code}")
                                            print("Você está olhando pros Órgãos Expeditores",
                                                  f"<{id_estado}:{id_municipio}:{id_orgao}>")
                                            erros += 1
                                            break
                        else:
                            print(f"Deu ruim! Status code: {response_munic.status_code}")
                            print("Você está olhando pros Municípios",
                                  f"<{id_estado}:{id_municipio}>")
                            erros += 1
                            break
        else:
            print(f"Deu ruim! Status code: {response.status_code}")
            print("Erro inesperado :(. Você está olhando pros estados", f"<{id_estado}>")
            erros += 1
            #print(response.text)
            #print(response.raise_for_status())
            break

print("Escrevendo arquivo ids_list.py..")
inicio_escrita = time.time()
write_id(ids_list)
fim_escrita = time.time()
print(f"Tempo para escrita: {(fim_escrita - inicio_escrita):.2f} segundos.")
end_time = time.time()

print(f"Total de erros: {erros}")
print()
print(f"Tempo total de execução: {(end_time-start_time):.2f} segundos.")
