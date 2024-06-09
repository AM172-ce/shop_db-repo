import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime, timedelta

today = datetime.now()
fake = Faker()

# Define the save path
save_path = r'/mnt/shared/data'

# Generate offices data
def generate_offices(n):
    offices = []
    territory_list = ['NorthShopper','CentralMart','EastMall','WestBuy','MetroMarket','UrbanChoice','SuburbSaver','CoastalCart','HeartlandHub','PeakPlaza']
    for _ in range(n):
        office = {
            'office_code': fake.unique.bothify(text='??###'),
            'city': fake.city(),
            'phone': fake.phone_number(),
            'address_line1': fake.street_address(),
            'address_line2': fake.secondary_address(),
            'state': fake.state(),
            'country': fake.country(),
            'postal_code': fake.postcode(),
            'territory': random.choice(territory_list)
        }
        offices.append(office)
    return pd.DataFrame(offices)

# Generate employees data
def generate_employees(n, office_codes):
    employees = []
    job_title_hierarchy = {
        'Manager': ['Sales Associate', 'Customer Service Representative', 'Store Manager', 'Inventory Manager', 'Purchasing Manager', 'Warehouse Supervisor', 'Cashier', 'Retail Assistant', 'Product Specialist', 'Marketing Coordinator'],
        'Sales Associate': ['Sales Assistant', 'Retail Sales Representative', 'Product Demonstrator'],
        'Customer Service Representative': ['Customer Support Specialist', 'Call Center Agent', 'Complaints Resolution Officer'],
        'Store Manager': ['Assistant Store Manager', 'Department Supervisor', 'Shift Leader'],
        'Inventory Manager': ['Inventory Control Specialist', 'Stockroom Coordinator', 'Receiving Clerk'],
        'Purchasing Manager': ['Procurement Specialist', 'Buyer', 'Vendor Relations Coordinator'],
        'Warehouse Supervisor': ['Shipping and Receiving Supervisor', 'Distribution Center Manager', 'Logistics Coordinator'],
        'Cashier': ['Front End Supervisor', 'Checkout Operator', 'Cash Office Clerk'],
        'Retail Assistant': ['Sales Support Associate', 'Merchandising Assistant', 'Floor Assistant'],
        'Product Specialist': ['Brand Ambassador', 'Product Advisor', 'Demonstrator Coordinator'],
        'Marketing Coordinator': ['Social Media Coordinator', 'Event Coordinator', 'Marketing Assistant']
    }

    job_title_list = [
        'Sales Associate', 'Sales Assistant', 'Retail Sales Representative', 'Product Demonstrator',
        'Customer Service Representative', 'Customer Support Specialist', 'Call Center Agent', 'Complaints Resolution Officer',
        'Store Manager', 'Assistant Store Manager', 'Department Supervisor', 'Shift Leader',
        'Inventory Manager', 'Inventory Control Specialist', 'Stockroom Coordinator', 'Receiving Clerk',
        'Purchasing Manager', 'Procurement Specialist', 'Buyer', 'Vendor Relations Coordinator',
        'Warehouse Supervisor', 'Shipping and Receiving Supervisor', 'Distribution Center Manager', 'Logistics Coordinator',
        'Cashier', 'Front End Supervisor', 'Checkout Operator', 'Cash Office Clerk',
        'Retail Assistant', 'Sales Support Associate', 'Merchandising Assistant', 'Floor Assistant',
        'Product Specialist', 'Brand Ambassador', 'Product Advisor', 'Demonstrator Coordinator',
        'Marketing Coordinator', 'Social Media Coordinator', 'Event Coordinator', 'Marketing Assistant'
    ]
    # Ensure we have at least one supervisor for each key role
    required_supervisors = [
        'Manager', 'Sales Associate', 'Customer Service Representative', 'Store Manager',
        'Inventory Manager', 'Purchasing Manager', 'Warehouse Supervisor', 'Cashier',
        'Retail Assistant', 'Product Specialist', 'Marketing Coordinator'
    ]

    # Generate supervisors first
    for job_title in required_supervisors:
        supervisor = {
            'employee_number': fake.unique.random_number(digits=6, fix_len=True),
            'lastname': fake.last_name(),
            'firstname': fake.first_name(),
            'extension': fake.bothify(text='???##'),
            'email': fake.email(),
            'office_code': random.choice(office_codes),
            'reports_to': None,
            'job_title': job_title
        }
        employees.append(supervisor)

    # Generate the remaining employees without the 'reports_to' field
    for _ in range(n - len(required_supervisors)):
        employee = {
            'employee_number': fake.unique.random_number(digits=6, fix_len=True),
            'lastname': fake.last_name(),
            'firstname': fake.first_name(),
            'extension': fake.bothify(text='???##'),
            'email': fake.email(),
            'office_code': random.choice(office_codes),
            'reports_to': None,
            'job_title': random.choice(job_title_list)
        }
        employees.append(employee)

    # Create a DataFrame for easy manipulation
    df_employees = pd.DataFrame(employees)

    # Assign 'reports_to' based on the hierarchy
    for job_title, subordinates in job_title_hierarchy.items():
        supervisors = df_employees[df_employees['job_title'] == job_title]['employee_number'].tolist()
        for subordinate in subordinates:
            subordinate_indices = df_employees[(df_employees['job_title'] == subordinate) & (df_employees['reports_to'].isnull())].index.tolist()
            for index in subordinate_indices:
                if supervisors:
                    df_employees.at[index, 'reports_to'] = random.choice(supervisors)
    return df_employees

# Generate customers data
def generate_customers(n, employee_numbers):
    customers = []
    for _ in range(n):
        customer = {
            'customer_number': fake.unique.random_number(digits=6, fix_len=True),
            'contact_lastname': fake.last_name(),
            'contact_firstname': fake.first_name(),
            'phone': fake.phone_number(),
            'address_line1': fake.street_address(),
            'address_line2': fake.secondary_address(),
            'city': fake.city(),
            'state': fake.state(),
            'postal_code': fake.postcode(),
            'country': fake.country(),
            'sales_employee_number': random.choice(employee_numbers),
            'credit_limit': round(random.uniform(1000, 100000), 2)
        }
        customers.append(customer)
    return pd.DataFrame(customers)

# Generate orders data

def generate_orders(n, customer_numbers):
    orders = []
    for _ in range(n):
        order_date = fake.date_time_between(start_date='-2y', end_date='now')
        status = random.choice(['Shipped', 'Pending', 'Cancelled'])
        
        if status == 'Shipped':
            shipped_date = fake.date_time_between(start_date=order_date, end_date=today)
            required_date = fake.date_time_between(start_date=shipped_date, end_date='+30d')
        else:
            shipped_date = None
            required_date = fake.date_time_between(start_date=order_date, end_date='+30d')
        
        order = {
            'order_number': fake.unique.random_number(digits=6, fix_len=True),
            'order_date': order_date,
            'required_date': required_date,
            'shipped_date': shipped_date,
            'status': status,
            'comments': fake.text(),
            'customer_number': random.choice(customer_numbers)
        }
        orders.append(order)
    return pd.DataFrame(orders)

# Generate payments data
def generate_payments(n, customer_numbers):
    print("generate_payments start")
    payments = []
    unique_combinations = set()  # To store unique (customer_number, check_number) combinations
    
    while len(unique_combinations) < n:
        customer_number = random.choice(customer_numbers)
        check_number = fake.unique.bothify(text='??###')
        combination = (customer_number, check_number)
        
        # Check if the combination is already generated
        if combination in unique_combinations:
            continue
        # Generate the payment date
        payment_date = fake.date_time_between(start_date="-2y", end_date=today)

        # Generate the payment
        payment = {
            'customer_number': customer_number,
            'check_number': check_number,
            'payment_date': payment_date,
            'amount': round(random.uniform(100, 10000), 2)
        }
        # Add the combination to the set of unique combinations
        unique_combinations.add(combination)
        
        # Append the payment to the list
        payments.append(payment)
    return pd.DataFrame(payments)

# Generate product_categories data
def generate_product_categories(n):
    print("generate_product_categories start")
    categories = []
    categories_names_list = [
    "Apparel","Footwear","Accessories","Home Appliances","Bedding & Linens",
    "Sports & Fitness","Personal Care","Bags & Luggage",
    "Kitchenware","Gadgets & Electronics","Home Decor",
    "Outdoor Gear","Beauty & Skincare","Office Supplies",
    "Travel Essentials","Cooking & Dining","Pet Supplies",
    "Health & Wellness","Fashion","Toys & Games"
    ]
    for _ in range(n):
        category_name = random.choice(categories_names_list)
        categories_names_list.remove(category_name) 
        product_category = {
            'product_category_code': fake.unique.bothify(text='??###'),
            'category_name': category_name,
            'product_category_description': fake.text(),
            'parent_category_code': None  # Can be populated later if necessary
        }
        categories.append(product_category)
    return pd.DataFrame(categories)

# Generate products data
def generate_products(n, category_codes):
    products = []
    product_name_list = [
    "SuperSoft Cotton T-Shirt","UltraGrip Running Shoes","Premium Leather Wallet","FreshBrew Coffee Maker",
    "LuxeComfort Bedding Set","ProFit Gym Shorts","EcoFresh Bamboo Toothbrush","PowerGlide Laptop Backpack","CrystalClear Water Bottle",
    "Chef'sChoice Knife Set","AirPurify HEPA Filter","OrganicGlow Facial Serum","FlexiFit Yoga Mat","TechSafe Laptop Sleeve",
    "MegaChill Cooler Bag","NatureSense Plant Pot","SwiftCharge Power Bank","SmartClean Robot Vacuum","AdventureSeeker Backpack",
    "Fashionista Sunglasses","GourmetBlend Spice Rack","HarmonyHues Paint Set","FitFlex Resistance Bands","ChefMaster Cooking Utensils",
    "BeautyBoost Hair Dryer","PeakPerformance Protein Powder","TranquilVibes Essential Oil Diffuser","ZenZone Meditation Cushion","SportPro Compression Socks","EcoScape Bamboo Cutlery Set",
    "UrbanExplorer Travel Backpack","FreshHarvest Salad Spinner","AquaZone Swim Goggles","BioGlow LED Desk Lamp","HomeComfort Throw Blanket","IronGrip Dumbbell Set",
    "Nature'sGift Aromatherapy Candle","WanderLust Travel Pillow","StyleSavvy Makeup Organizer","ComfortZone Lounge Chair","ZenWellness Meditation Kit",
    "EcoEats Bamboo Dinnerware Set","BlazeTech BBQ Grill Set","SoundSoothe White Noise Machine","PetParadise Cat Tree","InstaFresh Salad Spinner",
    "AdventureReady Hiking Boots","ChefDelight Cookware Set","SleepTight Weighted Blanket","ProForm Workout Bench","GardenGlow Solar Lights","EcoCleanse Bamboo Cleaning Brushes",
    "ChillZone Cooling Towel","StudySmart Desk Organizer","FashionForward Handbag","AquaPulse Water Flosser","PowerFlex Resistance Bands","ExploreMore Camping Tent",
    "StyleSense Jewelry Organizer","SportZone Exercise Ball","EarthEssence Bamboo Towel Set","CozyComfort Throw Pillow","LifeBalance Wellness Tracker","TrendSetter Sunglasses",
    "EcoChic Bamboo Toothbrush Holder","Chef'sDelight Kitchen Scale","NightRelief Sleep Mask","TechTrend Wireless Earbuds","PowerUp Portable Charger","ZenGarden Mini Fountain",
    "HomeHarmony Oil Diffuser","UrbanEscape Backpack","PetPamper Grooming Kit","StyleStash Jewelry Box","EcoEase Bamboo Soap Dish","AquaSplash Water Bottle","FitFlex Yoga Block",
    "ProGlide Shaving Kit","AdventureAwaits Backpack","Chef'sChoice Knife Sharpener","PetParadise Dog Bed","StyleSavvy Scarf Organizer","PowerUp Solar Charger",
    "ExploreMore Camping Stove","EcoFresh Bamboo Bath Mat","ChillFactor Ice Pack","StudySmart Book Stand","FashionForward Belt","AquaBoost Shower Head","PowerPro Portable Blender",
    "ZenDen Meditation Chair","EarthyEssence Bamboo Soap Dispenser","SportFit Running Belt","EcoClean Bamboo Dish Rack","AdventureBound Hiking Backpack","ChefPro Kitchen Timer",
    "SleepSound White Noise Machine","TechTrend Bluetooth Speaker","UrbanTrekker Travel Backpack","PetParadise Cat Toy"
    ]
    # Ensure that at least one record is generated for each product name
    num_product_names = len(product_name_list)
    if n < num_product_names:
        product_names = random.sample(product_name_list, n)
    else:
        product_names = product_name_list + [random.choice(product_name_list) for _ in range(n - num_product_names)]
  
    for product_name in product_names:
        product = {
            'product_code': fake.unique.bothify(text='??###'),
            'product_name': product_name,
            'product_vendor': fake.company(),
            'product_description': fake.text(),
            'quantity_in_stock': random.randint(1, 1000),
            'product_category_code': random.choice(category_codes)
        }
        products.append(product)
    return pd.DataFrame(products)

# Generate products_comments data
def generate_products_comments(n, product_codes, customer_numbers):
    print("generate_products_comments start")
    comments = []
    unique_combinations = set()  # To store unique (product_code, customer_number) combinations
    
    while len(unique_combinations) < n:
        product_code = random.choice(product_codes)
        customer_number = random.choice(customer_numbers)
        combination = (product_code, customer_number)

        # Check if the combination is already generated
        if combination in unique_combinations:
            continue
        # Generate the comment
        comment = {
            'product_code': product_code,
            'customer_number': customer_number,
            'comments': fake.text(),
            'rates': random.randint(1, 5)
        }
        # Add the combination to the set of unique combinations
        unique_combinations.add(combination)
        
        # Append the comment to the list
        comments.append(comment)
    return pd.DataFrame(comments)

# Generate discount_units data
def generate_discount_units():
    units = [
        {'discount_unit_code': 'P', 'discount_unit_name': 'Percentage'},
        {'discount_unit_code': 'A', 'discount_unit_name': 'Amount'}
    ]
    return pd.DataFrame(units)

# Generate products_discount data
def generate_products_discount(n, product_codes, discount_unit_codes):
    discounts = []
    for _ in range(n):
        date_created = fake.date_time_between(start_date="-2y", end_date=today)
        valid_until = fake.date_time_between(start_date=date_created, end_date=date_created + timedelta(days=365))
        
        discount = {
            'product_discount_code': fake.unique.random_number(digits=6, fix_len=True),
            'product_code': random.choice(product_codes),
            'discount_value': round(random.uniform(1, 50), 2),
            'discount_unit': random.choice(discount_unit_codes),
            'date_created': date_created,
            'valid_until': valid_until,
            'discount_description': fake.text()
        }
        discounts.append(discount)
    return pd.DataFrame(discounts)

# Generate product_categories_discount data
def generate_product_categories_discount(n, category_codes, discount_unit_codes):
    discounts = []
    for _ in range(n):
        date_created = fake.date_time_between(start_date="-2y", end_date=today)
        valid_until = fake.date_time_between(start_date=date_created, end_date=date_created + timedelta(days=365))
        
        discount = {
            'product_categories_discount_code': fake.unique.random_number(digits=6, fix_len=True),
            'product_categories_code': random.choice(category_codes),
            'discount_value': round(random.uniform(1, 50), 2),
            'discount_unit': random.choice(discount_unit_codes),
            'date_created': date_created,
            'valid_until': valid_until,
            'discount_description': fake.text()
        }
        discounts.append(discount)
    return pd.DataFrame(discounts)

# Generate products_pricing data
def generate_products_pricing(n, product_codes):
    print("generate_products_pricing start")
    pricing = []
    
    for product_code in product_codes:
        date_created = fake.date_time_between(start_date="-2y", end_date=today)
        price = {
            'products_pricing_code': fake.unique.random_number(digits=6, fix_len=True),
            'products_code': product_code,
            'base_price': round(random.uniform(10, 1000), 2),
            'date_created': date_created,
            'date_expiry': None,
            'in_active': True,
            'msrp': round(random.uniform(10, 1000), 2)
        }
        pricing.append(price)
    
    
    for _ in range(n - len(product_codes)):
        product_code = random.choice(product_codes)
        
        date_created = fake.date_time_between(start_date="-2y", end_date=today)
        date_expiry = fake.date_between(start_date=date_created, end_date=today)
        
        price = {
            'products_pricing_code': fake.unique.random_number(digits=6, fix_len=True),
            'products_code': product_code,
            'base_price': round(random.uniform(10, 1000), 2),
            'date_created': date_created,
            'date_expiry': date_expiry,
            'in_active': False,
            'msrp': round(random.uniform(10, 1000), 2)
        }
        pricing.append(price)
    return pd.DataFrame(pricing)

# Generate order_details data
def generate_order_details(n, order_numbers, product_codes):
    print("generate_order_details start")
    details = []
    unique_combinations = set()  # To store unique (order_number, product_code) combinations
    print("555")
    while len(unique_combinations) < n:
        order_number = random.choice(order_numbers)
        product_code = random.choice(product_codes)
        combination = (order_number, product_code)
        
        # Check if the combination is already generated
        if combination in unique_combinations:
            continue
        
        # Generate the order detail
        detail = {
            'order_number': order_number,
            'product_code': product_code,
            'quantity_ordered': random.randint(1, 100),
            'price_each': round(random.uniform(10, 1000), 2),
            'order_line_number': random.randint(1, 10)
        }
        
        # Add the combination to the set of unique combinations
        unique_combinations.add(combination)
        
        # Append the order detail to the list
        details.append(detail)
    return pd.DataFrame(details)

# Generate office_buys data
def generate_office_buys(n, product_codes, office_codes):
    buys = []
    for i in range(n):
        buy_date = fake.date_time_between(start_date="-2y", end_date=today)
        buy = {
            'office_buy_code': i + 1,
            'buy_date': buy_date,
            'product_code': random.choice(product_codes),
            'buy_quantity': random.randint(1, 1000),
            'buy_price': round(random.uniform(10, 1000), 2),
            'office_code': random.choice(office_codes)
        }
        buys.append(buy)
    return pd.DataFrame(buys)


# Generate data
office_data = generate_offices(15)
employee_data = generate_employees(60, office_data['office_code'].tolist())
customer_data = generate_customers(150, employee_data['employee_number'].tolist())
order_data = generate_orders(400, customer_data['customer_number'].tolist())
payment_data = generate_payments(300, customer_data['customer_number'].tolist())
category_data = generate_product_categories(20)
product_data = generate_products(150, category_data['product_category_code'].tolist())
comment_data = generate_products_comments(350, product_data['product_code'].tolist(), customer_data['customer_number'].tolist())
discount_unit_data = generate_discount_units()
product_discount_data = generate_products_discount(60, product_data['product_code'].tolist(), discount_unit_data['discount_unit_code'].tolist())
category_discount_data = generate_product_categories_discount(40, category_data['product_category_code'].tolist(), discount_unit_data['discount_unit_code'].tolist())
pricing_data = generate_products_pricing(450, product_data['product_code'].tolist())
order_detail_data = generate_order_details(450, order_data['order_number'].tolist(), product_data['product_code'].tolist())
office_buy_data = generate_office_buys(150, product_data['product_code'].tolist(), office_data['office_code'].tolist())

# Save to CSV
office_data.to_csv(os.path.join(save_path, 'offices.csv'), index=False)
employee_data.to_csv(os.path.join(save_path, 'employees.csv'), index=False)
customer_data.to_csv(os.path.join(save_path, 'customers.csv'), index=False)
order_data.to_csv(os.path.join(save_path, 'orders.csv'), index=False)
payment_data.to_csv(os.path.join(save_path, 'payments.csv'), index=False)
category_data.to_csv(os.path.join(save_path, 'product_categories.csv'), index=False)
product_data.to_csv(os.path.join(save_path, 'products.csv'), index=False)
comment_data.to_csv(os.path.join(save_path, 'products_comments.csv'), index=False)
discount_unit_data.to_csv(os.path.join(save_path, 'discount_units.csv'), index=False)
product_discount_data.to_csv(os.path.join(save_path, 'products_discount.csv'), index=False)
category_discount_data.to_csv(os.path.join(save_path, 'product_categories_discount.csv'), index=False)
pricing_data.to_csv(os.path.join(save_path, 'products_pricing.csv'), index=False)
order_detail_data.to_csv(os.path.join(save_path, 'order_details.csv'), index=False)
office_buy_data.to_csv(os.path.join(save_path, 'office_buys.csv'), index=False)
print("progtam finished!")