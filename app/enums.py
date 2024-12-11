from enum import Enum


class ApiMessageEnum(Enum):
    REQUEST_COMPLETED = "Requisição concluída"
    ROUTE_NOT_FOUND = "Rota não encontrada"
    REQUEST_PARAMETER_MISSING = "Faltam parametros na requisição"
    ENDPOINT_ERROR = "Erro de endpoint"
    INVALID_ARGUMENT = "Argumento inválido"
    INVALID_REQUEST = "Requisição inválida"
    ACCESS_DENIED = "Acesso negado"
    UNKNOWN_ERROR = "Erro desconhecido"
    EXTERNAL_UNAVALIABLE_SERVICE = "Servico externo indisponível"
    USER_NOT_FOUND = "Usuário não encontrado"
    EMAIL_EXISTS = "Email existe"
    INVALID_USER_PASSWORD = "Usuário ou senha inválidos"
    NOT_ALLOWED_METHOD = "Método não permitido"