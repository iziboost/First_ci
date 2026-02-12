from sqlalchemy import Column, Integer, String

from hw1.database import Base


class Recipe(Base):
    __tablename__ = "Recipe"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    time_min = Column(Integer, index=True)
    ingredients = Column(String)
    description = Column(String)
    amount_views = Column(Integer, index=True, default=0)

    def increment_view(self):
        self.amount_views += 1
