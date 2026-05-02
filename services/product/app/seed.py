"""Seed the product database with Luxe Garments catalog."""
from app.database import async_session
from app.models import Category, Subcategory, Product
from sqlalchemy import select


CATALOG = {
    "electronics": {
        "name": "Electronics",
        "subcategories": {
            "smartphones": {
                "display_name": "Smartphones",
                "products": [
                    {"id": "ELEC-001", "name": "iPhone 15 Pro", "sub": "Premium smartphone", "price": 79999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1592286927505-1def25115558?w=400", "details": ["6.1 inch display", "A17 Pro chip", "Pro camera system", "Titanium design"]},
                    {"id": "ELEC-002", "name": "Samsung Galaxy S24", "sub": "Flagship Android", "price": 74999, "colors": ["#000", "#FFF"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=400", "details": ["6.2 inch display", "Snapdragon 8 Gen 3", "50MP main camera", "AI features"]},
                    {"id": "ELEC-003", "name": "Google Pixel 8", "sub": "Pure Android", "price": 59999, "colors": ["#000", "#FFF"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400", "details": ["6.3 inch display", "Tensor G3", "Advanced AI", "7 years updates"]},
                    {"id": "ELEC-004", "name": "OnePlus 12", "sub": "Fast charging", "price": 54999, "colors": ["#000"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1511294635253-b0661cff6600?w=400", "details": ["6.7 inch display", "Snapdragon 8 Gen 3", "100W charging", "Fluid AMOLED"]},
                    {"id": "ELEC-005", "name": "Xiaomi 14 Ultra", "sub": "Camera beast", "price": 49999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400", "details": ["6.73 inch display", "Leica optics", "1-inch sensor", "Snapdragon 8 Gen 3"]},
                ]
            },
            "laptops": {
                "display_name": "Laptops",
                "products": [
                    {"id": "ELEC-006", "name": "MacBook Pro M3", "sub": "Powerful laptop", "price": 149999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400", "details": ["8-core M3 chip", "8GB RAM", "512GB SSD", "13.3 inch display"]},
                    {"id": "ELEC-007", "name": "Dell XPS 15", "sub": "Ultra-slim", "price": 129999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1588872657840-790ff3a58e39?w=400", "details": ["Intel Core i7", "16GB RAM", "512GB SSD", "15.6 inch FHD"]},
                    {"id": "ELEC-008", "name": "HP Pavilion 15", "sub": "Everyday laptop", "price": 59999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400", "details": ["Intel Core i5", "8GB RAM", "256GB SSD", "15.6 inch HD"]},
                    {"id": "ELEC-009", "name": "Lenovo ThinkPad", "sub": "Business class", "price": 74999, "colors": ["#000"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400", "details": ["Intel Core i7", "16GB RAM", "512GB SSD", "14 inch FHD"]},
                    {"id": "ELEC-010", "name": "ASUS VivoBook", "sub": "Budget friendly", "price": 54999, "colors": ["#000"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1603302576837-37891a844e48?w=400", "details": ["AMD Ryzen 5", "8GB RAM", "256GB SSD", "15.6 inch HD"]},
                ]
            },
            "tablets": {
                "display_name": "Tablets",
                "products": [
                    {"id": "ELEC-011", "name": "iPad Pro 12.9", "sub": "Professional tablet", "price": 89999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1542992941-44c2c22e2d91?w=400", "details": ["M2 chip", "8GB RAM", "128GB storage", "ProMotion display"]},
                    {"id": "ELEC-012", "name": "Samsung Galaxy Tab S9", "sub": "Android flagship", "price": 64999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400", "details": ["Snapdragon 888", "8GB RAM", "128GB storage", "11 inch display"]},
                    {"id": "ELEC-013", "name": "iPad Air", "sub": "Mid-range Apple", "price": 59999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=400", "details": ["M1 chip", "8GB RAM", "64GB storage", "10.9 inch display"]},
                    {"id": "ELEC-014", "name": "Lenovo Tab P11", "sub": "Budget tablet", "price": 34999, "colors": ["#000"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1586253408875-cff102099c53?w=400", "details": ["MediaTek chip", "4GB RAM", "128GB storage", "11 inch display"]},
                    {"id": "ELEC-015", "name": "Microsoft Surface Go", "sub": "2-in-1 device", "price": 49999, "colors": ["#000"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1603387751919-a39bc6437ee0?w=400", "details": ["Intel m3", "4GB RAM", "64GB storage", "10.5 inch display"]},
                ]
            },
            "accessories": {
                "display_name": "Accessories",
                "products": [
                    {"id": "ELEC-016", "name": "USB-C Cable", "sub": "Universal charging", "price": 499, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1626348158427-acda1afb1d17?w=400", "details": ["2 meter length", "Fast charging", "Durable", "Universal compatible"]},
                    {"id": "ELEC-017", "name": "Phone Stand", "sub": "Adjustable holder", "price": 799, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "details": ["360 rotation", "Aluminum", "Adjustable angle", "Portable"]},
                    {"id": "ELEC-018", "name": "Screen Protector", "sub": "Glass protection", "price": 399, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1610529215189-df8a0b9cfa1c?w=400", "details": ["Tempered glass", "Anti-fingerprint", "Easy application", "Bubble-free"]},
                    {"id": "ELEC-019", "name": "Phone Case", "sub": "Protective cover", "price": 599, "colors": ["#000", "#FFF"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1605559427920-cd4628902d4a?w=400", "details": ["Shock absorbing", "Premium material", "Slim design", "Button protection"]},
                    {"id": "ELEC-020", "name": "Charging Dock", "sub": "Wireless charging", "price": 1499, "colors": ["#000"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400", "details": ["15W fast charging", "LED indicator", "Universal", "Compact design"]},
                ]
            },
            "audio": {
                "display_name": "Audio",
                "products": [
                    {"id": "ELEC-021", "name": "Sony WH-1000XM5", "sub": "Noise canceling", "price": 29999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "details": ["Active noise cancel", "30hr battery", "Bluetooth 5.3", "Premium sound"]},
                    {"id": "ELEC-022", "name": "Bose QC45", "sub": "Comfort fit", "price": 34999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=400", "details": ["Noise canceling", "24hr battery", "Comfortable padding", "Premium audio"]},
                    {"id": "ELEC-023", "name": "JBL Flip 6", "sub": "Portable speaker", "price": 14999, "colors": ["#000", "#FFF"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1545454675-3479f3a7a62c?w=400", "details": ["IPX7 waterproof", "12 hour battery", "Portable", "360 sound"]},
                    {"id": "ELEC-024", "name": "Apple AirPods Pro", "sub": "True wireless", "price": 24999, "colors": ["#FFF"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1572293552491-d51a085edcc8?w=400", "details": ["ANC", "Spatial audio", "6hr battery", "Seamless iOS"]},
                    {"id": "ELEC-025", "name": "Samsung Galaxy Buds", "sub": "Android exclusive", "price": 12999, "colors": ["#000"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400", "details": ["ANC", "8hr battery", "IPX7 rated", "Compact case"]},
                ]
            },
        }
    },
    "fashion": {
        "name": "Fashion",
        "subcategories": {
            "men": {
                "display_name": "Men",
                "products": [
                    {"id": "FASH-001", "name": "Cotton T-Shirt", "sub": "Basic essential", "price": 799, "colors": ["#FFF", "#000"], "sizes": ["S","M","L","XL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "details": ["100% Cotton", "Crew neck", "Breathable", "Easy care"]},
                    {"id": "FASH-002", "name": "Denim Jeans", "sub": "Classic fit", "price": 2499, "colors": ["#1B3A5C"], "sizes": ["30","32","34","36"], "badge": None, "img": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400", "details": ["Cotton denim", "Button fly", "5-pocket", "Classic rise"]},
                    {"id": "FASH-003", "name": "Formal Shirt", "sub": "Office wear", "price": 1999, "colors": ["#FFF", "#87CEEB"], "sizes": ["S","M","L","XL"], "badge": None, "img": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400", "details": ["Cotton blend", "Oxford cloth", "Professional", "Easy iron"]},
                    {"id": "FASH-004", "name": "Blazer", "sub": "Smart casual", "price": 5999, "colors": ["#191919"], "sizes": ["S","M","L","XL"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "details": ["Tailored fit", "Notch lapel", "Button closure", "Premium fabric"]},
                    {"id": "FASH-005", "name": "Casual Shorts", "sub": "Summer wear", "price": 1299, "colors": ["#000", "#87CEEB"], "sizes": ["S","M","L","XL"], "badge": "New", "img": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400", "details": ["Comfortable", "Quick dry", "Pockets", "Regular fit"]},
                ]
            },
            "women": {
                "display_name": "Women",
                "products": [
                    {"id": "FASH-006", "name": "Cotton Saree", "sub": "Traditional wear", "price": 2999, "colors": ["#FF69B4"], "sizes": ["Onesize"], "badge": None, "img": "https://images.unsplash.com/photo-1612551564844-2d34e0d2cf8d?w=400", "details": ["Pure cotton", "Elegant drape", "Breathable", "Handwoven"]},
                    {"id": "FASH-007", "name": "Kurti", "sub": "Casual ethnic", "price": 1499, "colors": ["#FF1493", "#FFB6C1"], "sizes": ["XS","S","M","L","XL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1598032895397-b9472444bf93?w=400", "details": ["Cotton fabric", "Printed design", "Comfortable", "Easy maintenance"]},
                    {"id": "FASH-008", "name": "Salwar Suit", "sub": "Ethnic ensemble", "price": 3499, "colors": ["#800080"], "sizes": ["S","M","L"], "badge": None, "img": "https://images.unsplash.com/photo-1599599810694-b5ac4dd37e3b?w=400", "details": ["Cotton blend", "3-piece set", "Embroidered", "Traditional"]},
                    {"id": "FASH-009", "name": "Ethnic Dress", "sub": "Festive wear", "price": 4999, "colors": ["#FFD700"], "sizes": ["XS","S","M","L"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400", "details": ["Premium fabric", "Hand details", "Special occasion", "Elegant cut"]},
                    {"id": "FASH-010", "name": "Top", "sub": "Casual blouse", "price": 999, "colors": ["#FFF", "#000"], "sizes": ["XS","S","M","L","XL"], "badge": "New", "img": "https://images.unsplash.com/photo-1617623814075-e51df1bdc82f?w=400", "details": ["Cotton", "Versatile", "Comfortable fit", "Easy wash"]},
                ]
            },
            "kids": {
                "display_name": "Kids",
                "products": [
                    {"id": "FASH-011", "name": "Kids T-Shirt", "sub": "Playful colors", "price": 599, "colors": ["#FF69B4", "#87CEEB"], "sizes": ["2","4","6","8"], "badge": None, "img": "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400", "details": ["Soft cotton", "Colorful print", "Durable", "Comfortable"]},
                    {"id": "FASH-012", "name": "Kids Shorts", "sub": "Active play", "price": 899, "colors": ["#000", "#FF69B4"], "sizes": ["2","4","6","8","10"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1471286174890-9c112ac6f76b?w=400", "details": ["Quick dry", "Comfortable", "Elastic waist", "Fun designs"]},
                    {"id": "FASH-013", "name": "Kids Dress", "sub": "Special occasion", "price": 1299, "colors": ["#FF1493", "#FFB6C1"], "sizes": ["2","4","6","8"], "badge": None, "img": "https://images.unsplash.com/photo-1604467794349-0b74285de7e7?w=400", "details": ["Soft fabric", "Pretty design", "Comfortable", "Easy care"]},
                    {"id": "FASH-014", "name": "Kids Jacket", "sub": "Layering piece", "price": 1999, "colors": ["#87CEEB"], "sizes": ["2","4","6","8"], "badge": "New", "img": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400", "details": ["Warm", "Lightweight", "Adjustable", "Durable"]},
                    {"id": "FASH-015", "name": "Kids Hoodie", "sub": "Cozy comfort", "price": 1499, "colors": ["#191919", "#87CEEB"], "sizes": ["2","4","6","8","10"], "badge": None, "img": "https://images.unsplash.com/photo-1556821552-107d8f92457d?w=400", "details": ["Fleece lined", "Kangaroo pocket", "Drawstring", "Comfortable"]},
                ]
            },
            "shoes": {
                "display_name": "Shoes",
                "products": [
                    {"id": "FASH-016", "name": "Running Shoes", "sub": "Athletic", "price": 4999, "colors": ["#000"], "sizes": ["6","7","8","9","10"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "details": ["Cushioned", "Breathable", "Lightweight", "Performance"]},
                    {"id": "FASH-017", "name": "Sports Shoes", "sub": "Casual sport", "price": 3999, "colors": ["#FFF", "#000"], "sizes": ["6","7","8","9","10"], "badge": None, "img": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400", "details": ["Flexible", "Durable", "Supportive", "Modern design"]},
                    {"id": "FASH-018", "name": "Casual Sneakers", "sub": "Everyday wear", "price": 2999, "colors": ["#FFF", "#000"], "sizes": ["6","7","8","9","10","11"], "badge": "New", "img": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400", "details": ["Comfortable", "Stylish", "Versatile", "Easy walk"]},
                    {"id": "FASH-019", "name": "Formal Shoes", "sub": "Office wear", "price": 3499, "colors": ["#191919"], "sizes": ["6","7","8","9","10"], "badge": None, "img": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=400", "details": ["Leather", "Professional", "Polished", "Comfortable"]},
                    {"id": "FASH-020", "name": "Flip Flops", "sub": "Beach wear", "price": 599, "colors": ["#000", "#FFF"], "sizes": ["6","7","8","9","10"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1595299892991-a1e70a94d5a9?w=400", "details": ["Lightweight", "Durable", "Comfortable", "Water resistant"]},
                ]
            },
            "accessories": {
                "display_name": "Accessories",
                "products": [
                    {"id": "FASH-021", "name": "Leather Belt", "sub": "Classic accessory", "price": 999, "colors": ["#191919", "#8B4513"], "sizes": ["30","32","34","36"], "badge": None, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "details": ["Genuine leather", "Adjustable", "Buckle", "Premium"]},
                    {"id": "FASH-022", "name": "Scarf", "sub": "Style statement", "price": 699, "colors": ["#FF69B4"], "sizes": ["Onesize"], "badge": "New", "img": "https://images.unsplash.com/photo-1596552183021-b3c3a3c723c3?w=400", "details": ["Soft fabric", "Colorful", "Versatile", "Easy drape"]},
                    {"id": "FASH-023", "name": "Sunglasses", "sub": "Eye protection", "price": 1999, "colors": ["#000"], "sizes": ["Onesize"], "badge": None, "img": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400", "details": ["UV protection", "Stylish", "Durable", "Lightweight"]},
                    {"id": "FASH-024", "name": "Watch", "sub": "Time keeper", "price": 3999, "colors": ["#000"], "sizes": ["Onesize"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=400", "details": ["Accurate", "Stylish", "Water resistant", "Long lasting"]},
                    {"id": "FASH-025", "name": "Bag", "sub": "Daily essential", "price": 2499, "colors": ["#191919", "#8B4513"], "sizes": ["Onesize"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400", "details": ["Spacious", "Durable", "Comfortable", "Stylish"]},
                ]
            },
        }
    },
    "home": {
        "name": "Home & Kitchen",
        "subcategories": {
            "kitchen": {
                "display_name": "Kitchen",
                "products": [
                    {"id": "HOME-001", "name": "Pan Set", "sub": "Cooking essential", "price": 2999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=400", "details": ["Non-stick coating", "3 pieces", "Heat resistant", "Easy clean"]},
                    {"id": "HOME-002", "name": "Cookware Set", "sub": "Premium quality", "price": 3499, "colors": ["#000"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1584588694223-7b9e9e79b93f?w=400", "details": ["Stainless steel", "10 pieces", "Durable", "Oven safe"]},
                    {"id": "HOME-003", "name": "Mixing Bowls", "sub": "Preparation set", "price": 899, "colors": ["#FFF"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1578500454673-85b8ce8b07b7?w=400", "details": ["5 different sizes", "Glass", "Microwave safe", "Easy store"]},
                    {"id": "HOME-004", "name": "Knife Set", "sub": "Sharp tools", "price": 1999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1566624432832-e94e2b338637?w=400", "details": ["Stainless steel", "6 pieces", "Sharp blade", "Wood handle"]},
                    {"id": "HOME-005", "name": "Cutting Board", "sub": "Prep surface", "price": 499, "colors": ["#FFF", "#000"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1577720643272-265e434f6edb?w=400", "details": ["Durable", "Non-slip", "Easy clean", "Compact"]},
                ]
            },
            "bedding": {
                "display_name": "Bedding",
                "products": [
                    {"id": "HOME-006", "name": "Bed Sheet", "sub": "Comfort sleep", "price": 1299, "colors": ["#FFF", "#87CEEB"], "sizes": ["Queen","King"], "badge": None, "img": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=400", "details": ["100% Cotton", "Soft", "Easy wash", "Durable"]},
                    {"id": "HOME-007", "name": "Pillow Set", "sub": "Neck support", "price": 1999, "colors": ["#FFF"], "sizes": ["Standard"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1584622181563-430f63602d4b?w=400", "details": ["Memory foam", "Ergonomic", "Washable", "Comfortable"]},
                    {"id": "HOME-008", "name": "Comforter", "sub": "Warm cover", "price": 3999, "colors": ["#FFF", "#87CEEB"], "sizes": ["Queen"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=400", "details": ["Soft", "Warm", "Easy care", "Lightweight"]},
                    {"id": "HOME-009", "name": "Mattress Protector", "sub": "Mattress care", "price": 899, "colors": ["#FFF"], "sizes": ["Queen"], "badge": None, "img": "https://images.unsplash.com/photo-1578500494198-246f612d03b3?w=400", "details": ["Waterproof", "Breathable", "Hypoallergenic", "Easy wash"]},
                    {"id": "HOME-010", "name": "Blanket", "sub": "Cozy warmth", "price": 1499, "colors": ["#000"], "sizes": ["Onesize"], "badge": "New", "img": "https://images.unsplash.com/photo-1584622181563-430f63602d4b?w=400", "details": ["Soft", "Portable", "Durable", "Machine wash"]},
                ]
            },
            "furniture": {
                "display_name": "Furniture",
                "products": [
                    {"id": "HOME-011", "name": "Wooden Chair", "sub": "Solid seating", "price": 4999, "colors": ["#8B4513"], "sizes": ["Onesize"], "badge": None, "img": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400", "details": ["Solid wood", "Sturdy", "Comfortable", "Durable"]},
                    {"id": "HOME-012", "name": "Dining Table", "sub": "Family meal center", "price": 12999, "colors": ["#8B4513"], "sizes": ["4-seater"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1581287720244-80d29270e647?w=400", "details": ["Wooden top", "Metal base", "Spacious", "Modern design"]},
                    {"id": "HOME-013", "name": "Bookshelf", "sub": "Storage solution", "price": 7999, "colors": ["#FFF"], "sizes": ["5-shelf"], "badge": None, "img": "https://images.unsplash.com/photo-1565183868294-7563f3ce63c8?w=400", "details": ["Wooden", "Spacious", "Sturdy", "Modern style"]},
                    {"id": "HOME-014", "name": "Sofa", "sub": "Comfort seating", "price": 24999, "colors": ["#191919"], "sizes": ["3-seater"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400", "details": ["Comfortable", "Durable", "Modern", "Easy clean"]},
                    {"id": "HOME-015", "name": "Side Table", "sub": "Accent piece", "price": 3999, "colors": ["#8B4513"], "sizes": ["Onesize"], "badge": "New", "img": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400", "details": ["Wooden", "Compact", "Elegant", "Functional"]},
                ]
            },
            "decor": {
                "display_name": "Decor",
                "products": [
                    {"id": "HOME-016", "name": "Wall Art", "sub": "Wall decoration", "price": 1999, "colors": ["#000"], "sizes": ["Onesize"], "badge": None, "img": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=400", "details": ["Framed", "Modern", "Stylish", "Easy hang"]},
                    {"id": "HOME-017", "name": "Throw Pillows", "sub": "Sofa accent", "price": 799, "colors": ["#FF1493", "#87CEEB"], "sizes": ["Onesize"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "details": ["Soft", "Colorful", "Comfortable", "Easy wash"]},
                    {"id": "HOME-018", "name": "Curtains", "sub": "Window cover", "price": 2499, "colors": ["#FFF", "#191919"], "sizes": ["Onesize"], "badge": None, "img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400", "details": ["Elegant", "Blackout", "Easy hang", "Durable"]},
                    {"id": "HOME-019", "name": "Plant Pot", "sub": "Plant container", "price": 599, "colors": ["#8B4513"], "sizes": ["6 inch"], "badge": "New", "img": "https://images.unsplash.com/photo-1585068934529-fb0d0656b90f?w=400", "details": ["Ceramic", "Durable", "Stylish", "Drainage hole"]},
                    {"id": "HOME-020", "name": "Mirror", "sub": "Reflection piece", "price": 1999, "colors": ["#191919"], "sizes": ["Onesize"], "badge": None, "img": "https://images.unsplash.com/photo-1581430872221-d1cfed785922?w=400", "details": ["Framed", "Clear reflection", "Modern", "Easy mount"]},
                ]
            },
            "appliances": {
                "display_name": "Appliances",
                "products": [
                    {"id": "HOME-021", "name": "Microwave Oven", "sub": "Quick cooking", "price": 8999, "colors": ["#000"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400", "details": ["25L capacity", "6 power levels", "Digital display", "Timer function"]},
                    {"id": "HOME-022", "name": "Toaster", "sub": "Bread toasting", "price": 1999, "colors": ["#191919"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400", "details": ["2 slots", "6 settings", "Cancel button", "Compact"]},
                    {"id": "HOME-023", "name": "Coffee Maker", "sub": "Morning brew", "price": 2999, "colors": ["#000"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1517668808822-9ebb02ae2a0e?w=400", "details": ["12-cup capacity", "Auto shut-off", "Brew timer", "Easy clean"]},
                    {"id": "HOME-024", "name": "Blender", "sub": "Smoothie maker", "price": 3499, "colors": ["#191919"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1570197571499-166b36435e9f?w=400", "details": ["1000W power", "6 speeds", "Glass pitcher", "Durable blades"]},
                    {"id": "HOME-025", "name": "Vacuum Cleaner", "sub": "Floor cleaning", "price": 12999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?w=400", "details": ["Powerful suction", "HEPA filter", "Cordless", "Lightweight"]},
                ]
            },
        }
    },
    "books": {
        "name": "Books",
        "subcategories": {
            "fiction": {
                "display_name": "Fiction",
                "products": [
                    {"id": "BOOK-001", "name": "The Great Gatsby", "sub": "Classic novel", "price": 399, "colors": [], "sizes": [], "badge": "Classic", "img": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400", "details": ["F. Scott Fitzgerald", "Classic", "English", "Paperback"]},
                    {"id": "BOOK-002", "name": "To Kill a Mockingbird", "sub": "American classic", "price": 349, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400", "details": ["Harper Lee", "Classic", "English", "Paperback"]},
                    {"id": "BOOK-003", "name": "1984", "sub": "Dystopian novel", "price": 399, "colors": [], "sizes": [], "badge": "Popular", "img": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400", "details": ["George Orwell", "Fiction", "English", "Paperback"]},
                    {"id": "BOOK-004", "name": "Pride and Prejudice", "sub": "Romance classic", "price": 349, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400", "details": ["Jane Austen", "Classic", "English", "Paperback"]},
                    {"id": "BOOK-005", "name": "The Hobbit", "sub": "Fantasy adventure", "price": 449, "colors": [], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400", "details": ["J.R.R. Tolkien", "Fantasy", "English", "Hardcover"]},
                ]
            },
            "nonfiction": {
                "display_name": "Non-Fiction",
                "products": [
                    {"id": "BOOK-006", "name": "Atomic Habits", "sub": "Self improvement", "price": 449, "colors": [], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400", "details": ["James Clear", "Self-help", "English", "Paperback"]},
                    {"id": "BOOK-007", "name": "Thinking Fast and Slow", "sub": "Psychology", "price": 599, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=400", "details": ["Daniel Kahneman", "Psychology", "English", "Hardcover"]},
                    {"id": "BOOK-008", "name": "Sapiens", "sub": "History", "price": 549, "colors": [], "sizes": [], "badge": "Popular", "img": "https://images.unsplash.com/photo-1550399105-c4db5fb85c18?w=400", "details": ["Yuval Noah Harari", "History", "English", "Paperback"]},
                    {"id": "BOOK-009", "name": "The Innovators", "sub": "Technology history", "price": 499, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400", "details": ["Walter Isaacson", "Tech", "English", "Hardcover"]},
                    {"id": "BOOK-010", "name": "Educated", "sub": "Memoir", "price": 449, "colors": [], "sizes": [], "badge": "Award winner", "img": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=400", "details": ["Tara Westover", "Memoir", "English", "Paperback"]},
                ]
            },
            "educational": {
                "display_name": "Educational",
                "products": [
                    {"id": "BOOK-011", "name": "Math Textbook", "sub": "Learning resource", "price": 299, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1507842217343-583f7270bfbb?w=400", "details": ["Comprehensive", "Exercises", "Solutions", "Illustrated"]},
                    {"id": "BOOK-012", "name": "Science Guide", "sub": "Study material", "price": 349, "colors": [], "sizes": [], "badge": "Popular", "img": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400", "details": ["Detailed", "Diagrams", "Clear", "Comprehensive"]},
                    {"id": "BOOK-013", "name": "English Grammar", "sub": "Language skills", "price": 279, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400", "details": ["Rules", "Examples", "Practice", "Clear"]},
                    {"id": "BOOK-014", "name": "History Notes", "sub": "Reference guide", "price": 249, "colors": [], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400", "details": ["Concise", "Important", "Facts", "Timeline"]},
                    {"id": "BOOK-015", "name": "Coding Basics", "sub": "Programming guide", "price": 399, "colors": [], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400", "details": ["Step-by-step", "Examples", "Practical", "Beginner-friendly"]},
                ]
            },
            "comics": {
                "display_name": "Comics",
                "products": [
                    {"id": "BOOK-016", "name": "Manga Vol 1", "sub": "Japanese comics", "price": 299, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400", "details": ["Illustrated", "Action", "Japanese", "Series"]},
                    {"id": "BOOK-017", "name": "Graphic Novel", "sub": "Visual storytelling", "price": 499, "colors": [], "sizes": [], "badge": "Popular", "img": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400", "details": ["Illustrated", "Adult", "Modern", "Award-winning"]},
                    {"id": "BOOK-018", "name": "Comic Series", "sub": "Ongoing story", "price": 199, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=400", "details": ["Adventure", "Colorful", "Exciting", "Continued"]},
                    {"id": "BOOK-019", "name": "Anime Comics", "sub": "Japanese animation", "price": 349, "colors": [], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1550399105-c4db5fb85c18?w=400", "details": ["Anime adaptation", "Illustrated", "Popular", "Series"]},
                    {"id": "BOOK-020", "name": "Adventure Comics", "sub": "Action packed", "price": 279, "colors": [], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400", "details": ["Exciting", "Illustrated", "Colorful", "Fun"]},
                ]
            },
            "reference": {
                "display_name": "Reference",
                "products": [
                    {"id": "BOOK-021", "name": "Dictionary", "sub": "Word reference", "price": 599, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=400", "details": ["Comprehensive", "Definitions", "Pronunciations", "Examples"]},
                    {"id": "BOOK-022", "name": "Encyclopedia", "sub": "Knowledge base", "price": 799, "colors": [], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1507842217343-583f7270bfbb?w=400", "details": ["Complete", "Illustrated", "Detailed", "Multiple volumes"]},
                    {"id": "BOOK-023", "name": "Atlas", "sub": "World maps", "price": 499, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400", "details": ["Detailed maps", "Countries", "Geography", "Colors"]},
                    {"id": "BOOK-024", "name": "Thesaurus", "sub": "Synonym reference", "price": 449, "colors": [], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400", "details": ["Synonyms", "Antonyms", "Usage", "Comprehensive"]},
                    {"id": "BOOK-025", "name": "Almanac", "sub": "Annual facts", "price": 349, "colors": [], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400", "details": ["Annual", "Facts", "Data", "Updated"]},
                ]
            },
        }
    },
    "sports": {
        "name": "Sports",
        "subcategories": {
            "equipment": {
                "display_name": "Equipment",
                "products": [
                    {"id": "SPORT-001", "name": "Football", "sub": "Soccer ball", "price": 799, "colors": ["#000"], "sizes": ["5"], "badge": None, "img": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400", "details": ["Official size", "Durable", "PU leather", "Perfect grip"]},
                    {"id": "SPORT-002", "name": "Cricket Bat", "sub": "Willow bat", "price": 2999, "colors": ["#8B4513"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=400", "details": ["English willow", "Grade 1", "Professional", "Lightweight"]},
                    {"id": "SPORT-003", "name": "Tennis Racket", "sub": "Aluminum frame", "price": 3999, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1527365828478-c6bbc84f0122?w=400", "details": ["Graphite", "27 inch", "Durable strings", "Good balance"]},
                    {"id": "SPORT-004", "name": "Basketball", "sub": "Game ball", "price": 999, "colors": ["#FF6600"], "sizes": ["7"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400", "details": ["Official size", "Rubber material", "Great bounce", "Durable"]},
                    {"id": "SPORT-005", "name": "Badminton Set", "sub": "Complete kit", "price": 1499, "colors": [], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400", "details": ["2 rackets", "Shuttlecocks", "Net", "Portable"]},
                ]
            },
            "apparel": {
                "display_name": "Apparel",
                "products": [
                    {"id": "SPORT-006", "name": "Sports Jersey", "sub": "Team wear", "price": 1299, "colors": ["#000"], "sizes": ["S","M","L","XL"], "badge": None, "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "details": ["Moisture-wicking", "Lightweight", "Durable", "Quick-dry"]},
                    {"id": "SPORT-007", "name": "Gym Shorts", "sub": "Athletic wear", "price": 899, "colors": ["#000", "#FFF"], "sizes": ["S","M","L","XL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1600080972464-8e5f801ecefd?w=400", "details": ["Comfortable", "Breathable", "Elastic waist", "Pockets"]},
                    {"id": "SPORT-008", "name": "Sports Bra", "sub": "Women support", "price": 1499, "colors": ["#000"], "sizes": ["S","M","L"], "badge": None, "img": "https://images.unsplash.com/photo-1600080972464-8e5f801ecefd?w=400", "details": ["High support", "Breathable", "Comfortable", "Durable"]},
                    {"id": "SPORT-009", "name": "Track Pants", "sub": "Training wear", "price": 1999, "colors": ["#191919"], "sizes": ["S","M","L","XL"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1600080972464-8e5f801ecefd?w=400", "details": ["Tapered fit", "Moisture-wicking", "Comfortable", "Stylish"]},
                    {"id": "SPORT-010", "name": "Compression Wear", "sub": "Performance gear", "price": 1699, "colors": ["#000"], "sizes": ["S","M","L","XL"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1600080972464-8e5f801ecefd?w=400", "details": ["Compression fabric", "Muscle support", "Breathable", "Durable"]},
                ]
            },
            "outdoor": {
                "display_name": "Outdoor",
                "products": [
                    {"id": "SPORT-011", "name": "Tent", "sub": "Camping shelter", "price": 4999, "colors": ["#191919"], "sizes": ["2-person"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400", "details": ["Easy setup", "Waterproof", "Durable", "Lightweight"]},
                    {"id": "SPORT-012", "name": "Camping Bag", "sub": "Travel pack", "price": 3499, "colors": ["#191919"], "sizes": ["60L"], "badge": None, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "details": ["Large capacity", "Comfortable", "Durable straps", "Waterproof"]},
                    {"id": "SPORT-013", "name": "Sleeping Bag", "sub": "Bedding for camping", "price": 2999, "colors": ["#000"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400", "details": ["Warm", "Waterproof", "Portable", "Lightweight"]},
                    {"id": "SPORT-014", "name": "Hiking Boot", "sub": "Mountain shoes", "price": 3999, "colors": ["#8B4513"], "sizes": ["6","7","8","9","10"], "badge": None, "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "details": ["Ankle support", "Waterproof", "Durable", "Comfortable"]},
                    {"id": "SPORT-015", "name": "Backpack", "sub": "Hiking pack", "price": 2499, "colors": ["#191919"], "sizes": ["50L"], "badge": "New", "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "details": ["Ergonomic", "Multiple pockets", "Ventilated", "Durable"]},
                ]
            },
            "fitness": {
                "display_name": "Fitness",
                "products": [
                    {"id": "SPORT-016", "name": "Dumbbell Set", "sub": "Strength training", "price": 3999, "colors": ["#000"], "sizes": ["5kg"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1517836357463-d25ddfcbf042?w=400", "details": ["Adjustable", "Non-slip grip", "Durable", "Complete set"]},
                    {"id": "SPORT-017", "name": "Resistance Band", "sub": "Elastic training", "price": 499, "colors": ["#FF1493"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45b?w=400", "details": ["Multiple resistance", "Portable", "Versatile", "Durable"]},
                    {"id": "SPORT-018", "name": "Yoga Mat", "sub": "Exercise pad", "price": 899, "colors": ["#191919"], "sizes": ["173cm"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1517836357463-d25ddfcbf042?w=400", "details": ["Non-slip", "Cushioned", "Portable", "Durable"]},
                    {"id": "SPORT-019", "name": "Jump Rope", "sub": "Cardio equipment", "price": 299, "colors": ["#000"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1517836357463-d25ddfcbf042?w=400", "details": ["Adjustable length", "Speed rope", "Light", "Durable"]},
                    {"id": "SPORT-020", "name": "Fitness Tracker", "sub": "Activity monitor", "price": 4999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1575505586569-646b2ca898fc?w=400", "details": ["Heart rate", "Steps tracking", "Sleep monitor", "Smart band"]},
                ]
            },
            "games": {
                "display_name": "Games",
                "products": [
                    {"id": "SPORT-021", "name": "Board Game", "sub": "Family fun", "price": 999, "colors": [], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=400", "details": ["Strategy game", "2-4 players", "Fun", "Educational"]},
                    {"id": "SPORT-022", "name": "Chess Set", "sub": "Classic game", "price": 1499, "colors": ["#191919"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400", "details": ["Wooden pieces", "Storage board", "Professional", "Classic"]},
                    {"id": "SPORT-023", "name": "Puzzle Game", "sub": "Brain teaser", "price": 599, "colors": [], "sizes": ["1000 pieces"], "badge": None, "img": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=400", "details": ["Challenging", "Colorful", "Quality print", "Complete set"]},
                    {"id": "SPORT-024", "name": "Card Game", "sub": "Quick play", "price": 299, "colors": [], "sizes": [], "badge": "Popular", "img": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=400", "details": ["Easy rules", "Fast paced", "Portable", "Fun"]},
                    {"id": "SPORT-025", "name": "Video Game Console", "sub": "Gaming", "price": 34999, "colors": ["#000"], "sizes": [], "badge": "Premium", "img": "https://images.unsplash.com/photo-1550258987-920a2eae4da1?w=400", "details": ["Latest generation", "Powerful", "Games included", "Online ready"]},
                ]
            },
        }
    },
    "beauty": {
        "name": "Beauty",
        "subcategories": {
            "skincare": {
                "display_name": "Skincare",
                "products": [
                    {"id": "BEAUTY-001", "name": "Face Wash", "sub": "Daily cleansing", "price": 399, "colors": [], "sizes": ["100ml"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "details": ["Gentle formula", "Natural", "Skin-friendly", "Daily use"]},
                    {"id": "BEAUTY-002", "name": "Moisturizer", "sub": "Hydration cream", "price": 699, "colors": [], "sizes": ["50ml"], "badge": None, "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400", "details": ["Deep hydration", "Light texture", "Natural", "All skin types"]},
                    {"id": "BEAUTY-003", "name": "Face Mask", "sub": "Treatment mask", "price": 299, "colors": [], "sizes": ["pack"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "details": ["Sheet mask", "Nourishing", "Easy apply", "Relaxing"]},
                    {"id": "BEAUTY-004", "name": "Sunscreen", "sub": "UV protection", "price": 499, "colors": [], "sizes": ["75ml"], "badge": None, "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "details": ["SPF 50", "Water resistant", "Natural", "Non-greasy"]},
                    {"id": "BEAUTY-005", "name": "Serum", "sub": "Concentrated care", "price": 899, "colors": [], "sizes": ["30ml"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400", "details": ["Vitamin C", "Anti-aging", "Brightening", "Powerful"]},
                ]
            },
            "makeup": {
                "display_name": "Makeup",
                "products": [
                    {"id": "BEAUTY-006", "name": "Foundation", "sub": "Base makeup", "price": 599, "colors": ["Shade 1"], "sizes": ["30ml"], "badge": None, "img": "https://images.unsplash.com/photo-1596289519271-78246ebc6b08?w=400", "details": ["Long-lasting", "Natural finish", "Matte", "Full coverage"]},
                    {"id": "BEAUTY-007", "name": "Lipstick", "sub": "Lip color", "price": 399, "colors": ["Red"], "sizes": [], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400", "details": ["Vibrant color", "Smooth texture", "Long wear", "Moisturizing"]},
                    {"id": "BEAUTY-008", "name": "Eyeshadow Palette", "sub": "Eye colors", "price": 899, "colors": [], "sizes": ["12 shades"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1596289519271-78246ebc6b08?w=400", "details": ["Blendable", "Pigmented", "Long-lasting", "Versatile"]},
                    {"id": "BEAUTY-009", "name": "Mascara", "sub": "Lash enhancement", "price": 349, "colors": ["Black"], "sizes": [], "badge": None, "img": "https://images.unsplash.com/photo-1596289519271-78246ebc6b08?w=400", "details": ["Volumizing", "Waterproof", "Long-lasting", "Easy apply"]},
                    {"id": "BEAUTY-010", "name": "Blush", "sub": "Face color", "price": 449, "colors": ["Pink"], "sizes": [], "badge": "New", "img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400", "details": ["Natural flush", "Blendable", "Pigmented", "Soft texture"]},
                ]
            },
            "haircare": {
                "display_name": "Haircare",
                "products": [
                    {"id": "BEAUTY-011", "name": "Shampoo", "sub": "Hair wash", "price": 299, "colors": [], "sizes": ["200ml"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "details": ["Gentle formula", "Cleansing", "Natural", "All hair types"]},
                    {"id": "BEAUTY-012", "name": "Conditioner", "sub": "Hair treatment", "price": 329, "colors": [], "sizes": ["200ml"], "badge": None, "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "details": ["Moisturizing", "Smooth hair", "Nourishing", "Silky feel"]},
                    {"id": "BEAUTY-013", "name": "Hair Oil", "sub": "Scalp treatment", "price": 199, "colors": [], "sizes": ["100ml"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "details": ["Natural oils", "Strengthening", "Nourishing", "Massage"]},
                    {"id": "BEAUTY-014", "name": "Hair Mask", "sub": "Deep conditioning", "price": 449, "colors": [], "sizes": ["200ml"], "badge": None, "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400", "details": ["Intensive care", "Moisturizing", "Repair", "Weekly use"]},
                    {"id": "BEAUTY-015", "name": "Hair Serum", "sub": "Shine booster", "price": 379, "colors": [], "sizes": ["50ml"], "badge": "New", "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400", "details": ["Frizz control", "Shiny", "Smooth", "Light formula"]},
                ]
            },
            "fragrance": {
                "display_name": "Fragrance",
                "products": [
                    {"id": "BEAUTY-016", "name": "Perfume", "sub": "Eau de parfum", "price": 1999, "colors": [], "sizes": ["50ml"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1541643600914-78b084683702?w=400", "details": ["Long-lasting", "Luxurious", "Intense", "Premium scent"]},
                    {"id": "BEAUTY-017", "name": "Body Spray", "sub": "Light fragrance", "price": 399, "colors": [], "sizes": ["200ml"], "badge": None, "img": "https://images.unsplash.com/photo-1587556930799-8dca1f6f02a1?w=400", "details": ["Refreshing", "Light scent", "Quick dry", "Daily use"]},
                    {"id": "BEAUTY-018", "name": "Cologne", "sub": "Fresh scent", "price": 1499, "colors": [], "sizes": ["100ml"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400", "details": ["Masculine", "Fresh", "Long-lasting", "Premium"]},
                    {"id": "BEAUTY-019", "name": "Deodorant", "sub": "Odor protection", "price": 249, "colors": [], "sizes": ["150ml"], "badge": None, "img": "https://images.unsplash.com/photo-1590156206657-aff38c0e9d7d?w=400", "details": ["24hr protection", "Fresh scent", "Gentle", "Daily use"]},
                    {"id": "BEAUTY-020", "name": "Fragrance Oil", "sub": "Essential oils", "price": 599, "colors": [], "sizes": ["30ml"], "badge": "New", "img": "https://images.unsplash.com/photo-1547887537-6158d64c35b3?w=400", "details": ["Concentrated", "Pure oils", "Natural", "Multipurpose"]},
                ]
            },
            "wellness": {
                "display_name": "Wellness",
                "products": [
                    {"id": "BEAUTY-021", "name": "Vitamin Supplement", "sub": "Nutritional support", "price": 449, "colors": [], "sizes": ["60 tablets"], "badge": None, "img": "https://images.unsplash.com/photo-1584577860890-c73a7a01cf59?w=400", "details": ["Essential vitamins", "Daily support", "Natural", "Quality"]},
                    {"id": "BEAUTY-022", "name": "Protein Powder", "sub": "Fitness supplement", "price": 999, "colors": [], "sizes": ["500g"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1584577860890-c73a7a01cf59?w=400", "details": ["Muscle building", "Easy mix", "Natural", "Tasty"]},
                    {"id": "BEAUTY-023", "name": "Multivitamin", "sub": "Overall health", "price": 399, "colors": [], "sizes": ["60 tablets"], "badge": "Popular", "img": "https://images.unsplash.com/photo-1584577860890-c73a7a01cf59?w=400", "details": ["Complete nutrition", "Daily", "Safe", "Effective"]},
                    {"id": "BEAUTY-024", "name": "Herbal Tea", "sub": "Wellness drink", "price": 299, "colors": [], "sizes": ["25 bags"], "badge": None, "img": "https://images.unsplash.com/photo-1597318972767-42e70d54d17c?w=400", "details": ["Organic", "Relaxing", "Natural", "Healthy"]},
                    {"id": "BEAUTY-025", "name": "Wellness Drink", "sub": "Health elixir", "price": 599, "colors": [], "sizes": ["250ml"], "badge": "New", "img": "https://images.unsplash.com/photo-1597318972767-42e70d54d17c?w=400", "details": ["Energizing", "Natural", "Nutrient-rich", "Daily boost"]},
                ]
            },
        }
    },
}


async def seed_database():
    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(select(Product).limit(1))
        if result.scalar():
            print("Database already seeded, skipping.")
            return

        # Create categories and subcategories
        for category_slug, category_data in CATALOG.items():
            category = Category(name=category_data["name"], slug=category_slug)
            session.add(category)
            await session.flush()

            for subcategory_slug, subcategory_data in category_data["subcategories"].items():
                subcategory = Subcategory(
                    category_id=category.id,
                    name=subcategory_data["display_name"],
                    slug=subcategory_slug,
                    display_name=subcategory_data["display_name"],
                )
                session.add(subcategory)
                await session.flush()

                # Create products
                for product_data in subcategory_data["products"]:
                    product = Product(
                        id=product_data["id"],
                        subcategory_id=subcategory.id,
                        name=product_data["name"],
                        subtitle=product_data.get("sub", ""),
                        price=product_data.get("price", 0),
                        original_price=None,
                        image_url=product_data.get("img", ""),
                        colors=product_data.get("colors", []),
                        sizes=product_data.get("sizes", []),
                        badge=product_data.get("badge"),
                        details=product_data.get("details", []),
                    )
                    session.add(product)

        await session.commit()
        print("Database seeded with full catalog!")
