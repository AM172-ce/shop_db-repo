from models import session, Product, Product_Pricing, Product_Discount
from sqlalchemy.exc import SQLAlchemyError

def search_products():
    try:
        query = session.query(Product).join(Product_Pricing, 
                                            Product.product_code == Product_Pricing.products_code
                                            ).outerjoin(Product_Discount, 
                                                        Product.product_code == Product_Discount.product_code
                                                        ).filter(Product.is_deleted == False, 
                                                                 Product_Pricing.in_active == True)
        
        search_option = input("Search by (1) Product Name or (2) Product Description? Enter 1 or 2: ").strip()
        search_term = input("Enter the search term: ").strip()
        if search_term:
            if search_option == "1":
                query = query.filter(Product.product_name.ilike(f"%{search_term}%"))
            elif search_option == "2":
                query = query.filter(Product.product_description.ilike(f"%{search_term}%"))
            else:
                print("Invalid option selected.")
            return 
        filter_min_price = input("Enter minimum price (or press Enter to skip): ").strip()
        filter_max_price = input("Enter maximum price (or press Enter to skip): ").strip()
        filter_min_inventory = input("Enter minimum inventory (or press Enter to skip): ").strip()
        filter_max_inventory = input("Enter maximum inventory (or press Enter to skip): ").strip()
        filter_min_rate = input("Enter minimum user rate (or press Enter to skip): ").strip()
        filter_max_rate = input("Enter maximum user rate (or press Enter to skip): ").strip()
        sort_by = input("Enter field to sort by (price/inventory/rate): ").strip()
        sort_order = input("Enter sort order (asc/desc): ").strip().lower()


        if filter_min_price:
            query = query.filter(Product_Pricing.base_price >= float(filter_min_price))
        if filter_max_price:
            query = query.filter(Product_Pricing.base_price <= float(filter_max_price))

        if filter_min_inventory:
            query = query.filter(Product.quantity_in_stock >= int(filter_min_inventory))
        if filter_max_inventory:
            query = query.filter(Product.quantity_in_stock <= int(filter_max_inventory))

        if filter_min_rate:
            query = query.filter(Product_Discount.rates >= int(filter_min_rate))
        if filter_max_rate:
            query = query.filter(Product_Discount.rates <= int(filter_max_rate))

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
                query = query.order_by(Product_Discount.rates.asc())
            else:
                query = query.order_by(Product_Discount.rates.desc())

        results = query.all()

        if results:
            print(f"{'Product Code':<15} {'Name':<30} {'Vendor':<20} {'Price':<10} {'Inventory':<10} {'Rate':<5}")
            print("="*90)
            for product in results:
                active_pricing = next((pricing for pricing in product.pricings if pricing.in_active), None)
                rate = session.query(Product_Discount).filter(Product_Discount.product_code == product.product_code).first()
                rate_value = rate.rates if rate else 'N/A'
                if active_pricing:
                    print(f"{product.product_code:<15} {product.product_name:<30} {product.product_vendor:<20} {active_pricing.base_price:<10} {product.quantity_in_stock:<10} {rate_value:<5}")
        else:
            print("No products found.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        session.close()


