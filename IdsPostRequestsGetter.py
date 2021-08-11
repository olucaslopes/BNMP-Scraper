import time
import requests
import csv
from fake_useragent import UserAgent

start_time = time.time()
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
            with open('data_BNMP_POST.tsv', 'a+', newline='\n', encoding="utf-8") as tsvfile:
                writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                for e in row_data["content"]:
                    writer.writerow(e)

            fim_parse = time.time()

            print(f"Tempo para acesso e parse: {fim_parse - inicio_acesso:.2f} segundos.")
            print(f"Acesso: {fim_acesso - inicio_acesso:.2f} segundos.")
            print(f"Parse: {fim_parse - inicio_parse:.2f} segundos.")

            page_number += 1
        else:
            print(f"Deu ruim! Status code: {response.status_code}")
            print("Erro inesperado :(. Você está olhando pros estados", f"<{id_estado}>")
            erros += 1
            #print(response.text)
            #print(response.raise_for_status())
            break



end_time = time.time()

print(f"Total de erros: {erros}")
print()
print(f"Tempo total de execução: {(end_time-start_time):.2f} segundos.")
