from enum import Enum

# Essa classe de satus é para o Model, para retornar se houve falha ou sucesso

# Ela é ultizada em Model.py

class StatusResposta(Enum):
    sucesso=1
    falha=0