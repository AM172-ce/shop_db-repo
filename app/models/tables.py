from sqlalchemy import (
    Column, String, BigInteger, Integer, Numeric, Text,
    text, ForeignKey, Boolean, TIMESTAMP, Identity)
from sqlalchemy.orm import relationship
from app.database import Base




class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'production'}
    
    product_code = Column(String(15), primary_key=True, default=None, server_default=text("set_product_code()"))
    product_name = Column(String(70), nullable=False)
    product_vendor = Column(String(50), nullable=False)
    product_description = Column(Text, nullable=False)
    quantity_in_stock = Column(BigInteger, nullable=False)
    product_category_code = Column(String(15), ForeignKey('production.product_categories.product_category_code'))
    is_deleted = Column(Boolean, default=False)

    pricings = relationship("Product_Pricing", backref="product")
    comments = relationship("Product_Comment", backref="product")

class Product_Pricing(Base):
    __tablename__ = 'products_pricing'
    __table_args__ = {'schema': 'production'}
    
    
    products_pricing_code = Column(BigInteger, primary_key=True, default=None, server_default=text("set_pricing_code()"))
    product_code = Column(String(15), ForeignKey('production.products.product_code'), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    date_expiry = Column(TIMESTAMP)
    in_active = Column(Boolean, nullable=False)
    msrp = Column(Numeric(10, 2), nullable=False)

class Discount_unit(Base):
    __tablename__ = 'discount_units'
    __table_args__ = {'schema': 'production'}

    discount_unit_code = Column(String(1), primary_key=True)
    discount_unit_name = Column(String(15), nullable=False)


class Product_Discount(Base):
    __tablename__ = 'products_discount'
    __table_args__ = {'schema': 'production'}

    product_discount_code = Column(BigInteger, primary_key=True, default=None, server_default=text("set_discount_code()"))
    product_code = Column(String(15), ForeignKey('production.products.product_code'), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    discount_unit = Column(String(1), ForeignKey('production.discount_units.discount_unit_code'), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    discount_description = Column(Text)
    in_active = Column(Boolean, default=True)

class Product_Comment(Base):
    __tablename__ = 'products_comments'
    __table_args__ = {'schema': 'production'}
    
    product_code = Column(String(15), ForeignKey('production.products.product_code'), primary_key=True)
    customer_number = Column(BigInteger, ForeignKey('customers.customer_number'), primary_key=True)
    comments = Column(Text)
    rates = Column(Integer, nullable=False)


class Product_Category(Base):
    __tablename__ = 'product_categories'
    __table_args__ = {'schema': 'production'}
    
    product_category_code = Column(String(15), primary_key=True)
    category_name = Column(String(70), nullable=False)
    product_category_description = Column(Text)
    parent_category_code = Column(String(15), ForeignKey('production.product_categories.product_category_code'))


class Product_Categories_Discount(Base):
    __tablename__ = 'product_categories_discount'
    __table_args__ = {'schema': 'production'}

    product_categories_discount_code = Column(BigInteger, primary_key=True)
    product_categories_code = Column(String(15), ForeignKey('production.product_categories.product_category_code'), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    discount_unit = Column(String(1), ForeignKey('production.discount_units.discount_unit_code'), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    discount_description = Column(Text)
    in_active = Column(Boolean, default=True)


########################## public schema ###########################

class Office(Base):
    __tablename__ = 'offices'
    __table_args__ = {'schema': 'public'}
    
    office_code = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address_line1 = Column(String(50), nullable=False)
    address_line2 = Column(String(50))
    state = Column(String(50))
    country = Column(String(50), nullable=False)
    postal_code = Column(String(15), nullable=False)
    territory = Column(String(20), nullable=False)


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'public'}
    
    employee_number = Column(BigInteger, primary_key=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    office_code = Column(String(10), ForeignKey('public.offices.office_code'), nullable=False)
    reports_to = Column(BigInteger, ForeignKey('public.employees.employee_number'))
    job_title = Column(String(50), nullable=False)


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'public'}
    
    customer_number = Column(BigInteger, primary_key=True)
    contact_lastname = Column(String(50))
    contact_firstname = Column(String(50))
    phone = Column(String(50), nullable=False)
    address_line1 = Column(String(50), nullable=False)
    address_line2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(15))
    country = Column(String(60), nullable=False)
    sales_employee_number = Column(BigInteger, ForeignKey('public.employees.employee_number'))


class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'public'}
    
    customer_number = Column(BigInteger, ForeignKey('public.customers.customer_number'), primary_key=True)
    check_number = Column(String(50), primary_key=True)
    payment_date = Column(TIMESTAMP, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'public'}

    order_number = Column(BigInteger, primary_key=True, index=True)
    order_date = Column(TIMESTAMP, nullable=False)
    required_date = Column(TIMESTAMP, nullable=False)
    shipped_date = Column(TIMESTAMP, nullable=True)
    status = Column(String(15), nullable=False)
    comments = Column(Text, nullable=True)
    customer_number = Column(BigInteger, ForeignKey('customers.customer_number'), nullable=False)




class Order_Detail(Base):
    __tablename__ = 'order_details'
    __table_args__ = {'schema': 'public'}
    
    order_number = Column(BigInteger, ForeignKey('public.orders.order_number'), primary_key=True)
    product_code = Column(String(15), ForeignKey('production.products.product_code'), primary_key=True)
    quantity_ordered = Column(BigInteger, nullable=False)
    price_each = Column(Numeric(10, 2), nullable=False)
    order_line_number = Column(Integer, nullable=False)


class Office_Buy(Base):
    __tablename__ = 'office_buys'
    __table_args__ = {'schema': 'public'}
    
    office_buy_code = Column(BigInteger, Identity(always=True), primary_key=True)
    buy_date = Column(TIMESTAMP)
    product_code = Column(String(15), ForeignKey('production.products.product_code'))
    buy_quantity = Column(BigInteger)
    buy_price = Column(Numeric(10, 2))
    office_code = Column(String(10), ForeignKey('public.offices.office_code'))

