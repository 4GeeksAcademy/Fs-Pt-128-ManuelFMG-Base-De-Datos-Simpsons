from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites_characters_table = Table(
    "favoritesCharacters",
    db.metadata,
    Column("user", ForeignKey("user.id")),
    Column("characters", ForeignKey("characters.id"))
)


favorites_locations_table = Table(
    "favoritesLocations",
    db.metadata,
    Column("user", ForeignKey("user.id")),
    Column("locations", ForeignKey("locations.id"))
)




class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favoritesCharacters: Mapped [list["Characters"]] = relationship(
        "Characters",
        secondary = favorites_characters_table,
        back_populates = 'favorite_by'

    )

    favoritesLocations: Mapped [list["Locations"]] = relationship(
        "Locations",
        secondary = favorites_locations_table,
        back_populates = 'favorite_by'

    )
    

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "favorites": [characters.serialize() for characters in self.favorites]
            
        }
    
class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[str] = mapped_column(String(20), nullable=False)
    ocupation: Mapped[str] = mapped_column(String(50), nullable=False)
    image: Mapped[str] = mapped_column(String(200), nullable=False)
    phrases: Mapped[str] = mapped_column(String(200), nullable=False)
    favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary = favorites_characters_table,
        back_populates = 'favoritesCharacters'
    )
    


    def serialize(self):
        return {
            "id": self.id,
            "age": self.age,
            "occupation": self.occupation,
            "phrases": self.phrases,
            "image": self.image
            
        }
    
class Locations(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    town: Mapped[str] = mapped_column(String(20), nullable=False)
    image: Mapped[str] = mapped_column(String(200), nullable=False)
    favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary = favorites_locations_table,
        back_populates = 'favoritesLocations'
    )
    
    


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "town": self.town,
            "image": self.image
            
        }
