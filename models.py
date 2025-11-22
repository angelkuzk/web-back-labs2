from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Office(db.Model):
    __tablename__ = 'offices'
    
    number = db.Column(db.Integer, primary_key=True)
    tenant = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'number': self.number,
            'tenant': self.tenant,
            'price': self.price
        }