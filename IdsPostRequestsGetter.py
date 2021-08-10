import time
import pandas as pd
import requests

headers = {
    'authority': 'portalbnmp.cnj.jus.br',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
    'accept': 'application/json',
    'fingerprint': '',
    'sec-ch-ua-mobile': '?1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 Edg/92.0.902.67',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://portalbnmp.cnj.jus.br',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://portalbnmp.cnj.jus.br/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'portalbnmp=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJndWVzdF9wb3J0YWxibm1wIiwiYXV0aCI6IlJPTEVfQU5PTllNT1VTIiwiZXhwIjoxNjI4NjkxNDg3fQ.PrvyrMLkPxOoVWuw6g53Vjvuqtq-5YLqrevhVdBZ5JDkNiY3qwKc_S-stcJXlMja2h2MWAnrnXiYpad7G1Lcxg',
}

start_time = time.time()
df = pd.DataFrame()
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

        inicio = time.time()

        response = requests.post('https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter', headers=headers, params=params, data=data)

        if response.status_code != 200:
            print(f"Deu ruim! Status code: {response.status_code}")
            if erros > 10:
                break
            time.sleep(5)
            response = requests.post('https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter', headers=headers,
                                     params=params, data=data)

            if response.status_code != 200:
                print(f"Não deu mesmo :/ Status code: {response.status_code}")
                erros += 1
                continue

        row_data = response.json()

        last_page = row_data['totalPages']
        for e in row_data["content"]:
            df = df.append(e, ignore_index=True)

        fim = time.time()

        print(f"Tempo para acesso e parse: {(fim-inicio):.2f} segundos.")

        page_number += 1

if len(df) > 0:
    df.to_csv("data_BNMP_POST.tsv", index=False, sep="\t")

end_time = time.time()

print(f"Tempo total de execução: {(end_time-start_time):.2f} segundos.")
