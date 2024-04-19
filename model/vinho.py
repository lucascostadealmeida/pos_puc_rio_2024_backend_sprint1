from sql_alchemy import banco


class VinhoModel(banco.Model):
    __tablename__ = 'vinhos'

    vinho_id = banco.Column(banco.Integer, primary_key=True)
    vinho = banco.Column(banco.String(40), nullable=False)
    uva = banco.Column(banco.String(40), nullable=False)
    safra = banco.Column(banco.String(40), nullable=False)
    
    def __init__(self, vinho, uva, safra, vinho_id=None):
        self.vinho_id = vinho_id
        self.vinho = vinho
        self.uva = uva
        self.safra = safra
      
    def json(self):
        return {
            'vinho_id': self.vinho_id,
            'vinho': self.vinho,
            'uva': self.uva,
            'safra': self.safra,
        }

    @classmethod
    def find_vinho(cls, vinho_id):
        vinho = cls.query.filter_by(vinho_id=vinho_id).first()
        if vinho:
            return vinho
        return None

    @classmethod
    def find_by_vinhoName(cls, vinho):
        vinho = cls.query.filter_by(vinho=vinho).first()
        if vinho:
            return vinho
        return None

    def save_vinho(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_vinho(self):
        banco.session.delete(self)
        banco.session.commit()
