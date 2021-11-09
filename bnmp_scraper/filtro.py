# from .api import Estado, Municipio, OrgaoExpedidor
from .errors import MandadosNotFoundError
import requests
import concurrent.futures
from itertools import repeat
from .settings import PARAMS_FORCA_BRUTA
from tqdm import tqdm


class Filtro:
    def __init__(self, headers):
        self._mandados_list = []
        self._headers = headers

    def obter_mandados(self) -> list:
        if not self._mandados_list:
            raise MandadosNotFoundError("Você ainda não baixou os mandados. Utilize .baixar_mandados() para baixa-los")
        return self._mandados_list.copy()

    # def __add__(self, val):
    #     if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
    #         raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
    #     return self.obter_mandados() + val.obter_mandados()

    def _request_post(self, params, data):
        """Faz uma requisição do tipo POST e retorna
        um JSON se ela for bem sucedida e um NoneType
        caso contrário"""
        response = requests.post(
            url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
            headers=self._headers,
            params=params,
            data=data
        )
        if response.ok:
            return response.json()
        else:
            print(f"Deu Ruim! POST request não bem sucedida. Status code:{response.status_code}")

    def _obter_data_post(self, id_estado: int, id_municipio: int = "", id_orgao: int = "") -> str:
        """Tem como parâmetros os ids em questão.
        Retorna a variável data necessário para
        fazer uma requisição do tipo POST."""
        if not id_municipio and not id_orgao:
            # Só tem estado!
            return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(id_estado) + '}'
        elif not id_orgao:
            # Tem estado e id_municipio!
            return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(
                id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'
        else:
            # Tem estado, municipio e orgao!
            return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(id_orgao) + '},"idEstado":' + str(
                id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'

    def _obter_post_pag1(self, id_estado: int, id_municipio: int = 0, id_orgao: int = 0, size: int = 10) -> dict:
        """Faz um POST request da primeira página para
        obter até 2.000 elementos. Retorna um dicionário
         e um int com o total de mandados daquele id."""
        params = (
            ('page', '0'),
            ('size', f'{size}'),
            ('sort', 'dataExpedicao,ASC'),
        )

        data = self._obter_data_post(id_estado, id_municipio, id_orgao)

        raw_data = self._request_post(params, data)
        return raw_data

    def _request_post_poucos_mandados(self, response_pag1: dict, id_estado: int, id_municipio: int = 0,
                                      id_orgao: int = 0) -> list:
        """
        Obtém até 10.000 linhas de dados.
        Retorna uma lista de dicts
        :param response_pag1: 'raw_data': dict
        :param id_estado: id que pertence ao intervalo [1,27].
        :param id_municipio: id interno
        :param id_orgao: id interno
        :return: list: lista de dicionários de mandados
        """
        data = self._obter_data_post(id_estado, id_municipio, id_orgao)
        tot_elements = response_pag1.get('totalElements')
        tot_pages = tot_elements // 2000 if tot_elements % 2000 == 0 else tot_elements // 2000 + 1
        params = tuple((('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,ASC')) for x in range(0, tot_pages))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            novos_mandados = list(executor.map(self._request_post, params, repeat(data)))
        return [x for sublist in novos_mandados for x in sublist['content']]  # List unpacking

    def _request_post_expandido(self, response_pag1: dict, id_estado: int, id_municipio: int = 0,
                                id_orgao: int = 0) -> list:
        """
        Aproveita-se da ordenação para extrapolar o
        limite de 10.000 linhas e alcaçar até o dobro disso.
        Retorna uma lista de dicts
        """
        data = self._obter_data_post(id_estado, id_municipio, id_orgao)
        tot_elements = response_pag1['totalElements']
        params = tuple((('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,ASC')) for x in range(0, 5))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            novos_mandados = list(executor.map(self._request_post, params, repeat(data)))
        all_mandados = [x for sublist in novos_mandados for x in sublist['content']]  # List unpacking
        paginas_restantes = (tot_elements - 10000) // 2000
        if paginas_restantes >= 1:
            params = tuple(
                (('page', str(x)), ('size', '2000'),
                 ('sort', 'dataExpedicao,DESC')) for x in range(0, int(paginas_restantes)))
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                novos_mandados = executor.map(self._request_post, params, repeat(data))
            for e in [x['content'] for x in novos_mandados]:
                all_mandados.extend(e)
        params = (('page', str(paginas_restantes)), ('size', '2000'), ('sort', 'dataExpedicao,DESC'))
        ultima_pag = self._request_post(params, data)
        all_mandados.extend([x for x in ultima_pag['content'] if x not in all_mandados])
        return all_mandados

    def _request_post_forcabruta(self, id_estado: int, id_municipio: int, id_orgao: int) -> list:
        """
        Aplica todas as ordenações disponíveis para
        obter o maior número de mandados possíveis,
        mesmo sem conseguir acessar todas as páginas
        do Banco de Dados.
        Retorna uma lista com todos os mandados adquiridos.
        """
        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(id_orgao) + '},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'

        all_mandados = list()

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            novos_mandados = list(
                tqdm(executor.map(self._request_post, PARAMS_FORCA_BRUTA, repeat(data)), total=len(PARAMS_FORCA_BRUTA)))
        for lista_mandados in [x['content'] for x in novos_mandados if x]:
            all_mandados.extend([mandado for mandado in lista_mandados if mandado not in all_mandados])
        return all_mandados

    def _pega_conteudo_completo(self, linha: dict):
        """
        "Entra" em cada um dos mandados com o
        método GET para pegar mais informações
        e salva-nas em json/<id_mandado>.json
        """
        if not isinstance(linha, dict):
            print(f"ERROR: Mandado is {type(linha)}")
            return None
        # HEADERS['user-agent'] = ua.random
        id_mandado = linha.get("id")
        id_tipo_peca = linha.get("idTipoPeca")
        if id_tipo_peca is None:
            id_tipo_peca = linha['tipoPeca'].get('id')

        response = requests.get(
            url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/certidaos/{id_mandado}/{id_tipo_peca}',
            headers=self._headers
        )
        if response.ok:
            return response.json()
            # with open(f"jsons/{response_dict['id']}.json", 'wb') as outf:
            #     outf.write(response.content)
        else:
            print(f"Deu ruim! Status code: {response.status_code}")
            # print("Você está no pega_conteudo_completo")
            # pass

    def _baixar_conteudo_completo_parallel(self, lista_mandados: list) -> list:
        """
        Dada uma lista de mandados, utiliza concorrência
        para salvar cada mandado em um arquivo JSON de
        maneira mais eficiente.
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
        result = list(executor.map(self._pega_conteudo_completo, lista_mandados))
        return [mandado for mandado in result if mandado is not None]
