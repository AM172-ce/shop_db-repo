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

def insert_product_discont(input_product_code):
    try:
        existing_active_discount = session.query(Product_Discount).filter(
            Product_Discount.product_code == input_product_code,
            Product_Discount.in_active == True
        ).first()
        flag = True
        if existing_active_discount or flag == True:
            print(f"An active discount record already exists for product {input_product_code}.")
            print("Deactivate the old one?(yes/no)")
            choice = input("Enter yout answer:")
            while True:
                if choice == 'yes':
                    delete_product_discount(input_product_code)
                    flag = False
                    break
                elif choice == 'no':
                    return
                else:
                    print("Invalid choice. Please try again.")

        product_discount_code = fake.unique.random_number(digits=6, fix_len=True)
        discount_value = float(input("Enter discount value: "))
        discount_unit = input("Enter discount unit (P for percentage, A for amount): ")
        date_created = today
        valid_until = datetime.strptime(input("Enter valid until date (YYYY-MM-DD)" 
                                              "(or press Enter to be generated automatically): "), '%Y-%m-%d'
                                              ) or fake.date_time_between(start_date=date_created, 
                                                                          end_date=date_created + timedelta(days=365)) 
        discount_description = input("Enter discount description: ")

        new_discount = Product_Discount(
            product_discount_code=product_discount_code,
            product_code=input_product_code,
            discount_value=discount_value,
            discount_unit=discount_unit,
            date_created=date_created,
            valid_until=valid_until,
            discount_description=discount_description
        )
        session.add(new_discount)
        session.commit()

        print(f"Product discount for {input_product_code} added successfully.")    
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting product: {str(e)}")
    finally:
        session.close()

###########################################################################################################
#Update functions on product
###########################################################################################################

def fundamental_update_product(input_product_code):
    try:
        product = session.query(Product).filter(Product.product_code == input_product_code).first()
        while True:
            print("\n1. change the name")
            print("2. change the vendor name")
            print("3. change the description")
            print("4. Exit")
            choice = input ("Enter your choice: ")
            if choice == '1':
                if product:
                    product.product_name = input(f"Enter new name for product {input_product_code}(or press Enter to keep current): ") or product.product_name
                    session.commit()
                    print(f"Product name of {input_product_code} updated successfully.")
                else:
                    print(f"Product {input_product_code} not found.")
            elif choice == '2':
                if product:
                    product.product_vendor = input(f"Enter new vendor for product {input_product_code}(or press Enter to keep current): ") or product.product_vendor
                    session.commit()
                    print(f"Product vendor of {input_product_code} updated successfully.")
                else:
                    print(f"Product {input_product_code} not found.")
            elif choice == '3':
                if product:
                    product.product_description = input(f"Enter new description for product {input_product_code}(or press Enter to keep current): ") or product.product_description
                    session.commit()
                    print(f"Product description of {input_product_code} updated successfully.")
                else:
                    print(f"Product {input_product_code} not found.")
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating product: {str(e)}")
    finally:
        session.close()

def update_product_inventory(input_product_code):
    try:
        product = session.query(Product).filter(Product.product_code == input_product_code).first()
        if product:
            product.quantity_in_stock = int(input(f"Enter new quantity in stock for product {input_product_code}(or press Enter to keep current): ") or product.quantity_in_stock)
            session.commit()
            print(f"Product inventory of {input_product_code} updated successfully.")
        else:
            print(f"Product {input_product_code} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting product: {str(e)}")
    finally:
        session.close()


def update_product_pricing(input_product_code):
    try:
        active_pricing = session.query(Product_Pricing).filter(Product_Pricing.products_code == input_product_code,
                                                               Product_Pricing.in_active == True).first()
        if active_pricing:
            active_pricing.in_active = False
            active_pricing.date_expiry = today
        else:
            print(f"active price for {input_product_code} not found.")

        new_base_price = float(input("Enter new base price (or press Enter to keep current): ")or Product_Pricing.base_price)
        new_msrp = float(input("Enter new MSRP(or press Enter to keep current): ") or Product_Pricing.msrp)
        new_pricing = Product_Pricing(
            products_code=input_product_code,
            base_price=new_base_price,
            date_created=today,
            in_active=True,
            msrp=new_msrp
        )
        session.add(new_pricing)

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting product: {str(e)}")
    finally:
        session.close()


def update_product_discount(input_product_code):
    try:
        product_discount = session.query(Product_Discount).filter(Product_Discount.products_code == input_product_code,
                                                                 Product_Discount.in_active == True).first()
        while True:
            print("\n1. change the discount value or unit")
            print("2. change the discount description")
            print("3. Exit")
            choice = input ("Enter your choice: ")
            if choice == '1':
                if product_discount:
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

                    print(f"Discount info of {input_product_code} updated successfully.")
                else:
                    print(f"Active Product discount for {input_product_code} not found.")
    
            elif choice == '2':
                if product_discount:
                    product_discount.product_description = input(f"Enter new description for discount of product {input_product_code}(or press Enter to keep current): ") or product_discount.product_description
                    session.commit()
                    print(f"Product description of {input_product_code} updated successfully.")
                else:
                    print(f"Active Product discount for {input_product_code} not found.")
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting product: {str(e)}")
    finally:
        session.close()



###########################################################################################################
#Delete functions on product
###########################################################################################################

def delete_product_discount(input_product_code):
    try:
        product_discount = session.query(Product_Discount).filter(Product_Discount.products_code == input_product_code,
                                                                 Product_Discount.in_active == True).first()
        if product_discount:
            product_discount.in_active = False
            session.commit()
            print(f"Discount record of Product {input_product_code} deactivated successfully.")
        else:
            print(f"Product discount {input_product_code} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting product: {str(e)}")
    finally:
        session.close()




def delete_product(product_code):
    try:
        product = session.query(Product).filter(Product.product_code == product_code).first()
        if product:
           
            product.is_active = False
            session.commit()

            active_pricing = session.query(Product_Pricing).filter(Product_Pricing.products_code == product_code,
                                                                   Product_Pricing.in_active == True).first()
            if active_pricing:
                active_pricing.in_active = False
                active_pricing.date_expiry = today
                session.commit()

            print(f"Product {product_code} and its pricing records deactivated successfully.")
        else:
            print(f"Product {product_code} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting product: {str(e)}")
    finally:
        session.close()

