# operations.py

from app.models.tables import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from faker import Faker

today = datetime.now()
fake = Faker()

####################-INSERT-#########################
def insert_product(
        session,
        product_name, 
        product_vendor, 
        product_description, 
        quantity_in_stock, 
        product_category_code, 
        base_price, msrp,
        office_code
        ):
    try:
        new_product = Product(
            product_name=product_name,
            product_vendor=product_vendor,
            product_description=product_description,
            quantity_in_stock=quantity_in_stock,
            product_category_code=product_category_code
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        new_pricing = Product_Pricing(
            product_code=new_product.product_code,
            base_price=base_price,
            date_created=today,
            in_active=True,
            msrp=msrp
        )
        session.add(new_pricing)

        new_office_buy = Office_Buy(
            product_code=new_product.product_code,
            buy_quantity=quantity_in_stock,
            buy_price=base_price,
            office_code=office_code,
            buy_date=today
        )
        session.add(new_office_buy)

        session.commit()
        session.refresh(new_pricing)
        session.refresh(new_office_buy)
        print("successfull")
        return {"message": f"Product {new_product.product_code} and its pricing inserted successfully."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error inserting product: {str(e)}"}
    finally:
        session.close()


def insert_product_discount(
        session,
        product_code, 
        discount_value, 
        discount_unit, 
        valid_until=None, 
        discount_description=None,
        action=None
        ):
    try:
        existing_active_discount = session.query(Product_Discount).filter(
            Product_Discount.product_code == product_code,
            Product_Discount.in_active == True
        ).first()

        if existing_active_discount:
            if action == "deactivate":
                existing_active_discount.in_active = False
                existing_active_discount.valid_until = today
                session.commit()
                return
            else:
                return {
                    "message": f"An active discount record already exists for product {product_code}.",
                    "action": "deactivate",
                    "existing_discount": existing_active_discount
                }

        date_created = today
        if not valid_until:
            valid_until = fake.date_time_between(
                start_date=date_created, end_date=date_created + timedelta(days=365))

        new_discount = Product_Discount(
            product_code=product_code,
            discount_value=discount_value,
            discount_unit=discount_unit,
            date_created=date_created,
            valid_until=valid_until,
            discount_description=discount_description
        )
        session.add(new_discount)
        session.commit()
        session.refresh(new_discount)
        return {"message": f"Product discount for {product_code} added successfully."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error inserting product discount: {str(e)}"}
    finally:
        session.close()

####################-UPDATE-#########################

def fundamental_update_product(
        session,
        product_code, 
        name=None, 
        vendor=None, 
        description=None
        ):
    try:
        product = session.query(Product).filter(
            Product.product_code == product_code).first()
        if product:
            if name:
                product.product_name = name
            if vendor:
                product.product_vendor = vendor
            if description:
                product.product_description = description
            session.commit()
            return {"message": f"Product {product_code} updated successfully."}
        else:
            return {"message": f"Product {product_code} not found."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error updating product: {str(e)}"}
    finally:
        session.close()


def update_product_inventory(session, product_code, quantity_in_stock):
    try:
        product = session.query(Product).filter(
            Product.product_code == product_code).first()
        if product:
            product.quantity_in_stock = quantity_in_stock
            session.commit()
            return {"message": f"Product inventory of {product_code} updated successfully."}
        else:
            return {"message": f"Product {product_code} not found."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error updating product inventory: {str(e)}"}
    finally:
        session.close()


def update_product_pricing(
        session,
        product_code, 
        new_base_price=None, 
        new_msrp=None
        ):
    try:
        active_pricing = session.query(Product_Pricing).filter(
            Product_Pricing.product_code == product_code,
            Product_Pricing.in_active == True
        ).first()
        if active_pricing:
            active_pricing.in_active = False
            active_pricing.date_expiry = datetime.now()
        else:
            return {"message": f"Active price for {product_code} not found."}

        new_pricing = Product_Pricing(
            product_code=product_code,
            base_price=new_base_price,
            date_created=datetime.now(),
            in_active=True,
            msrp=new_msrp
        )
        session.add(new_pricing)
        session.commit()
        session.refresh(new_pricing)
        return {"message": f"Product pricing for {product_code} updated successfully."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error updating product pricing: {str(e)}"}
    finally:
        session.close()


def update_product_discount(
        session,
        input_product_code, 
        discount_value=None, 
        discount_unit=None, 
        valid_until=None, 
        discount_description=None, 
        action=None):
    try:
        active_product_discount = session.query(Product_Discount).filter(
            Product_Discount.product_code == input_product_code,
            Product_Discount.in_active == True).first()
        
        if active_product_discount:
            if action == 1:
                active_product_discount.in_active = False
                active_product_discount.valid_until = today
                session.commit()
                session.refresh(active_product_discount)
                if valid_until is None:
                    valid_until = fake.date_time_between(start_date=today,
                                                                        end_date=today + timedelta(days=365))
            
                new_discount = Product_Discount(
                    product_code=input_product_code,
                    discount_value=discount_value,
                    discount_unit=discount_unit,
                    date_created=today,
                    valid_until=valid_until,
                    discount_description=active_product_discount.discount_description
                )
                session.add(new_discount)
                session.commit()
                session.refresh(new_discount)

                return {"message": f"Discount info of {input_product_code} updated successfully."}
            
            elif action == 2:
                active_product_discount.product_description = discount_description
                session.commit()
                session.refresh(active_product_discount)
                return {"message": f"Product description of {input_product_code} updated successfully."}
            else:
                return {"error": "Invalid action. Please try again."}
        else:
            return {"error": f"Active Product discount for {input_product_code} not found."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"error": f"Error updating product discount: {str(e)}"}
    finally:
        session.close()

####################-DELETE-#########################

def delete_product_discount(session, product_code):
    try:
        product_discount = session.query(Product_Discount).filter(
            Product_Discount.product_code == product_code,
            Product_Discount.in_active == True
        ).first()
        if product_discount:
            product_discount.in_active = False
            session.commit()
            return {"message": f"Discount record of Product {product_code} deactivated successfully."}
        else:
            return {"message": f"Product discount {product_code} not found."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error deleting product: {str(e)}"}
    finally:
        session.close()


def delete_product(session, product_code):
    try:
        product = session.query(Product).filter(
            Product.product_code == product_code).first()
        if product:
            if product.is_deleted == True:
                return {"message": f"Product {product_code} is already deleted"}
            else:
                product.is_deleted = True
                session.commit()

                active_pricing = session.query(Product_Pricing).filter(
                    Product_Pricing.product_code == product_code,
                    Product_Pricing.in_active == True
                ).first()
                if active_pricing:
                    active_pricing.in_active = False
                    active_pricing.date_expiry = today
                    session.commit()

                active_discount = session.query(Product_Discount).filter(
                    Product_Discount.product_code == product_code,
                    Product_Discount.in_active == True
                ).first()
                if active_discount:
                    active_discount.in_active = False
                    active_discount.date_expiry = today
                    session.commit()

                return {"message": f"Product {product_code} and its pricing records deactivated successfully."}
        else:
           return {"message": f"Product {product_code} not found."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error deleting product: {str(e)}"}
    finally:
        session.close()
