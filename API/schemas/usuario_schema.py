from pydantic import BaseModel
from typing import List
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuario a ser inserido deve ser representado
    """
    name: str = "Roberto"
    time_spent_alone: int = 5  # Horas passadas sozinho diariamente (0–11)
    stage_fear: str = "Yes"  # Presença de medo de palco (Sim/Não)
    social_event_attendance: int = 5
    going_outside: int = 2  # Frequência com que sai de casa (0–7).
    drained_after_socializing: str = "Yes"  # Sensação de exaustão após socializar (Sim/Não).
    friends_circle_size: int = 2  # Número de amigos próximos (0–15).
    post_frequency: int = 1  # Frequência de postagens nas redes sociais (0–10).


class UsuarioViewSchema(BaseModel):
    """ Define como um novo usuario a ser inserido deve ser representado
    """
    id: int = 1
    name: str = "Roberto"
    time_spent_alone: int = 5  # Horas passadas sozinho diariamente (0–11)
    stage_fear: str = "Yes"  # Presença de medo de palco (Sim/Não)
    social_event_attendance: int = 5  # Frequência de participação em eventos sociais (0–10)
    going_outside: int = 2  # Frequência com que sai de casa (0–7).
    drained_after_socializing: str = "Yes"  # Sensação de exaustão após socializar (Sim/Não).
    friends_circle_size: int = 2  # Número de amigos próximos (0–15).
    post_frequency: int = 1  # Frequência de postagens nas redes sociais (0–10).
    personality: str = None  # Variável alvo (Extrovertido (0) /Introvertido (1)).


class UsuarioBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do usuario.
    """
    name: str = "Roberto"


class ListaUsuariosSchema(BaseModel):
    """Define como uma lista de usuarios será representada
    """
    usuarios: List[UsuarioSchema]


class UsuarioDelSchema(BaseModel):
    """Define como um usuario para ser deletado será representado
    Será feito com base no nome do usuario.
    """
    name: str = "Roberto"


def apresenta_usuario(usuario: Usuario):
    ''' Retorna representação do usuario seguind o schema de
        UsuarioViewSchema
    '''
    return {
        "id": usuario.id,
        "name": usuario.name,
        "time_spent_alone": usuario.time_spent_alone,
        "stage_fear": usuario.stage_fear,
        "social_event_attendance": usuario.social_event_attendance,
        "going_outside": usuario.going_outside,
        "drained_after_socializing": usuario.drained_after_socializing,
        "friends_circle_size": usuario.friends_circle_size,
        "post_frequency": usuario.post_frequency,
        "personality": usuario.personality
    }


def apresenta_usuarios(usuarios: List[Usuario]):
    '''Retorna uma lista de todos os usuarios seguindo o schema de
        UsuarioViewSchema
    '''
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "name": usuario.name,
            "time_spent_alone": usuario.time_spent_alone,
            "stage_fear": usuario.stage_fear,
            "social_event_attendance": usuario.social_event_attendance,
            "going_outside": usuario.going_outside,
            "drained_after_socializing": usuario.drained_after_socializing,
            "friends_circle_size": usuario.friends_circle_size,
            "post_frequency": usuario.post_frequency,
            "personality": usuario.personality
        })

    return {"usuarios": result}