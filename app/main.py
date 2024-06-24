from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import product
import os


app = FastAPI()

app.include_router(product.router)



app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=os.path.join("app", "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route for the supervisor menu
@app.get("/supervisor", response_class=HTMLResponse)
async def supervisor_menu(request: Request):
    return templates.TemplateResponse("supervisor.html", {"request": request})

# Route for the search products page
@app.get("/supervisor/search", response_class=HTMLResponse)
async def search_products(request: Request):
    return templates.TemplateResponse("search_products.html", {"request": request})

# Route for the manage products page
@app.get("/supervisor/manage", response_class=HTMLResponse)
async def manage_products(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})

@app.get("/manage/insert_product.html", response_class=HTMLResponse)
async def insert_product(request: Request):
    return templates.TemplateResponse("insert_product.html", {"request": request})

@app.get("/manage/insert_product_discount.html", response_class=HTMLResponse)
async def insert_product_discount(request: Request):
    return templates.TemplateResponse("insert_product_discount.html", {"request": request})

@app.get("/manage/update_product.html", response_class=HTMLResponse)
async def update_product(request: Request):
    return templates.TemplateResponse("update_product.html", {"request": request})

@app.get("/manage/update_product_inventory.html", response_class=HTMLResponse)
async def update_product_inventory(request: Request):
    return templates.TemplateResponse("update_product_inventory.html", {"request": request})

@app.get("/manage/update_product_pricing.html", response_class=HTMLResponse)
async def update_product_pricing(request: Request):
    return templates.TemplateResponse("update_product_pricing.html", {"request": request})

@app.get("/manage/update_product_discount.html", response_class=HTMLResponse)
async def update_product_discount(request: Request):
    return templates.TemplateResponse("update_product_discount.html", {"request": request})

@app.get("/manage/delete_product_discount.html", response_class=HTMLResponse)
async def delete_product_discount(request: Request):
    return templates.TemplateResponse("delete_product_discount.html", {"request": request})

@app.get("/manage/delete_product.html", response_class=HTMLResponse)
async def delete_product(request: Request):
    return templates.TemplateResponse("delete_product.html", {"request": request})

