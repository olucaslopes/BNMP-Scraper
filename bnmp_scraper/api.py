import requests
from .settings import *
# from .utils import obter_post_pag1, request_post_poucos_mandados, request_post_expandido, \
#     request_post_forcabruta, baixar_conteudo_completo_parallel
from .errors import MandadosNotFoundError, EstadoNotFoundError
import concurrent.futures
from tqdm import tqdm
from .filtro import Filtro
# from extrator import Extrator


class Estado(Filtro):
    def __init__(self, headers, id_estado: [int, str]):
        super().__init__(headers)
        self._id = self._set_id(id_estado)
        self._init_info = self._obter_post_pag1(self._id)
        self._totalElements = self._init_info['totalElements']
        self._munic_info = {}
        self._munic_objs = []

    def baixar_mandados(self, force: bool = False):
        if self._mandados_list and not force:
            return self._mandados_list
        if self._totalElements <= 20000:
            if self._totalElements <= 10000:
                mandados_parciais = self._request_post_poucos_mandados(self._init_info, self._id)
            else:
                mandados_parciais = self._request_post_expandido(self._init_info, self._id)
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        else:
            municips = self._gerar_municipios()
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
            list(tqdm(executor.map(Municipio.baixar_mandados, municips), total=len(municips)))
            self._mandados_list = [item for munic in municips for item in munic.obter_mandados()]
        print(f"Recuperados {len(self._mandados_list)}/{self._totalElements} mandados")

    def obter_municicipios(self) -> list:
        """
        Retorna uma lista de ids dos municipios dessa uf.
        """
        return list(self._baixar_municipios().keys())

    def _baixar_municipios(self, force: bool = False) -> dict:
        """
        A partir do id da de uma UF retorna um
        dict mapeando todos os municípios dessa
        UF aos seus ids.
        """
        if self._munic_info and not force:
            return self._munic_info
        response_munic = requests.get(
            url=f'https://portalbnmp.cnj.jus.br/scaservice/api/municipios/por-uf/{self._id}',
            headers=HEADERS
        )
        munic_list = response_munic.json()
        self._munic_info = {munic['nome']: munic['id'] for munic in munic_list}
        return self._munic_info

    def _gerar_municipios(self, force: bool = False) -> list:
        """"
        Retorna uma lista de objetos Municipio
        com todos os municípios de um Estado.
        """""
        if self._munic_objs and not force:
            return self._munic_objs
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
        munics_ids = list(self._baixar_municipios().values())  # Pega os ids dos municípios
        munic = list(executor.map(
            lambda munic_id: Municipio(self._headers, self._id, munic_id), munics_ids
        ))  # Cria as instâncias
        self._munic_objs = [m for m in munic if len(m) > 0]
        return self._munic_objs  # retorna somente os municípios que tem mandados

    def _set_id(self, id_estado):
        if isinstance(id_estado, str):
            id_estado = id_estado.upper()
            if id_estado in UF_MAP:
                return UF_MAP[id_estado]
        elif isinstance(id_estado, int):
            if id_estado in NUM_MAP:
                return id_estado
        raise EstadoNotFoundError("id_estado precisa ser a sigla de uma UF ou um número entre 1 e 27")

    def _set_sigla(self):
        return NUM_MAP[self._id]

    def __len__(self):
        return self._totalElements

    def __add__(self, val):
        if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
            raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
        return self.obter_mandados() + val.obter_mandados()

    sigla = property(_set_sigla, None)


class Municipio(Filtro):
    def __init__(self, headers, id_estado: int, id_munic: int):
        super().__init__(headers)
        self._id_estado = id_estado
        self._id = id_munic
        self._init_info = self._obter_post_pag1(self._id_estado, self._id)
        self._totalElements = self._init_info['totalElements']
        self._mandados_list = []
        self._orgaos_info = {}
        self._orgaos_objs = []

    def baixar_mandados(self, force: bool = False):
        if self._mandados_list and not force:
            return self._mandados_list
        if self._totalElements <= 20000:
            if self._totalElements <= 10000:
                mandados_parciais = self._request_post_poucos_mandados(self._init_info, self._id_estado, self._id)
            else:
                mandados_parciais = self._request_post_expandido(self._init_info, self._id_estado, self._id)
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        else:
            orgaos = self._gerar_orgaos()
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
            list(tqdm(executor.map(OrgaoExpedidor.baixar_mandados, orgaos), total=len(orgaos)))
            self._mandados_list = [item for orgao in orgaos for item in orgao.obter_mandados()]
        # print(f"Recuperados {len(self._mandados_list)}/{self._totalElements} mandados")

    def obter_mandados(self) -> list:
        if not self._mandados_list:
            raise MandadosNotFoundError("Você ainda não baixou os mandados. Utilize .baixar_mandados() para baixa-los")
        return self._mandados_list.copy()

    def _baixar_orgaos(self, force: bool = False) -> dict:
        """
        A partir do id da de um município retorna
        um dict mapeando todos os Órgãos Expeditores
        desse município aos seus ids.
        """
        if self._orgaos_info and not force:
            return self._orgaos_info
        response_org = requests.get(
            url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/orgaos/municipio/{self._id}',
            headers=HEADERS
        )
        org_list = response_org.json()
        return {org['nome']: org['id'] for org in org_list}

    def obter_orgaos(self) -> list:
        """
        Retorna uma lista de ids dos municipios dessa uf.
        """
        return list(self._baixar_orgaos().keys())

    def _gerar_orgaos(self, force: bool = False) -> list:
        """"
        Retorna uma lista de objetos Municipio
        com todos os municípios de um Estado.
        """""
        if self._orgaos_objs and not force:
            return self._orgaos_objs
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
        orgaos_ids = list(self._baixar_orgaos().values())  # Pega os ids dos órgãos expedidores
        org = list(executor.map(
            lambda org_id: OrgaoExpedidor(self._headers, self._id_estado, self._id, org_id), orgaos_ids
        ))  # Cria as instâncias
        return [o for o in org if len(o) > 0]  # retorna somente os orgaos que tem mandados

    def __len__(self):
        return self._totalElements

    def __add__(self, val):
        if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
            raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
        return self.obter_mandados() + val.obter_mandados()


class OrgaoExpedidor(Filtro):
    def __init__(self, headers, id_estado, id_munic, id_orgao):
        super().__init__(headers)
        self._id_estado = id_estado
        self._id_munic = id_munic
        self._id = id_orgao
        self._init_info = self._obter_post_pag1(self._id_estado, self._id_munic, self._id)
        self._totalElements = self._init_info['totalElements']
        self._mandados_list = []

    def baixar_mandados(self, force: bool = False):
        if self._mandados_list and not force:
            return self._mandados_list
        if self._totalElements <= 20000:
            if self._totalElements <= 10000:
                mandados_parciais = self._request_post_poucos_mandados(
                    self._init_info, self._id_estado, self._id_munic, self._id
                )
            else:
                mandados_parciais = self._request_post_expandido(
                    self._init_info, self._id_estado, self._id_munic, self._id
                )
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        else:
            mandados_parciais = self._request_post_forcabruta(self._id_estado, self._id_munic, self._id)
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        # print(f"Recuperados {len(self._mandados_list)}/{self._totalElements} mandados")

    def obter_mandados(self) -> list:
        if not self._mandados_list:
            raise MandadosNotFoundError("Você ainda não baixou os mandados. Utilize .baixar_mandados() para baixa-los")
        return self._mandados_list.copy()

    def __len__(self):
        return self._totalElements

    def __add__(self, val):
        if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
            raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
        return self.obter_mandados() + val.obter_mandados()
