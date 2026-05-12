from app import db
from app.models.base import BaseModel

class InventoryTransaction(BaseModel):
    __tablename__ = "inventory_transactions"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)

    product = db.relationship("Product", backref=db.backref("transactions", passive_deletes=True))