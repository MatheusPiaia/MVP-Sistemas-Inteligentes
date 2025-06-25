from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column("pk_id", Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    time_spent_alone = Column(Integer)
    stage_fear = Column(String(3))
    social_event_attendance = Column(Integer)
    going_outside = Column(Integer)
    drained_after_socializing = Column(String(3))
    friends_circle_size = Column(Integer)
    post_frequency = Column(Integer)
    personality = Column(String)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, name: str, time_spent_alone: int, stage_fear: str,
                 social_event_attendance: int, going_outside: int,
                 drained_after_socializing: str, friends_circle_size: int,
                 post_frequency: int, personality: str,
                 data_insercao: Union[DateTime, None] = None):
        
        '''
        Cria um usuario
        Atributos:
        name: str = "Roberto"
        time_spent_alone: Horas passadas sozinho diariamente (0–11)
        stage_fear: Presença de medo de palco (Sim/Não)
        social_event_attendance: Frequência de participação em eventos sociais (0–10)
        going_outside: Frequência com que sai de casa (0–7).
        drained_after_socializing: Sensação de exaustão após socializar (Sim/Não).
        friends_circle_size: Número de amigos próximos (0–15).
        post_frequency: Frequência de postagens nas redes sociais (0–10).
        personality: Variável alvo (Extrovertido /Introvertido).
        '''

        self.name = name
        self.time_spent_alone = time_spent_alone
        self.stage_fear = stage_fear
        self.social_event_attendance = social_event_attendance
        self.going_outside = going_outside
        self.drained_after_socializing = drained_after_socializing
        self.friends_circle_size = friends_circle_size
        self.post_frequency = post_frequency
        self.personality = personality

        if data_insercao:
            self.data_insercao = data_insercao