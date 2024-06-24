from fastapi import APIRouter, Form, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.dependencies import get_db_session
from app.crud.operations import (
    insert_product, 
    insert_product_discount,
    fundamental_update_product,
    update_product_inventory,
    update_product_pricing,
    update_product_discount,
    delete_product_discount,
    delete_product
    )
from app.models.tables import Product, Product_Pricing, Product_Comment
from datetime import datetime
from typing import Optional


router = APIRouter()


####################-INSERT-#########################
@router.post("/api/insert_product")
async def insert_product_api(
    product_name: str = Form(...),
    product_vendor: str = Form(...),
    product_description: str = Form(...),
    quantity_in_stock: int = Form(...),
    product_category_code: str = Form(...),
    base_price: float = Form(...),
    msrp: float = Form(...),
    office_code: str = Form(...),
    session: Session = Depends(get_db_session)
):
    result = insert_product(
        session=session,
        product_name=product_name,
        product_vendor=product_vendor,
        product_description=product_description,
        quantity_in_stock=quantity_in_stock,
        product_category_code=product_category_code,
        base_price=base_price,
        msrp=msrp,
        office_code=office_code
    )
    return result

@router.post("/api/insert_product_discount")
async def insert_product_discount_api(
    product_code: str = Form(...),
    discount_value: float = Form(...),
    discount_unit: str = Form(...),
    valid_until: datetime = Form(None),
    discount_description: str = Form(None),
    action: str = Form(None),
    session: Session = Depends(get_db_session)
):
    result = insert_product_discount(
            session=session,
            product_code=product_code,
            discount_value=discount_value,
            discount_unit=discount_unit,
            valid_until=valid_until,
            discount_description=discount_description,
            action=action
    )
    return result
####################-UPDATE-#########################

@router.post("/api/fundamental_update_product")
async def api_fundamental_update_product(
    product_code: str = Form(...),
    name: str = Form(None),
    vendor: str = Form(None),
    description: str = Form(None),
    session: Session = Depends(get_db_session)
):
    try:
        result = fundamental_update_product(
            session,
            product_code, 
            name, vendor, 
            description)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error updating product: {str(e)}")

@router.post("/api/update_product_inventory")
async def api_update_product_inventory(
    product_code: str = Form(...),
    quantity_in_stock: int = Form(...),
    session: Session = Depends(get_db_session)
):
    try:
        result = update_product_inventory(session, product_code, quantity_in_stock)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error updating product inventory: {str(e)}")


@router.post("/api/update_product_pricing")
async def api_update_product_pricing(
    product_code: str = Form(...),
    new_base_price: float = Form(None),
    new_msrp: float = Form(None),
    session: Session = Depends(get_db_session)
):
    try:
        result = update_product_pricing(
            session, 
            product_code, 
            new_base_price, 
            new_msrp)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error updating product pricing: {str(e)}")
    

@router.post("/api/update_product_discount")
async def api_update_product_discount(
    input_product_code: str = Form(...),
    discount_value: float = Form(None),
    discount_unit: str = Form(None),
    valid_until: str = Form(None),
    discount_description: str = Form(None),
    action: int = Form(...),
    session: Session = Depends(get_db_session)
):
    try:
        
        result = update_product_discount(
            session,
            input_product_code=input_product_code, 
            discount_value=discount_value, 
            discount_unit=discount_unit, 
            valid_until=valid_until, 
            discount_description=discount_description,
            action=action
            )
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error updating product discount: {str(e)}")
    
####################-DELETE-#########################

@router.post("/api/delete_product_discount")
async def api_delete_product_discount(
    product_code: str = Form(...),
    session: Session = Depends(get_db_session)
):
    try:
        
        result = delete_product_discount(
            session,
            product_code=product_code
            )
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error deleting product discount: {str(e)}")
    
@router.post("/api/delete_product")
async def api_delete_product(
    product_code: str = Form(...),
    session: Session = Depends(get_db_session)
):
    try:
        
        result = delete_product(
            session,
            product_code=product_code
            )
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error deleting product: {str(e)}")
    


####################-SEARCH-#########################


@router.get("/api/search_products")
async def search_products(
    product_name: Optional[str] = Query(None),
    product_description: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_inventory: Optional[int] = Query(None),
    max_inventory: Optional[int] = Query(None),
    min_rate: Optional[int] = Query(None),
    max_rate: Optional[int] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query(None),
    session: Session = Depends(get_db_session)
):
    try:
        query = session.query(Product)

    
        query = query.join(Product_Pricing, Product.product_code == Product_Pricing.product_code).filter(Product_Pricing.in_active == True)
        query = query.join(Product_Comment, Product.product_code == Product_Comment.product_code)

        if product_name:
            query = query.filter(Product.product_name.ilike(f"%{product_name}%"))
        if product_description:
            query = query.filter(Product.product_description.ilike(f"%{product_description}%"))
        if min_price:
            query = query.filter(Product_Pricing.base_price >= min_price)
        if max_price:
            query = query.filter(Product_Pricing.base_price <= max_price)
        if min_inventory:
            query = query.filter(Product.quantity_in_stock >= min_inventory)
        if max_inventory:
            query = query.filter(Product.quantity_in_stock <= max_inventory)
        if min_rate:
            query = query.filter(Product_Comment.rates >= min_rate)
        if max_rate:
            query = query.filter(Product_Comment.rates <= max_rate)

        if sort_by == 'price':
            if sort_order == 'asc':
                query = query.order_by(Product_Pricing.base_price.asc())
            else:
                query = query.order_by(Product_Pricing.base_price.desc())
        elif sort_by == 'inventory':
            if sort_order == 'asc':
                query = query.order_by(Product.quantity_in_stock.asc())
            else:
                query = query.order_by(Product.quantity_in_stock.desc())
        elif sort_by == 'rate':
            if sort_order == 'asc':
                query = query.order_by(Product_Comment.rates.asc())
            else:
                query = query.order_by(Product_Comment.rates.desc())

  
        results = query.all()

        products = []
        for product in results:

            active_pricing = next((pricing for pricing in product.pricings if pricing.in_active), None)
            rate_value = product.comments[0].rates if product.comments else 'N/A'

            products.append({
                "product_code": product.product_code,
                "product_name": product.product_name,
                "product_vendor": product.product_vendor,
                "base_price": active_pricing.base_price if active_pricing else None,
                "quantity_in_stock": product.quantity_in_stock,
                "rate": rate_value
            })

        return {"products": products}

    except SQLAlchemyError as e:
        session.rollback() 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    finally:
        session.close()
