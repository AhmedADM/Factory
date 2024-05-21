import decimal
import enum

from datetime import datetime
from sqlalchemy import Column, create_engine, DateTime, Enum, Integer, ForeignKey,  String
from sqlalchemy.orm import DeclarativeBase, Mapped, raiseload, relationship, Session, subqueryload
from sqlalchemy.orm.collections import  InstrumentedList
from sqlalchemy.sql import func
from typing import List


class Base(DeclarativeBase):
    pass


class ProductStatus(enum.Enum):
    Available = 1
    Sold = 2


class Product(Base):
    __tablename__ = "product"

    id = Column( Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    source = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    sizes = relationship("Size", lazy="subquery")


class Size(Base):
    __tablename__ = "product_size"
    id = Column( Integer,primary_key=True, autoincrement=True, nullable=False)
    sku = Column(String(100), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    size = Column(String(100), nullable=False)
    description = Column(String[200], nullable=False)
    price = Column(Integer, nullable=False)
    # items =  relationship("Item", lazy="subquery")



class Item(Base):
    __tablename__ = "product_item"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    size_id = Column(Integer, ForeignKey("product_size.id"), nullable=False)
    issue_date: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    expire_date: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(ProductStatus))



class FactoryDB():
    def __init__(self, connection_str):
        self.engin = create_engine(connection_str, echo=True)
        Base.metadata.create_all(self.engin)

    def dictdump(self, object, exclude_list = []):
        if object is None:
            return None
        
        if type(object) != list:
        
            output_dict = object.__dict__
    
            if  '_sa_instance_state' in output_dict:
                output_dict.pop('_sa_instance_state')

            for exclude in exclude_list:
                if hasattr(output_dict, exclude):
                    output_dict.pop(exclude)

            for attribute in output_dict:
                if hasattr(output_dict[attribute], '_sa_instance_state'):
                    output_dict[attribute] = self.dictdump(output_dict[attribute], exclude_list)
                elif type(output_dict[attribute]) == InstrumentedList:
                    attribute_list = output_dict[attribute]
                    new_list = []
    
                    for sub_attribute in attribute_list:
                        new_sub_attribute = self.dictdump(sub_attribute, exclude_list)
                        new_list.append(new_sub_attribute)
    
                    output_dict[attribute] = new_list

                elif type(output_dict[attribute]) == ProductStatus:
                    output_dict[attribute] = output_dict[attribute].name

                elif type(output_dict[attribute]) == decimal.Decimal:
                    output_dict[attribute] = float(output_dict.get(attribute, 0.0))
                elif type(output_dict[attribute]) == datetime:
                    output_dict[attribute] = str(output_dict.get(attribute))

            return output_dict
        else:
            output_list = []
            for item in object:
                output_list.append(self.dictdump(item))

            return  output_list
            
            



    def get_product(self, id = 0, join = False):
        with Session(self.engin) as session:

            if join:
                product = session.query(Product).filter_by(id = id).first()
            else:
                product = session.query(Product).options(raiseload("*")).filter_by(id = id).first()
            if product:
                product_dict = self.dictdump(product)
                return product_dict
            return {}

    def get_product_sizes(self, product_id = 0):
        with Session(self.engin) as session:
            sizes = session.query(Size).filter_by(product_id = product_id).all()
            if sizes:
                size_dict = self.dictdump(sizes)
                return size_dict
            return []


    def get_product_items(self, product_id=0):
        with Session(self.engin) as session:
            sizes = self.get_product_sizes(product_id)
            items = []
            if sizes:
                for size in  sizes:
                    size_items = session.query(Item).filter_by(size_id = size.get('id')).all()
                    size_items_dict = self.dictdump(size_items)
                    print(size_items_dict)
                    items += size_items_dict

                return  items

            return []



