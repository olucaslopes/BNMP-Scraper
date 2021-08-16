from fake_useragent import UserAgent
from utils.utils import *
from tqdm import tqdm
import requests
import time
import csv

start_time = time.time()

fieldnames = ['id', 'dataExpedicao', 'dataCriacao', 'numeroPeca', 'tipoPeca_id', 'tipoPeca_descricao', 'status_id',
              'status_descricao', 'numeroProcesso', 'numeroPecaAnterior', 'pessoa_id', 'pessoa_enderecos',
              'pessoa_outrasAlcunhas', 'pessoa_outrosNomes', 'pessoa_nomePai', 'pessoa_nomeMae',
              'pessoa_dataNascimento', 'pessoa_foto', 'pessoa_telefone', 'pessoa_documento', 'pessoa_sinaisMarcas',
              'pessoa_numeroIndividuo', 'pessoa_dadosGeraisPessoa_paisNascimento_nome',
              'pessoa_dadosGeraisPessoa_paisNascimento_id', 'pessoa_dadosGeraisPessoa_naturalidade_id',
              'pessoa_dadosGeraisPessoa_naturalidade_nome', 'pessoa_dadosGeraisPessoa_sexo_id',
              'pessoa_dadosGeraisPessoa_sexo_descricao', 'pessoa_dadosGeraisPessoa_profissao', 'orgaoUsuarioCriador_id',
              'orgaoUsuarioCriador_nome', 'orgaoUsuarioCriador_municipio_id', 'orgaoUsuarioCriador_municipio_nome',
              'orgaoUsuarioCriador_municipio_uf_id', 'orgaoUsuarioCriador_municipio_uf_nome',
              'orgaoUsuarioCriador_municipio_uf_sigla', 'orgaoUsuarioCriador_municipio_codIbge',
              'orgaoUsuarioCriador_municipio_flgDistrito', 'orgaoUsuarioCriador_municipio_idCorporativo',
              'orgaoUsuarioCriador_orgaoTribunal_id', 'orgaoUsuarioCriador_orgaoTribunal_nome',
              'orgaoUsuarioCriador_orgaoTribunal_ativoFormatado', 'orgaoUsuarioCriador_ativoFormatado',
              'orgaoJudiciario_id', 'orgaoJudiciario_nome', 'orgaoJudiciario_municipio_id',
              'orgaoJudiciario_municipio_nome', 'orgaoJudiciario_municipio_uf_id', 'orgaoJudiciario_municipio_uf_nome',
              'orgaoJudiciario_municipio_uf_sigla', 'orgaoJudiciario_municipio_codIbge',
              'orgaoJudiciario_municipio_flgDistrito', 'orgaoJudiciario_municipio_idCorporativo',
              'orgaoJudiciario_orgaoTribunal_id', 'orgaoJudiciario_orgaoTribunal_nome',
              'orgaoJudiciario_orgaoTribunal_ativoFormatado', 'orgaoJudiciario_ativoFormatado', 'sinteseDecisao',
              'magistrado', 'dataValidade', 'especiePrisao', 'cumprimento', 'observacao', 'localOcorrencia',
              'tempoPena', 'tempoPenaAno', 'tempoPenaMes', 'tempoPenaDia', 'regimePrisional', 'recaptura',
              'outrasPecas', 'tipificacaoPenal', 'pessoa_dadosGeraisPessoa_naturalidade_uf_id',
              'pessoa_dadosGeraisPessoa_naturalidade_uf_nome', 'pessoa_dadosGeraisPessoa_naturalidade_uf_sigla']

ua = UserAgent()
cookie = "portalbnmp=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJndWVzdF9wb3J0YWxibm1wIiwiYXV0aCI6IlJPTEVfQU5PTllNT1VTIiwiZXhwIjoxNjI4OTc2MTAzfQ.BgMi8EI52GPVcSJ56vu-jT8SZC2UcT_joDwBFGrtHzTW9H3iHl8jzJFTPGgII2mZrki1DILbjzTT4TWBqTBttw"
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

with open('data_BNMP.tsv', 'w', newline='', encoding="utf-8") as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()


erros = 0
for id_estado in range(1, 2):
    page_number = 0
    last_page = 1
    while page_number < last_page:
        params = (
            ('page', str(page_number)),
            ('size', '2000'),
            ('sort', ''),
        )

        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(id_estado) + '}'

        print(f"Acessando estado {id_estado}/27, página {page_number + 1}/{last_page}")

        inicio_acesso = time.time()
        response = requests.post(
            url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
            headers=headers,
            params=params,
            data=data
        )
        fim_acesso = time.time()

        if response.ok:
            inicio_parse = time.time()
            row_data = response.json()

            last_page = row_data['totalPages']
            if last_page < 6:
                with open('data_BNMP.tsv', 'a+', newline='', encoding="utf-8") as tsvfile:
                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
                    conteudos_completos = list()
                    for e in tqdm(row_data["content"]):
                        conteudo_completo = pega_conteudo_completo(e, headers)
                        conteudos_completos.append(conteudo_completo)

                    writer.writerows(conteudos_completos)

                fim_parse = time.time()

                print(f"Tempo para acesso e parse: {fim_parse - inicio_acesso:.2f} segundos.")
                print(f"Acesso: {fim_acesso - inicio_acesso:.2f} segundos.")
                print(f"Parse: {fim_parse - inicio_parse:.2f} segundos.")

                page_number += 1
            else:
                id_municipios = parse_municipios(id_estado, headers=headers)
                tot_municipios = len(id_municipios)
                munic_cont = 0
                for id_municipio in id_municipios:
                    page_number = 0
                    last_page = 1
                    munic_cont += 1
                    tot_orgaos = None
                    org_cont = 0
                    while page_number < last_page and not (org_cont == tot_orgaos):
                        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(
                            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'

                        params = (
                            ('page', str(page_number)),
                            ('size', '2000'),
                            ('sort', ''),
                        )

                        print(
                            f"Acessando MUNICÍPIO({id_municipio}) {munic_cont}/{tot_municipios}, página {page_number + 1}/{last_page}")
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
                                with open('data_BNMP.tsv', 'a+', newline='', encoding="utf-8") as tsvfile:
                                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                                    for e in raw_data_munic["content"]:
                                        conteudo_completo = pega_conteudo_completo(e, headers)
                                        writer.writerow(conteudo_completo)
                                fim_parse = time.time()

                                print(f"Tempo para acesso e parse: {fim_parse - inicio_acesso:.2f} segundos.")
                                print(f"Acesso: {fim_acesso - inicio_acesso:.2f} segundos.")
                                print(f"Parse: {fim_parse - inicio_parse:.2f} segundos.")

                                page_number += 1
                            else:
                                id_orgaos = parse_orgao(id_municipio, headers=headers)
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
                                                with open('data_BNMP.tsv', 'a+', newline='',
                                                          encoding="utf-8") as tsvfile:
                                                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames,
                                                                            delimiter='\t')
                                                    for e in raw_data_org["content"]:
                                                        conteudo_completo = pega_conteudo_completo(e, headers)
                                                        writer.writerow(conteudo_completo)
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
            # print(response.text)
            # print(response.raise_for_status())
            break

end_time = time.time()

print(f"Total de erros: {erros}")
print()
print(f"Tempo total de execução: {(end_time - start_time):.2f} segundos.")
