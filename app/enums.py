from enum import Enum


class ApiMessageEnum(Enum):
    REQUEST_COMPLETED = "Requisição concluída"
    ROUTE_NOT_FOUND = "Rota não encontrada"
    REQUEST_PARAMETER_MISSING = "Faltam parâmetros na requisição"
    ENDPOINT_ERROR = "Erro de endpoint"
    INVALID_ARGUMENT = "Argumento inválido"
    INVALID_REQUEST = "Requisição inválida"
    ACCESS_DENIED = "Acesso negado"
    UNKNOWN_ERROR = "Erro desconhecido"
    EXTERNAL_UNAVAILABLE_SERVICE = "Serviço externo indisponível"
    NOT_ALLOWED_METHOD = "Método não permitido"
    INVALID_TOKEN = "Token invalido"
    EXPIRED_TOKEN = "Token expirado"
    USER_NOT_FOUND = "Usuário não encontrado"
    USER_EMAIL_EXISTS = "Já existe um usuário com esse email"
    INVALID_USER_PASSWORD = "Usuário ou senha inválidos"
    USER_PASSWORD_MANDATORY = "A senha é obrigatória"
    USER_PASSWORDS_DO_NOT_MATCH = "As senhas não coincidem"
