from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from model.vinho import VinhoModel


class VinhoSchema(BaseModel):
    """ Define como um novo vinho a ser inserido deve ser representado
    """
    vinho: str
    uva: str
    safra: str 

class ListagemVinhosSchema(BaseModel):
    """ Define como uma listagem de vinhos será retornada.
    """
    vinhos:List[VinhoSchema]


def apresenta_vinhos(vinhos: List[VinhoModel], token: str) -> Dict[str, Any]:
    """ Retorna uma representação do vinho seguindo o schema definido em
        ProdutoViewSchema, além de exigir um token de autenticação.
    """
    result = []
    for vinho in vinhos:
        result.append({
            "vinho": vinho.vinho,
            "uva": vinho.uva,
            "safra": vinho.safra
        })

    return {"vinhos": result, "token": token}

def apresenta_vinho(vinho: VinhoModel):
    """ Retorna uma representação do vinho seguindo o schema definido em
        VinhoViewSchema.
    """
    return {
       "vinho": vinho.vinho,
        "uva": vinho.uva,
        "safra": vinho.safra
    }
    
class VinhoViewSchema(BaseModel):
    """ Define como um vinho será retornado: vinho 
    """
    vinho: str = "Sociedade Vinícola Rio-Grandense - Cabernet Franc 1951"
    uva: str = "Cabernet Franc"
    safra: str = "1951"