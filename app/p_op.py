from random import choice
from models import session, Product, Product_Pricing, Product_Discount
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from faker import Faker
from fastapi import FastAPI, Form

today = datetime.now()
fake = Faker()
app = FastAPI()

@app.post("/api/insert_product")
async def insert_product(
    product_name: str = Form(...),
    product_vendor: str = Form(...),
    product_description: str = Form(...),
    quantity_in_stock: int = Form(...),
    product_category_code: str = Form(...),
    base_price: float = Form(...),
    msrp: float = Form(...)
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
        
        new_pricing = Product_Pricing(
            products_code=new_product.product_code,
            base_price=base_price,
            date_created=today,
            in_active=True,
            msrp=msrp
        )
        session.add(new_pricing)
        
        session.commit()
        return {"message": f"Product {new_product.product_code} and its pricing inserted successfully."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error inserting product: {str(e)}"}
    finally:
        session.close()

@app.post("/api/insert_product_discount")
async def insert_product_discount(
    product_code: str = Form(...),
    discount_value: float = Form(...),
    discount_unit: str = Form(...),
    valid_until: datetime = Form(None),
    discount_description: str = Form(None),
    action: str = Form(None)
):
    try:
        if action == "deactivate":
            delete_product_discount(product_code) # type: ignore
            return {"message": f"Previous discount for product {product_code} deactivated successfully."}

        existing_active_discount = session.query(Product_Discount).filter(
            Product_Discount.product_code == product_code,
            Product_Discount.in_active == True
        ).first()

        if existing_active_discount:
            return {
                "message": f"An active discount record already exists for product {product_code}.",
                "action": "deactivate"
            }
        
        product_discount_code = fake.unique.random_number(digits=6, fix_len=True)
        date_created = today
        if not valid_until:
            valid_until = fake.date_time_between(start_date=date_created, end_date=date_created + timedelta(days=365))
        
        new_discount = Product_Discount(
            product_discount_code=product_discount_code,
            product_code=product_code,
            discount_value=discount_value,
            discount_unit=discount_unit,
            date_created=date_created,
            valid_until=valid_until,
            discount_description=discount_description
        )
        session.add(new_discount)
        session.commit()
        return {"message": f"Product discount for {product_code} added successfully."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error inserting product discount: {str(e)}"}
    finally:
        session.close()


########################################

@app.post("/api/fundamental_update_product")
async def fundamental_update_product(
    product_code: str = Form(...),
    name: str = Form(None),
    vendor: str = Form(None),
    description: str = Form(None)
):
    try:
        product = session.query(Product).filter(Product.product_code == product_code).first()
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

@app.post("/api/update_product_inventory")
async def update_product_inventory(
    product_code: str = Form(...),
    quantity_in_stock: int = Form(...)
):
    try:
        product = session.query(Product).filter(Product.product_code == product_code).first()
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

@app.post("/api/update_product_pricing")
async def update_product_pricing(
    product_code: str = Form(...),
    new_base_price: float = Form(None),
    new_msrp: float = Form(None)
):
    try:
        active_pricing = session.query(Product_Pricing).filter(
            Product_Pricing.products_code == product_code,
            Product_Pricing.in_active == True
        ).first()
        if active_pricing:
            active_pricing.in_active = False
            active_pricing.date_expiry = datetime.now()
        else:
            return {"message": f"Active price for {product_code} not found."}

        new_pricing = Product_Pricing(
            products_code=product_code,
            base_price=new_base_price,
            date_created=datetime.now(),
            in_active=True,
            msrp=new_msrp
        )
        session.add(new_pricing)
        session.commit()
        return {"message": f"Product pricing for {product_code} updated successfully."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error updating product pricing: {str(e)}"}
    finally:
        session.close()

    
@app.post("/api/update_product_discount")
async def update_product_discount(
    input_product_code: str = Form(...),
    action: int = Form(...)
):
    try:
        product_discount = session.query(Product_Discount).filter(Product_Discount.products_code == input_product_code,
                                                                 Product_Discount.in_active == True).first()
        if action == 1:
            product_discount_code = fake.unique.random_number(digits=6, fix_len=True)
            discount_value = input(f"Enter new discount value for product {input_product_code}(or press Enter to keep current): ") or product_discount.discount_value
            discount_unit = input(f"Enter new discount unit for product {input_product_code} (or press Enter to keep current): ") or product_discount.discount_unit
            valid_until = datetime.strptime(input("Enter valid until date (YYYY-MM-DD)" 
                                      "(or press Enter to be generated automatically): "), '%Y-%m-%d'
                                      ) or fake.date_time_between(start_date=today, 
                                                                  end_date=today + timedelta(days=365))
            new_discount = Product_Discount(
                product_discount_code=product_discount_code,
                product_code=input_product_code,
                discount_value=discount_value,
                discount_unit=discount_unit,
                date_created=today,
                valid_until=valid_until,
                discount_description=product_discount.discount_description
                )
            session.add(new_discount)
            session.commit()

            return {"message": f"Discount info of {input_product_code} updated successfully."}
        elif action == 2:
            if product_discount:
                product_discount.product_description = input(f"Enter new description for discount of product {input_product_code}(or press Enter to keep current): ") or product_discount.product_description
                session.commit()
                return {"message": f"Product description of {input_product_code} updated successfully."}
            else:
                return {"error": f"Active Product discount for {input_product_code} not found."}
        else:
            return {"error": "Invalid action. Please try again."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"error": f"Error updating product discount: {str(e)}"}
    finally:
        session.close()


@app.post("/api/delete_product_discount")
async def delete_product_discount(product_code):
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

@app.post("/api/delete_product")
async def delete_product(product_code: str):
    try:
        product = session.query(Product).filter(Product.product_code == product_code).first()
        if product:
            product.is_active = False
            session.commit()

            active_pricing = session.query(Product_Pricing).filter(
                Product_Pricing.products_code == product_code,
                Product_Pricing.in_active == True
            ).first()
            if active_pricing:
                active_pricing.in_active = False
                active_pricing.date_expiry = today
                session.commit()

            return {"message": f"Product {product_code} and its pricing records deactivated successfully."}
        else:
            return {"message": f"Product {product_code} not found."}
    except SQLAlchemyError as e:
        session.rollback()
        return {"message": f"Error deleting product: {str(e)}"}
    finally:
        session.close()