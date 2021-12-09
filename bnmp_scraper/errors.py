class CookieOutDatedError(Exception):
    """O cookie está expirado"""
    pass


class InvalidCookieError(Exception):
    """O cookie passado não é válido"""
    pass


class MandadosNotFoundError(Exception):
    """Os mandados para a tarefa executada não foram encontrados"""
    pass


class EstadoNotFoundError(Exception):
    """O input passado não encontrou nenhum estado"""
    pass


class MunicipioNotFoundError(Exception):
    """O input passado não encontrou nenhum município"""
    pass
