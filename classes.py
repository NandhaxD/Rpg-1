from init_session import session, Base
import asyncio
from sqlalchemy import Column, Integer, String, select


class Enemy:
    def __init__(self, id):
        enemy = session.execute(select(Mobs).where(Mobs.MobID == int(id))).one()
        self.name = enemy.Mobs.MobName
        self.hp = enemy.Mobs.HP
        self.attack = enemy.Mobs.Attack
        self.armour = enemy.Mobs.Armour
        self.m_armour = enemy.Mobs.MagicArmour
        self.xp = enemy.Mobs.XP
        self.attack_type = enemy.Mobs.AttackType
        self.money = enemy.Mobs.Money

class Timer:

    async def start(self):
        await asyncio.sleep(60)
        if not self.answer:
            return False
        else:
            return True

    def __init__(self):
        self.answer = False


class Persons(Base):
    __tablename__ = 'Persons'  # table name
    UserID = Column(Integer, name='UserID', primary_key=True)
    Nickname = Column(String)
    Level = Column(Integer)
    HP = Column(Integer)
    CurHP = Column(Integer)
    Money = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    XP = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    LocationID = Column(Integer)


class Mobs(Base):
    __tablename__ = 'Mobs'  # table name
    MobID = Column(Integer, primary_key=True)
    MobName = Column(String)
    HP = Column(Integer)
    XP = Column(Integer)
    Money = Column(Integer)
    ReqLevel = Column(Integer)
    AttackType = Column(String)
    Attack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)


class Locations(Base):
    __tablename__ = 'Locations'
    LocationID = Column(Integer, primary_key=True)
    LocationName = Column(String)
    XCoord = Column(Integer)
    YCoord = Column(Integer)
    LocationType = Column(String)


class Items(Base):
    __tablename__ = 'Items'
    ItemID = Column(Integer, primary_key=True)
    Name = Column(String)
    Cost = Column(Integer)
    CostToSale = Column(Integer)
    ItemType = Column(String)
    HP = Column(Integer)
    Mana = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    ReqLevel = Column(Integer)
    Availability = Column(Integer)


class Inventory(Base):
    __tablename__ = 'Inventory'
    UserID = Column(Integer, primary_key=True)
    Nickname = Column(String)
    ItemID = Column(Integer)
    Quantity = Column(Integer)  # positive - there are several such things in the inventory, one of them is worn
    # negative - several in inventory, not worn
