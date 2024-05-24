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

    def add_product(self, data):
        with Session(self.engin) as session:
            new_product = Product(**data)
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            return self.dictdump(new_product)


    def update_product(self, product_id, **data):
        with Session(self.engin) as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return None
            for attr in data:
                if hasattr(product, attr):
                    setattr(product, attr, data[attr])

            session.add(product)
            session.commit()
            return product

    def delete_product(self, product_id):
        with Session(self.engin) as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return None
            elif product.sizes:
                raise Exception("Unable to delete product that has multiple sizes")
            session.delete(product)
            session.commit()

            return product_id


    def get_size(self, size_id = 0):
        with Session(self.engin) as session:
            size =  session.query(Size).filter_by(id = size_id).first()
            if size:
                size_dict = self.dictdump(size)
                return size_dict

            return {}

    def update_size(self, size_id, **data):
        with Session(self.engin) as session:
            size = session.query(Size).filter_by(id = size_id).first()
            if not size:
                return None

            for attr in data:
                if hasattr(size, attr):
                    setattr(size, attr, data[attr])

            session.add(size)
            session.commit()
            return size


    def delete_size(self, size_id):
        with Session(self.engin) as session:
            size = session.query(Size).filter_by(id=size_id).first()
            if not size:
                return None
            session.delete(size)
            session.commit()

            return size_id

    def get_product_sizes(self, product_id = 0):
        with Session(self.engin) as session:
            sizes = session.query(Size).filter_by(product_id = product_id).all()
            if sizes:
                sizes_dict = self.dictdump(sizes)
                return sizes_dict
            return []

    def add_size(self, product_id, data):
        data["product_id"] = product_id
        with Session(self.engin) as session:
            new_size = Size(**data)
            session.add(new_size)
            session.commit()
            session.refresh(new_size)
            return self.dictdump(new_size)


    def add_sizes(self, sizes):
        with Session(self.engin) as session:
            session.add_all(sizes)
            session.commit()

            return len(sizes)


    def add_items(self, items):
        with Session(self.engin) as session:
            session.add_all(items)
            session.commit()

            return len(items)


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

                return  list(sorted(items, lambda i: i['expire_date'], reverse=True))

            return []


    def get_all_items(self):
        with Session(self.engin) as session:
            items = session.query(Item,Size,Product).join(Size, Item.size_id == Size.id).join(Product, Size.product_id == Product.id).all()
            if items:
                new_items = []
                for item in items:
                    new_item = self.dictdump(item[0])
                    new_item.pop('size_id')
                    size = item[1]
                    new_item['size'] = size.size
                    new_item['sku'] = size.sku

                    product = item[2]
                    new_item['product'] = product.name
                    new_item['product_description'] = product.description

                    new_items.append(new_item)
                return new_items
            return []


    def get_single_item(self, item_id = 0):
        with Session(self.engin) as session:
            item = session.query(Item).filter_by(id = item_id).order_by(Item.expire_date.desc()).first()
            if item:
                return self.dictdump(item)
            return {}


    def add_single_item(self, **data):
        with Session(self.engin) as session:
            item = Item(**data)
            session.add(item)
            session.commit()
            session.refresh(item)

            return item


    def update_item(self, item_id, **data):
        with Session(self.engin) as session:
            item = session.query(Item).filter_by(id = item_id).first()
            if not item:
                return None

            for attr in data:
                if hasattr(item, attr):
                    setattr(item, attr, data[attr])

            session.add(item)
            session.commit()
            return item

    def delete_item(self, item_id):
        with Session(self.engin) as session:
            item = session.query(Item).filter_by(id=item_id).first()
            if not item:
                return None
            session.delete(item)
            session.commit()

            return item_id



