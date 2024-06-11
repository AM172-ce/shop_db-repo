from sqlalchemy import (
    create_engine, 
    Column, String, BigInteger, Integer, Numeric, Text, 
    ForeignKey, Boolean, TIMESTAMP, 
    CheckConstraint, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.engine import URL
import psycopg2
import os
import time


def get_psycopg2_connection():
    try:
        conn = psycopg2.connect(
            dbname="shop",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def get_sqlalchemy_engine(psycopg2_conn):
    try:
        url = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password="postgres",
            host="db",
            port="5432",
            database="shop"
        )
        engine = create_engine(url, creator=lambda: psycopg2_conn)
        return engine
    except Exception as e:
        print(f"Error creating SQLAlchemy engine: {e}")
        return None


psycopg2_conn = get_psycopg2_connection()
if psycopg2_conn is None:
    print("Error in psycopg2 connection")
try:    
    engine = get_sqlalchemy_engine(psycopg2_conn)
    if engine:
        print("SQLAlchemy engine created successfully!")
except Exception as e:
    print(f"Error using SQLAlchemy engine: {e}")

# DATABASE_URL = os.environ.get('DATABASE_URL')

# def get_db_engine():
#     return create_engine(DATABASE_URL)

# while True:
#     try:
#         db_engine = get_db_engine().connect()
#         if db_engine:
#             break
#     except Exception as e:
#         print(f'++++ Error while connecting to database or while creating SQLAlchemy Engine: {str(e)} ++++')
#         time.sleep(5)

# engine = get_db_engine()

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'production'}
    
    product_code = Column(String(15), primary_key=True)
    product_name = Column(String(70), nullable=False)
    product_vendor = Column(String(50), nullable=False)
    product_description = Column(Text, nullable=False)
    quantity_in_stock = Column(BigInteger, nullable=False)
    product_category_code = Column(String(15), ForeignKey('production.product_categories.product_category_code'))
    is_deleted = Column(Boolean, default=False)

    pricings = relationship("ProductPricing", back_populates="product", cascade="all, delete-orphan")
    discounts = relationship("ProductDiscount", back_populates="product", cascade="all, delete-orphan")
    comments = relationship("ProductComment", back_populates="product", cascade="all, delete-orphan")
    office_buys = relationship("OfficeBuy", back_populates="product", cascade="all, delete-orphan")
    category = relationship("ProductCategory", back_populates="products")



class Product_Pricing(Base):
    __tablename__ = 'products_pricing'
    __table_args__ = {'schema': 'production'}
    
    
    products_pricing_code = Column(BigInteger, primary_key=True)
    products_code = Column(String(15), ForeignKey('production.products.product_code'), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    date_expiry = Column(TIMESTAMP)
    in_active = Column(Boolean, nullable=False)
    msrp = Column(Numeric(10, 2), nullable=False)

    product = relationship("Product", back_populates="pricings")


class Product_Discount(Base):
    __tablename__ = 'products_discount'
    __table_args__ = {'schema': 'production'}

    product_discount_code = Column(BigInteger, primary_key=True)
    product_code = Column(String(15), ForeignKey('production.products.product_code'), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    discount_unit = Column(String(1), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    discount_description = Column(Text)
    in_active = Column(Boolean, default=True)

    product = relationship("Product", back_populates="discounts")

class Product_Comment(Base):
    __tablename__ = 'products_comments'
    __table_args__ = {'schema': 'production'}
    
    product_code = Column(String(15), ForeignKey('production.products.product_code'), primary_key=True)
    customer_number = Column(BigInteger, ForeignKey('customers.customer_number'), primary_key=True)
    comments = Column(Text)
    rates = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="comments")

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    __table_args__ = {'schema': 'production'}
    
    product_category_code = Column(String(15), primary_key=True)
    category_name = Column(String(70), nullable=False)
    product_category_description = Column(Text)
    parent_category_code = Column(String(15), ForeignKey('production.product_categories.product_category_code'))

    parent_category = relationship("ProductCategory", remote_side=[product_category_code])
    products = relationship("Product", back_populates="category")

class ProductCategoriesDiscount(Base):
    __tablename__ = 'product_categories_discount'
    __table_args__ = {'schema': 'public'}

    product_categories_discount_code = Column(BigInteger, primary_key=True)
    product_categories_code = Column(String(15), ForeignKey('public.product_categories.product_category_code'), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    discount_unit = Column(String(1), nullable=False)
    date_created = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    discount_description = Column(Text)
    in_active = Column(Boolean, default=True)

    product_discount = relationship("ProductDiscount", back_populates="product_categories_discounts")



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

    office = relationship("Office")

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

    sales_employee = relationship("Employee")

class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'public'}
    
    customer_number = Column(BigInteger, ForeignKey('public.customers.customer_number'), primary_key=True)
    check_number = Column(String(50), primary_key=True)
    payment_date = Column(TIMESTAMP, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

class OrderDetail(Base):
    __tablename__ = 'order_details'
    __table_args__ = {'schema': 'public'}
    
    order_number = Column(BigInteger, ForeignKey('public.orders.order_number'), primary_key=True)
    product_code = Column(String(15), ForeignKey('public.products.product_code'), primary_key=True)
    quantity_ordered = Column(BigInteger, nullable=False)
    price_each = Column(Numeric(10, 2), nullable=False)
    order_line_number = Column(Integer, nullable=False)

class OfficeBuy(Base):
    __tablename__ = 'office_buys'
    __table_args__ = {'schema': 'public'}
    
    office_buy_code = Column(BigInteger, primary_key=True)
    buy_date = Column(TIMESTAMP)
    product_code = Column(String(15), ForeignKey('public.products.product_code'))
    buy_quantity = Column(BigInteger)
    buy_price = Column(Numeric(10, 2))
    office_code = Column(String(10), ForeignKey('public.offices.office_code'))

    product = relationship("Product")
    office = relationship("Office")
