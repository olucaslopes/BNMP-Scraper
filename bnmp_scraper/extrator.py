from .api import Estado, Municipio
from .settings import UF_MAP, NUM_MAP
from .errors import EstadoNotFoundError, MunicipioNotFoundError
import string


class BnmpScraper:
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
        _id = self._set_id_estado(sigla)
        return Estado(self._headers, _id)

    def municipio(self, sigla_estado, nome_municipio):
        def clean_string(name):
            name = name.lower()
            ascii_map = {'á': 'a', 'â': 'a', 'à': 'a', 'ã': 'a', 'é': 'e', 'ê': 'e', 'è': 'e', 'ẽ': 'e', 'í': 'i',
                         'î': 'i', 'ì': 'i', 'ĩ': 'i', 'ó': 'o', 'ô': 'o', 'ò': 'o', 'õ': 'o', 'ú': 'u', 'û': 'u',
                         'ù': 'u', 'ũ': 'u', 'ç': 'c'}
            result = ''
            for e in name:
                if e in string.ascii_lowercase:
                    result += e
                elif e in ascii_map:
                    result += ascii_map[e]
            return result

        estado = self.estado(sigla_estado)
        orig_munic_map = estado.obter_municicipios(ids=True)
        munic_map = {clean_string(munic): orig_munic_map[munic] for munic in orig_munic_map}
        nome_municipio = clean_string(nome_municipio)
        if nome_municipio in munic_map:
            reverse_munic_map = {value: key for key, value in orig_munic_map.items()}
            _id_munic = munic_map[nome_municipio]
            return Municipio(self._headers,
                             self._set_id_estado(sigla_estado),
                             _id_munic,
                             nome=reverse_munic_map[_id_munic])
        raise MunicipioNotFoundError('Município não encontrado')

    def _set_id_estado(self, id_estado):
        if isinstance(id_estado, str):
            id_estado = id_estado.upper()
            if id_estado in UF_MAP:
                return UF_MAP[id_estado]
        elif isinstance(id_estado, int):
            if id_estado in NUM_MAP:
                return id_estado
        raise EstadoNotFoundError("id_estado precisa ser a sigla de uma UF ou um número entre 1 e 27")
