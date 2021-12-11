from .settings import UF_MAP, NUM_MAP
from .errors import EstadoNotFoundError


def set_id_estado(id_estado: [int, str]):
    """
    Verifica se id_estado é uma str com a sigla
    de uma UF ou um int de 1 a 27 e retorna um int,
    que é a representação interna de uma UF.
    Caso id_estado não seja válido, sobe um erro.
    """
    if isinstance(id_estado, str):
        id_estado = id_estado.upper()
        if id_estado in UF_MAP:
            return UF_MAP[id_estado]
    elif isinstance(id_estado, int):
        if id_estado in NUM_MAP:
            return id_estado
    raise EstadoNotFoundError("id_estado precisa ser a sigla de uma UF ou um número entre 1 e 27")


def obter_data_post(id_estado: int, id_municipio: int = "", id_orgao: int = "") -> str:
    """Tem como parâmetros os ids em questão.
    Retorna a variável data necessário para
    fazer uma requisição do tipo POST."""
    if not id_municipio and not id_orgao:
        # Só tem estado!
        return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(id_estado) + '}'
    elif not id_orgao:
        # Tem estado e município!
        return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'
    else:
        # Tem estado, município e órgão!
        return '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(id_orgao) + '},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'
