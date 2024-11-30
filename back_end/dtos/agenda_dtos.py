from pydantic import BaseModel, validator
from typing import Optional, ClassVar  # Importa ClassVar
from datetime import date, datetime
import calendar

class Agendamento(BaseModel):
    ano: int
    mes: int
    dia: int
    hora: str
    turno: Optional[str] = None

    # Atributo da classe, não de instância
    MESES: ClassVar[dict[str, int]] = {
        "jan": 1, "fev": 2, "mar": 3, "abr": 4,
        "mai": 5, "jun": 6, "jul": 7, "ago": 8,
        "set": 9, "out": 10, "nov": 11, "dez": 12
    }

    @validator('mes', pre=True)
    def validar_mes(cls, mes):
        if isinstance(mes, str):
            mes = mes.strip().lower()[:3]
            if mes in cls.MESES:
                return cls.MESES[mes]
            raise ValueError("O mês deve ser um número de 1 a 12 ou um nome válido como 'Jan', 'Fev'.")
        if mes < 1 or mes > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        return mes

    @validator('ano')
    def validar_ano(cls, ano):
        ano_atual = datetime.now().year
        if ano < ano_atual:
            raise ValueError("O ano não pode ser menor que o ano atual.")
        return ano

    @validator('dia')
    def validar_dia(cls, dia, values):
        if 'mes' in values and 'ano' in values:
            ano = values['ano']
            mes = values['mes']
            ultimo_dia = calendar.monthrange(ano, mes)[1]
            if dia < 1 or dia > ultimo_dia:
                raise ValueError(
                    f"O dia não é válido para o mês e ano fornecidos. Dias válidos de 1 a {ultimo_dia}."
                )
        return dia

    @validator('hora')
    def validar_hora(cls, hora):
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            raise ValueError("A hora deve estar no formato HH:MM.")
        return hora




    # # Função para converter a string de data em um objeto datetime
    # def converte_str_datetime(self):
    #     meses = {
    #         'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
    #         'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
    #     }
    #     try:
    #         mes_num = meses[self.mes.lower()]  # Converte o mês para número
    #         data = datetime(int(self.ano), mes_num, self.dia)  # Converte a data
    #         return data
    #     except KeyError:
    #         raise ValueError(self.mes.lower())  # Apenas retorna o nome do mês em minúsculo
    #     except ValueError as e:
    #         raise ValueError(str(e))  # Retorna o erro como string sem mensagem adicional

    # @validator('mes')
    # def validar_mes(cls, mes):
    #     meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    #     if mes not in meses_validos:
    #         formatos_validos = ", ".join([f'"{m}"' for m in meses_validos])
    #         raise ValueError(f"inválido ou ausente, formatos válidos [{formatos_validos}]")
    #     return mes

    # @validator('dia')
    # def validar_dia(cls, dia, values):
    #     ano = values.get("ano")
    #     mes = values.get("mes")

    #     if not ano or not mes:
    #         return dia

    #     # Mapeamento do mês para número
    #     meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    #     mes_num = meses_validos.index(mes) + 1

    #     # Verifica o número de dias válidos para o mês e ano
    #     max_dias = monthrange(ano, mes_num)[1]

    #     if dia < 1 or dia > max_dias:
    #         raise ValueError(f"inválido ou ausente. Para o mês de {mes}, o dia deve ser entre 1 e {max_dias}.")

    #     return dia


class UsuarioAgendamento(Agendamento):
    usuario_id: Optional[int] = None


class AgendamentoResposta(Agendamento):
    data_criacao: str  # Vai ser retornada como string
    message: str = "Horário criado com sucesso!"

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        # Certifica-se que a data seja formatada corretamente para o formato DD/MM/YYYY
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v


class AgendaOcupadaResposta(UsuarioAgendamento):
    data_criacao: str
    message: str = "Agendamento realizado com sucesso."

    class Config:
        from_attributes = True  # Atualização para Pydantic V2
