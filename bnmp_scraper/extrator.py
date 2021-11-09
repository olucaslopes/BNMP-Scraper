from .api import Estado  # , Municipio, OrgaoExpedidor
from .settings import UF_MAP, NUM_MAP
from .errors import EstadoNotFoundError


class Extrator:
    def __init__(self, cookie):
        self._headers = {
            'authority': 'portalbnmp.cnj.jus.br',
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko)\
     Chrome/24.0.1309.0 Safari/537.17',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://portalbnmp.cnj.jus.br',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://portalbnmp.cnj.jus.br/',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': cookie,
        }

    def estado(self, sigla: [int, str]):
        if isinstance(sigla, str):
            sigla = sigla.upper()
            if sigla in UF_MAP:
                return Estado(self._headers, UF_MAP[sigla])
        elif isinstance(sigla, int):
            if sigla in NUM_MAP:
                return Estado(self._headers, sigla)
        raise EstadoNotFoundError("id_estado precisa ser a sigla de uma UF ou um número entre 1 e 27")
