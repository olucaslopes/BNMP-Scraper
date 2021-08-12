from fake_useragent import UserAgent
from utils.utils import *
from tqdm import tqdm
import requests
import time
import csv

start_time = time.time()

fieldnames = ['id', 'dataExpedicao', 'dataCriacao', 'numeroPeca', 'tipoPeca_id', 'tipoPeca_descricao', 'status_id',
              'status_descricao', 'numeroProcesso', 'dataExpedicaoString', 'url', 'numeroIndividuo',
              'numeroPecaAnterior', 'pessoa_id', 'pessoa_enderecos', 'pessoa_outrasAlcunhas', 'pessoa_outrosNomes',
              'pessoa_nomePai', 'pessoa_nomeMae', 'pessoa_dataNascimento', 'pessoa_foto', 'pessoa_telefone',
              'pessoa_documento', 'pessoa_sinaisMarcas', 'pessoa_datasNascimentoString', 'pessoa_outrosNomesString',
              'pessoa_outrasAlcunhasString', 'pessoa_nomeMaeString', 'pessoa_nomePaiString', 'pessoa_numeroIndividuo',
              'pessoa_dadosGeraisPessoa_paisNascimento_nome', 'pessoa_dadosGeraisPessoa_paisNascimento_id',
              'pessoa_dadosGeraisPessoa_naturalidade_id', 'pessoa_dadosGeraisPessoa_naturalidade_nome',
              'pessoa_dadosGeraisPessoa_naturalidade_uf', 'pessoa_dadosGeraisPessoa_naturalidade_codIbge',
              'pessoa_dadosGeraisPessoa_naturalidade_flgDistrito',
              'pessoa_dadosGeraisPessoa_naturalidade_idCorporativo', 'pessoa_dadosGeraisPessoa_sexo_id',
              'pessoa_dadosGeraisPessoa_sexo_descricao', 'pessoa_dadosGeraisPessoa_profissao', 'orgaoUsuarioCriador_id',
              'orgaoUsuarioCriador_externo', 'orgaoUsuarioCriador_nome', 'orgaoUsuarioCriador_telefone',
              'orgaoUsuarioCriador_ativo', 'orgaoUsuarioCriador_dtCadastro', 'orgaoUsuarioCriador_tipo',
              'orgaoUsuarioCriador_municipio_id', 'orgaoUsuarioCriador_municipio_nome',
              'orgaoUsuarioCriador_municipio_uf_id', 'orgaoUsuarioCriador_municipio_uf_nome',
              'orgaoUsuarioCriador_municipio_uf_sigla', 'orgaoUsuarioCriador_municipio_uf_paisId',
              'orgaoUsuarioCriador_municipio_codIbge', 'orgaoUsuarioCriador_municipio_flgDistrito',
              'orgaoUsuarioCriador_municipio_idCorporativo', 'orgaoUsuarioCriador_usuarioId',
              'orgaoUsuarioCriador_orgaoPaiId', 'orgaoUsuarioCriador_orgaoPaiNome',
              'orgaoUsuarioCriador_orgaoTribunal_id', 'orgaoUsuarioCriador_orgaoTribunal_externo',
              'orgaoUsuarioCriador_orgaoTribunal_nome', 'orgaoUsuarioCriador_orgaoTribunal_telefone',
              'orgaoUsuarioCriador_orgaoTribunal_ativo', 'orgaoUsuarioCriador_orgaoTribunal_dtCadastro',
              'orgaoUsuarioCriador_orgaoTribunal_tipo', 'orgaoUsuarioCriador_orgaoTribunal_municipio',
              'orgaoUsuarioCriador_orgaoTribunal_usuarioId', 'orgaoUsuarioCriador_orgaoTribunal_orgaoPaiId',
              'orgaoUsuarioCriador_orgaoTribunal_orgaoPaiNome', 'orgaoUsuarioCriador_orgaoTribunal_orgaoTribunal',
              'orgaoUsuarioCriador_orgaoTribunal_filhos', 'orgaoUsuarioCriador_orgaoTribunal_logomarca',
              'orgaoUsuarioCriador_orgaoTribunal_cep', 'orgaoUsuarioCriador_orgaoTribunal_endereco',
              'orgaoUsuarioCriador_orgaoTribunal_bairro', 'orgaoUsuarioCriador_orgaoTribunal_complemento',
              'orgaoUsuarioCriador_orgaoTribunal_ordem', 'orgaoUsuarioCriador_orgaoTribunal_codHierarquia',
              'orgaoUsuarioCriador_orgaoTribunal_plantaoId', 'orgaoUsuarioCriador_orgaoTribunal_unidadeJurisdicional',
              'orgaoUsuarioCriador_orgaoTribunal_dominioEmails', 'orgaoUsuarioCriador_orgaoTribunal_ativoFormatado',
              'orgaoUsuarioCriador_filhos', 'orgaoUsuarioCriador_logomarca', 'orgaoUsuarioCriador_cep',
              'orgaoUsuarioCriador_endereco', 'orgaoUsuarioCriador_bairro', 'orgaoUsuarioCriador_complemento',
              'orgaoUsuarioCriador_ordem', 'orgaoUsuarioCriador_codHierarquia', 'orgaoUsuarioCriador_plantaoId',
              'orgaoUsuarioCriador_unidadeJurisdicional', 'orgaoUsuarioCriador_dominioEmails',
              'orgaoUsuarioCriador_ativoFormatado', 'orgaoJudiciario_id', 'orgaoJudiciario_externo',
              'orgaoJudiciario_nome', 'orgaoJudiciario_telefone', 'orgaoJudiciario_ativo', 'orgaoJudiciario_dtCadastro',
              'orgaoJudiciario_tipo', 'orgaoJudiciario_municipio_id', 'orgaoJudiciario_municipio_nome',
              'orgaoJudiciario_municipio_uf_id', 'orgaoJudiciario_municipio_uf_nome',
              'orgaoJudiciario_municipio_uf_sigla', 'orgaoJudiciario_municipio_uf_paisId',
              'orgaoJudiciario_municipio_codIbge', 'orgaoJudiciario_municipio_flgDistrito',
              'orgaoJudiciario_municipio_idCorporativo', 'orgaoJudiciario_usuarioId', 'orgaoJudiciario_orgaoPaiId',
              'orgaoJudiciario_orgaoPaiNome', 'orgaoJudiciario_orgaoTribunal_id',
              'orgaoJudiciario_orgaoTribunal_externo', 'orgaoJudiciario_orgaoTribunal_nome',
              'orgaoJudiciario_orgaoTribunal_telefone', 'orgaoJudiciario_orgaoTribunal_ativo',
              'orgaoJudiciario_orgaoTribunal_dtCadastro', 'orgaoJudiciario_orgaoTribunal_tipo',
              'orgaoJudiciario_orgaoTribunal_municipio', 'orgaoJudiciario_orgaoTribunal_usuarioId',
              'orgaoJudiciario_orgaoTribunal_orgaoPaiId', 'orgaoJudiciario_orgaoTribunal_orgaoPaiNome',
              'orgaoJudiciario_orgaoTribunal_orgaoTribunal', 'orgaoJudiciario_orgaoTribunal_filhos',
              'orgaoJudiciario_orgaoTribunal_logomarca', 'orgaoJudiciario_orgaoTribunal_cep',
              'orgaoJudiciario_orgaoTribunal_endereco', 'orgaoJudiciario_orgaoTribunal_bairro',
              'orgaoJudiciario_orgaoTribunal_complemento', 'orgaoJudiciario_orgaoTribunal_ordem',
              'orgaoJudiciario_orgaoTribunal_codHierarquia', 'orgaoJudiciario_orgaoTribunal_plantaoId',
              'orgaoJudiciario_orgaoTribunal_unidadeJurisdicional', 'orgaoJudiciario_orgaoTribunal_dominioEmails',
              'orgaoJudiciario_orgaoTribunal_ativoFormatado', 'orgaoJudiciario_filhos', 'orgaoJudiciario_logomarca',
              'orgaoJudiciario_cep', 'orgaoJudiciario_endereco', 'orgaoJudiciario_bairro',
              'orgaoJudiciario_complemento', 'orgaoJudiciario_ordem', 'orgaoJudiciario_codHierarquia',
              'orgaoJudiciario_plantaoId', 'orgaoJudiciario_unidadeJurisdicional', 'orgaoJudiciario_dominioEmails',
              'orgaoJudiciario_ativoFormatado', 'sinteseDecisao', 'magistrado', 'dataAtualString', 'mandado',
              'motivoExpedicaoAlvara', 'motivoExpedicao', 'dataValidade', 'dataValidadeString', 'especiePrisao',
              'cumprimento', 'observacao', 'localOcorrencia', 'tempoPena', 'tempoPenaAno', 'tempoPenaMes',
              'tempoPenaDia', 'regimePrisional', 'recaptura', 'alcunhasString', 'nomesString', 'nomesPaiString',
              'nomesMaeString', 'tipificacoesPenaisString', 'localDataFormatado', 'dataNascimentoString',
              'mandadosInternacaoAlcancados', 'mandadosPrisaoAlcancados', 'outrasPecas',
              'contramandadoMandadoAlcancados', 'isSolturaConcedida', 'tipificacaoPenal',
              'pessoa_dadosGeraisPessoa_naturalidade_uf_id', 'pessoa_dadosGeraisPessoa_naturalidade_uf_nome',
              'pessoa_dadosGeraisPessoa_naturalidade_uf_sigla', 'pessoa_dadosGeraisPessoa_naturalidade_uf_paisId']

ua = UserAgent()
cookie = 'portalbnmp=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJndWVzdF9wb3J0YWxibm1wIiwiYXV0aCI6IlJPTEVfQU5PTllNT1VTIiwiZXhwIjoxNjI4ODU3MjYyfQ.Eox3s6_vCT8ac13tVI2JyqqbehW2AsOFYVUbxaozsb_Zy0jUvljPjRCXldgiFYYUECA1Gqaq-KQv_GbYKzBtjg'
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
                with open('data_BNMP_POST.tsv', 'a+', newline='\n', encoding="utf-8") as tsvfile:
                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                    conteudos_completos = list()
                    for e in tqdm(row_data["content"]):
                        conteudo_completo = pega_conteudo_completo(e, headers)
                        conteudos_completos.append(conteudo_completo)
                        ids_list.append(e["id"])

                    writer.writerows(conteudo_completo)

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
                                with open('data_BNMP_POST.tsv', 'a+', newline='\n', encoding="utf-8") as tsvfile:
                                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                                    for e in raw_data_munic["content"]:
                                        conteudo_completo = pega_conteudo_completo(e, headers)
                                        writer.writerow(conteudo_completo)
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
                                                        conteudo_completo = pega_conteudo_completo(e, headers)
                                                        writer.writerow(conteudo_completo)
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
            # print(response.text)
            # print(response.raise_for_status())
            break

print("Escrevendo arquivo ids_list.py..")
inicio_escrita = time.time()
write_id(ids_list)
fim_escrita = time.time()
print(f"Tempo para escrita: {(fim_escrita - inicio_escrita):.2f} segundos.")
end_time = time.time()

print(f"Total de erros: {erros}")
print()
print(f"Tempo total de execução: {(end_time - start_time):.2f} segundos.")
