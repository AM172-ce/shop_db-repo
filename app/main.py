# from product_operations import (
#     insert_product, 
#     insert_product_discont, 

#     fundamental_update_product, 
#     update_product_inventory,
#     update_product_pricing, 
#     update_product_discount, 
    
#     delete_product,
#     delete_product_discount
#     )
# from search_products import search_products

# def main():
#     while True:
#         print("Continue as supervisor (1) or customer(2):")
#         print("3. Exit")
#         choice = input("Enter your choice: ")
#         if choice == '1':
#             supervisor()
#         elif choice == '2':
#             print("---------")
#         elif choice == '3':
#             break
#         else:
#             print("Invalid choice. Please try again.")

# def supervisor():
#     while True:
#         print("Select an option:")
#         print("1. Search for products")
#         print("2. Manage product information (CRUD operations)")
#         print("3. Exit")

#         choice = input("Enter your choice (1-3): ")

#         if choice == "1":
#             search_products()
#         elif choice == "2":
#             manage_product_crud()
#         elif choice == "3":
#             break
#         else:
#             print("Invalid choice. Please try again.")


# def manage_product_crud():
#     while True:
#         print("Select a CRUD operation:")
#         print("1. Add a new product")
#         print("2. Add discount to a product")
#         print("------------------------------")
#         print("3. Update product fundamental details(name,vendor, description)")
#         print("4. Update a product inventory")
#         print("5. Update a product price")
#         print("6. Update product discount details(value, description)")
#         print("------------------------------")
#         print("7. Remove a product discount")
#         print("8. Delete a product")
#         print("\n")
#         print("9. Back to main menu")

#         choice = input("Enter your choice (1-9): ")
        
#         if choice == "1":
#             insert_product()
#         elif choice == "2":
#             product_code = input("Enter the product code: ")
#             insert_product_discont(product_code)
#         elif choice == "3":
#             product_code = input("Enter the product code: ")
#             fundamental_update_product(product_code)
#         elif choice == "4":
#             product_code = input("Enter the product code: ")
#             update_product_inventory(product_code)
#         elif choice == "5":
#             product_code = input("Enter the product code: ")
#             update_product_pricing(product_code)
#         elif choice == "6":
#             product_code = input("Enter the product code: ")
#             update_product_discount(product_code)
#         elif choice == "7":
#             product_code = input("Enter the product code: ")
#             delete_product_discount(product_code)
#         elif choice == "8":
#             product_code = input("Enter the product code: ")
#             delete_product(product_code)
#         elif choice == "9":
#             break
#         else:
#             print("Invalid choice. Please try again.")


# if __name__ == "__main__":
#     main()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the static directory to serve CSS, JS, and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="UI")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/supervisor", response_class=HTMLResponse)
async def supervisor_menu(request: Request):
    return templates.TemplateResponse("supervisor.html", {"request": request})

@app.get("/supervisor/search", response_class=HTMLResponse)
async def search_products(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/supervisor/manage", response_class=HTMLResponse)
async def manage_products(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)

