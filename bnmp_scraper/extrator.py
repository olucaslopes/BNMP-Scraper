from .api import Estado, Municipio
from .errors import InvalidCookieError, CookieOutDatedError, MunicipioNotFoundError
from .utils import set_id_estado
import string


class BnmpScraper:
    def __init__(self, cookie):
        if cookie[:11] != 'portalbnmp=':
            raise InvalidCookieError("O cookie que você passou não é válido.")
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

    def estado(self, sigla: [int, str]) -> Estado:
        """
        Extrai todos os mandados da UF selecionada
        e armazena-os na instância da classe Estado.

        Parameters
        ----------
        sigla : int or str
            str com dois caracteres representando a sigla de uma UF ou
            um int de 1 a 27. São ignoradas letras maiúsculas e minúsculas.

        Notes
        -----
        Para obter uma lista com as informações dos mandados, utilize .data
        após baixar os mandados.
        """
        _id = set_id_estado(sigla)
        try:
            return Estado(self._headers, _id)
        except TypeError:
            raise CookieOutDatedError("O cookie que você passou está expirado! \
            \nPor favor, redefina o extrator com outro cookie.")

    def municipio(self, sigla_estado, nome_municipio):
        """
        Extrai todos os mandados do município selecionado
        e armazena-os na instância da classe Estado.

        Parameters
        ----------
        sigla_estado : int or str
            str com dois caracteres representando a sigla de uma UF ou
            um int de 1 a 27.

        nome_municipio : str
            str com o nome do município ao qual os dados serão extraidos.
            São ignorados acentos e letras maiúsculas e minúsculas.

        Notes
        -----
        Para obter uma lista com as informações dos mandados, utilize .data
        após baixar os mandados.
        """
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
            try:
                return Municipio(self._headers,
                                 set_id_estado(sigla_estado),
                                 _id_munic,
                                 nome=reverse_munic_map[_id_munic])
            except TypeError:
                raise CookieOutDatedError("O cookie que você passou está expirado! \
                \nPor favor, redefina o extrator com outro cookie.")
        raise MunicipioNotFoundError('Município não encontrado')
