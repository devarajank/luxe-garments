"""Seed the product database with Luxe Garments catalog."""
from app.database import async_session
from app.models import Category, Category, Subcategory, Product
from sqlalchemy import select


CATALOG = {
    "men": {
        "name": "Men",
        "subcategories": {
            "jeans": {
                "display_name": "Jeans",
                "products": [
                    {"id": "m-j-1", "name": "501 Original Fit Jeans", "sub": "Classic straight leg", "price": 89, "originalPrice": 98, "colors": ["#1B3A5C", "#2C2C2C"], "sizes": ["28","30","32","34","36"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400", "details": ["100% Cotton denim","Button fly","Straight leg","Classic rise"]},
                    {"id": "m-j-2", "name": "511 Slim Fit Jeans", "sub": "Modern slim cut", "price": 79, "colors": ["#1B3A5C", "#3D3D3D", "#4A3728"], "sizes": ["28","30","32","34","36"], "badge": "New", "img": "https://images.unsplash.com/photo-1604176354204-9268737828e4?w=400", "details": ["98% Cotton, 2% Elastane","Zip fly","Slim through hip and thigh","Narrow leg opening"]},
                    {"id": "m-j-3", "name": "502 Taper Fit Jeans", "sub": "Room to move", "price": 84, "colors": ["#1B3A5C", "#191919"], "sizes": ["30","32","34","36"], "img": "https://images.unsplash.com/photo-1605518216938-7c31b7b14ad0?w=400", "details": ["99% Cotton, 1% Elastane","Sits at waist","Regular through thigh","Tapered leg"]},
                    {"id": "m-j-4", "name": "505 Regular Fit Jeans", "sub": "Timeless regular", "price": 69, "originalPrice": 79, "colors": ["#2C2C2C", "#1B3A5C"], "sizes": ["30","32","34","36","38"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=400", "details": ["100% Cotton","Zip fly","Straight through thigh","Regular fit"]},
                    {"id": "m-j-5", "name": "Relaxed Carpenter Jeans", "sub": "Workwear inspired", "price": 94, "colors": ["#4A3728", "#1B3A5C"], "sizes": ["30","32","34","36"], "img": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=400", "details": ["Heavy duty cotton","Utility pockets","Relaxed fit","Hammer loop"]},
                    {"id": "m-j-6", "name": "Athletic Fit Jeans", "sub": "Built for movement", "price": 88, "colors": ["#1B3A5C", "#2C2C2C"], "sizes": ["30","32","34","36"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400", "details": ["96% Cotton, 4% Elastane","Extra room in thigh","Tapered below knee","Stretch comfort"]},
                    {"id": "m-j-7", "name": "Skinny Fit Jeans", "sub": "Most narrow fit", "price": 75, "colors": ["#191919", "#1B3A5C"], "sizes": ["28","30","32","34"], "img": "https://images.unsplash.com/photo-1555689502-c4b22d76c56f?w=400", "details": ["93% Cotton, 5% Polyester, 2% Elastane","Super skinny","Low rise","Narrow leg"]},
                    {"id": "m-j-8", "name": "Bootcut Classic Jeans", "sub": "Over-the-boot style", "price": 82, "colors": ["#1B3A5C"], "sizes": ["30","32","34","36","38"], "img": "https://images.unsplash.com/photo-1475178626620-a4d074967571?w=400", "details": ["100% Cotton","Bootcut leg","Classic rise","Relaxed seat"]},
                    {"id": "m-j-9", "name": "Selvedge Denim Jeans", "sub": "Premium Japanese denim", "price": 148, "colors": ["#191919"], "sizes": ["30","32","34"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1593091861277-a36c6c17bcca?w=400", "details": ["Japanese selvedge denim","Self-finished edges","Raw unwashed","14oz weight"]},
                    {"id": "m-j-10", "name": "Loose Fit Cargo Jeans", "sub": "Street style cargo", "price": 92, "colors": ["#4A3728", "#2C2C2C"], "sizes": ["30","32","34","36"], "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400", "details": ["Cotton blend","Cargo pockets","Loose through leg","Utility styling"]},
                ],
            },
            "jackets": {
                "display_name": "Jackets",
                "products": [
                    {"id": "m-k-1", "name": "Trucker Jacket", "sub": "Classic denim jacket", "price": 108, "colors": ["#1B3A5C", "#2C2C2C"], "sizes": ["S","M","L","XL"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400", "details": ["100% Cotton denim","Button front","Chest pockets","Adjustable waist tabs"]},
                    {"id": "m-k-2", "name": "Sherpa Trucker Jacket", "sub": "Warm lined jacket", "price": 148, "colors": ["#1B3A5C"], "sizes": ["S","M","L","XL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=400", "details": ["Denim with sherpa lining","Button front","Warm for winter","Chest pockets"]},
                    {"id": "m-k-3", "name": "Leather Moto Jacket", "sub": "Genuine leather", "price": 298, "colors": ["#191919", "#4A3728"], "sizes": ["S","M","L","XL"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1520975954732-35dd22299614?w=400", "details": ["Genuine leather","Asymmetric zip","Moto style","Zippered pockets"]},
                    {"id": "m-k-4", "name": "Bomber Jacket", "sub": "Lightweight nylon", "price": 118, "colors": ["#2C2C2C", "#0A1628"], "sizes": ["S","M","L","XL","XXL"], "img": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "details": ["Nylon shell","Ribbed cuffs and hem","Zip front","Lightweight"]},
                    {"id": "m-k-5", "name": "Corduroy Trucker Jacket", "sub": "Retro texture", "price": 112, "colors": ["#4A3728", "#6B4226"], "sizes": ["S","M","L","XL"], "badge": "New", "img": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400", "details": ["Cotton corduroy","Button front","Retro inspired","Chest pockets"]},
                    {"id": "m-k-6", "name": "Hooded Utility Jacket", "sub": "Weatherproof layer", "price": 138, "colors": ["#2C2C2C", "#3D5A3D"], "sizes": ["M","L","XL"], "img": "https://images.unsplash.com/photo-1495105787522-5334e726fa0d?w=400", "details": ["Water-resistant","Detachable hood","Multiple pockets","Drawstring waist"]},
                    {"id": "m-k-7", "name": "Quilted Shirt Jacket", "sub": "Layering essential", "price": 128, "colors": ["#191919", "#0A1628"], "sizes": ["S","M","L","XL"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1557418669-50db9d640a5e?w=400", "details": ["Quilted insulation","Snap buttons","Shirt-jacket hybrid","Lightweight warmth"]},
                    {"id": "m-k-8", "name": "Denim Vest", "sub": "Sleeveless classic", "price": 78, "colors": ["#1B3A5C"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400", "details": ["100% Cotton denim","Button front","Chest pockets","Classic fit"]},
                    {"id": "m-k-9", "name": "Parka Coat", "sub": "Cold weather essential", "price": 198, "colors": ["#0A1628", "#2C2C2C"], "sizes": ["S","M","L","XL"], "badge": "Limited", "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400", "details": ["Insulated fill","Faux fur hood","Water resistant","Below hip length"]},
                    {"id": "m-k-10", "name": "Lightweight Coach Jacket", "sub": "Snap-front style", "price": 88, "colors": ["#191919", "#C41230"], "sizes": ["S","M","L","XL","XXL"], "img": "https://images.unsplash.com/photo-1548883354-94bcfe321cbb?w=400", "details": ["Nylon shell","Snap front","Coach style","Packable"]},
                ],
            },
            "tshirts": {
                "display_name": "T-Shirts",
                "products": [
                    {"id": "m-t-1", "name": "Classic Logo Tee", "sub": "Iconic brand tee", "price": 29, "colors": ["#FFFFFF", "#191919", "#C41230"], "sizes": ["S","M","L","XL","XXL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "details": ["100% Cotton","Crew neck","Short sleeve","Screen-printed logo"]},
                    {"id": "m-t-2", "name": "Pocket Tee", "sub": "Everyday essential", "price": 25, "colors": ["#FFFFFF", "#0A1628", "#808080"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=400", "details": ["Cotton jersey","Chest pocket","Relaxed fit","Pre-shrunk"]},
                    {"id": "m-t-3", "name": "Graphic Band Tee", "sub": "Rock inspired", "price": 34, "colors": ["#191919", "#2C2C2C"], "sizes": ["S","M","L","XL"], "badge": "New", "img": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400", "details": ["Cotton blend","Graphic print","Vintage wash","Regular fit"]},
                    {"id": "m-t-4", "name": "V-Neck Slim Tee", "sub": "Clean v-neck", "price": 27, "colors": ["#FFFFFF", "#191919", "#0A1628"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400", "details": ["95% Cotton, 5% Elastane","V-neck","Slim fit","Stretch fabric"]},
                    {"id": "m-t-5", "name": "Henley Long Sleeve", "sub": "Button placket", "price": 39, "colors": ["#808080", "#0A1628", "#4A3728"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1618517351616-38fb9c5210c6?w=400", "details": ["Cotton waffle knit","3-button placket","Long sleeve","Regular fit"]},
                    {"id": "m-t-6", "name": "Striped Crew Tee", "sub": "Nautical stripes", "price": 32, "colors": ["#0A1628"], "sizes": ["S","M","L","XL"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1554568218-0f1715e72254?w=400", "details": ["100% Cotton","Horizontal stripes","Crew neck","Regular fit"]},
                    {"id": "m-t-7", "name": "Oversized Box Tee", "sub": "Streetwear cut", "price": 35, "colors": ["#191919", "#FFFFFF", "#808080"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1503341504253-dff4f94032ef?w=400", "details": ["Heavy cotton","Dropped shoulders","Oversized fit","Boxy silhouette"]},
                    {"id": "m-t-8", "name": "Performance Tee", "sub": "Moisture wicking", "price": 38, "colors": ["#191919", "#0A1628", "#808080"], "sizes": ["S","M","L","XL","XXL"], "img": "https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=400", "details": ["Polyester blend","Moisture-wicking","Athletic fit","Breathable mesh"]},
                    {"id": "m-t-9", "name": "Tie-Dye Festival Tee", "sub": "Colorful vibes", "price": 36, "colors": ["#C41230", "#1B3A5C"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1596609548086-85bbf8ddb6b6?w=400", "details": ["100% Cotton","Tie-dye pattern","Relaxed fit","Unique wash"]},
                    {"id": "m-t-10", "name": "Thermal Waffle Tee", "sub": "Warm base layer", "price": 34, "colors": ["#FFFFFF", "#191919", "#4A3728"], "sizes": ["S","M","L","XL"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400", "details": ["Cotton waffle knit","Crew neck","Long sleeve","Thermal weight"]},
                ],
            },
            "shirts": {
                "display_name": "Shirts",
                "products": [
                    {"id": "m-s-1", "name": "Western Denim Shirt", "sub": "Snap button front", "price": 68, "colors": ["#1B3A5C", "#808080"], "sizes": ["S","M","L","XL"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400", "details": ["100% Cotton denim","Pearl snap buttons","Pointed collar","Western yoke"]},
                    {"id": "m-s-2", "name": "Oxford Button-Down", "sub": "Smart casual staple", "price": 58, "colors": ["#FFFFFF", "#87CEEB", "#FFC0CB"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400", "details": ["Oxford cotton","Button-down collar","Chest pocket","Regular fit"]},
                    {"id": "m-s-3", "name": "Flannel Check Shirt", "sub": "Soft brushed cotton", "price": 62, "colors": ["#C41230", "#0A1628"], "sizes": ["S","M","L","XL","XXL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1507680434567-5739c80be1ac?w=400", "details": ["Brushed cotton flannel","Check pattern","Button front","Two chest pockets"]},
                    {"id": "m-s-4", "name": "Linen Camp Shirt", "sub": "Resort style", "price": 72, "colors": ["#FFFFFF", "#D4C5A9"], "sizes": ["S","M","L","XL"], "badge": "New", "img": "https://images.unsplash.com/photo-1598032895397-b9472444bf93?w=400", "details": ["100% Linen","Camp collar","Short sleeve","Relaxed fit"]},
                    {"id": "m-s-5", "name": "Chambray Work Shirt", "sub": "Sturdy workwear", "price": 64, "colors": ["#87CEEB", "#1B3A5C"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1589310243389-96a5483213a8?w=400", "details": ["Cotton chambray","Button front","Dual chest pockets","Regular fit"]},
                    {"id": "m-s-6", "name": "Hawaiian Print Shirt", "sub": "Tropical vibes", "price": 55, "colors": ["#0A1628", "#2E8B57"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1580331451062-99ff652288d9?w=400", "details": ["Rayon blend","All-over print","Camp collar","Relaxed fit"]},
                    {"id": "m-s-7", "name": "Corduroy Overshirt", "sub": "Heavy layer shirt", "price": 78, "colors": ["#4A3728", "#6B4226"], "sizes": ["S","M","L","XL"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=400", "details": ["Cotton corduroy","Button front","Chest pockets","Overshirt weight"]},
                    {"id": "m-s-8", "name": "Slim Dress Shirt", "sub": "Formal fit", "price": 65, "colors": ["#FFFFFF", "#87CEEB"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=400", "details": ["Cotton poplin","Point collar","Slim fit","French cuffs"]},
                    {"id": "m-s-9", "name": "Brushed Twill Shirt", "sub": "Soft texture", "price": 58, "colors": ["#808080", "#2C2C2C"], "sizes": ["S","M","L","XL"], "img": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=400", "details": ["Brushed twill cotton","Button front","Soft hand feel","Regular fit"]},
                    {"id": "m-s-10", "name": "Band Collar Shirt", "sub": "Mandarin style", "price": 62, "colors": ["#FFFFFF", "#191919"], "sizes": ["S","M","L","XL"], "badge": "Limited", "img": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400", "details": ["Cotton blend","Band collar","Hidden buttons","Modern fit"]},
                ],
            },
        },
    },
    "women": {
        "name": "Women",
        "subcategories": {
            "jeans": {
                "display_name": "Jeans",
                "products": [
                    {"id": "w-j-1", "name": "High Rise Skinny Jeans", "sub": "Figure-hugging fit", "price": 89, "colors": ["#1B3A5C", "#191919"], "sizes": ["24","26","28","30","32"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400", "details": ["92% Cotton, 6% Polyester, 2% Elastane","High rise","Skinny leg","Stretch denim"]},
                    {"id": "w-j-2", "name": "Mom Jeans", "sub": "Relaxed vintage", "price": 84, "colors": ["#87CEEB", "#1B3A5C"], "sizes": ["24","26","28","30","32"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400", "details": ["100% Cotton","High waist","Tapered leg","Vintage wash"]},
                    {"id": "w-j-3", "name": "Wide Leg Jeans", "sub": "Flowing silhouette", "price": 92, "colors": ["#1B3A5C", "#FFFFFF"], "sizes": ["24","26","28","30"], "badge": "New", "img": "https://images.unsplash.com/photo-1582418702059-97ebafb35d09?w=400", "details": ["Cotton denim","High rise","Wide leg","Full length"]},
                    {"id": "w-j-4", "name": "Straight Leg Crop", "sub": "Ankle length", "price": 78, "colors": ["#191919", "#1B3A5C"], "sizes": ["24","26","28","30","32"], "img": "https://images.unsplash.com/photo-1551854838-212c50b4c184?w=400", "details": ["Stretch denim","Mid rise","Straight leg","Cropped length"]},
                    {"id": "w-j-5", "name": "Bootcut Flare Jeans", "sub": "70s inspired", "price": 86, "colors": ["#1B3A5C"], "sizes": ["24","26","28","30"], "img": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?w=400", "details": ["Cotton blend","High rise","Flared from knee","Vintage vibe"]},
                    {"id": "w-j-6", "name": "Boyfriend Jeans", "sub": "Borrowed-from-him fit", "price": 82, "colors": ["#87CEEB", "#1B3A5C"], "sizes": ["24","26","28","30","32"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=400", "details": ["100% Cotton","Relaxed through hip","Tapered leg","Rolled cuff"]},
                    {"id": "w-j-7", "name": "Sculpt High Rise Jeans", "sub": "Shaping technology", "price": 98, "colors": ["#191919", "#1B3A5C"], "sizes": ["24","26","28","30"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=400", "details": ["Sculpt stretch denim","Tummy smoothing","High rise","Skinny leg"]},
                    {"id": "w-j-8", "name": "Relaxed Cargo Jeans", "sub": "Utility style", "price": 88, "colors": ["#4A3728", "#808080"], "sizes": ["24","26","28","30","32"], "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400", "details": ["Cotton blend","Cargo pockets","Relaxed fit","Mid rise"]},
                    {"id": "w-j-9", "name": "Super Low Rise Jeans", "sub": "Y2K comeback", "price": 76, "colors": ["#1B3A5C", "#87CEEB"], "sizes": ["24","26","28","30"], "img": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400", "details": ["Stretch denim","Super low rise","Bootcut leg","2000s inspired"]},
                    {"id": "w-j-10", "name": "Distressed Mom Jeans", "sub": "Ripped and lived-in", "price": 86, "colors": ["#87CEEB"], "sizes": ["24","26","28","30","32"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1565084888279-aca607ecce0c?w=400", "details": ["Cotton denim","Distressed details","High waist","Relaxed tapered"]},
                ],
            },
            "jackets": {
                "display_name": "Jackets",
                "products": [
                    {"id": "w-k-1", "name": "Cropped Trucker Jacket", "sub": "Waist-length denim", "price": 98, "colors": ["#1B3A5C", "#FFFFFF"], "sizes": ["XS","S","M","L"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=400", "details": ["Cotton denim","Cropped length","Button front","Chest pockets"]},
                    {"id": "w-k-2", "name": "Oversized Denim Jacket", "sub": "Relaxed layer", "price": 118, "colors": ["#87CEEB", "#1B3A5C"], "sizes": ["XS","S","M","L","XL"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=400", "details": ["Cotton denim","Oversized fit","Drop shoulders","Button front"]},
                    {"id": "w-k-3", "name": "Fitted Blazer", "sub": "Tailored look", "price": 148, "colors": ["#191919", "#D4C5A9"], "sizes": ["XS","S","M","L"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "details": ["Stretch blend","Single button","Notch lapel","Fitted silhouette"]},
                    {"id": "w-k-4", "name": "Sherpa Lined Jacket", "sub": "Cozy warmth", "price": 138, "colors": ["#1B3A5C"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=400", "details": ["Denim with sherpa","Button front","Warm lining","Regular length"]},
                    {"id": "w-k-5", "name": "Leather Biker Jacket", "sub": "Edge meets style", "price": 278, "colors": ["#191919"], "sizes": ["XS","S","M","L"], "badge": "Limited", "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400", "details": ["Genuine leather","Asymmetric zip","Belted waist","Moto style"]},
                    {"id": "w-k-6", "name": "Puffer Vest", "sub": "Lightweight warmth", "price": 88, "colors": ["#191919", "#C41230", "#FFFFFF"], "sizes": ["XS","S","M","L","XL"], "badge": "New", "img": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400", "details": ["Nylon shell","Synthetic fill","Zip front","Stand collar"]},
                    {"id": "w-k-7", "name": "Trench Coat", "sub": "Classic elegance", "price": 178, "colors": ["#D4C5A9", "#191919"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400", "details": ["Cotton blend","Double-breasted","Belted waist","Knee length"]},
                    {"id": "w-k-8", "name": "Quilted Shirt Jacket", "sub": "Transitional piece", "price": 108, "colors": ["#808080", "#2C2C2C"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1557418669-50db9d640a5e?w=400", "details": ["Quilted fill","Snap buttons","Patch pockets","Relaxed fit"]},
                    {"id": "w-k-9", "name": "Windbreaker", "sub": "Rain-ready layer", "price": 78, "colors": ["#C41230", "#0A1628"], "sizes": ["XS","S","M","L","XL"], "img": "https://images.unsplash.com/photo-1548883354-94bcfe321cbb?w=400", "details": ["Water-resistant nylon","Half zip","Packable","Lightweight"]},
                    {"id": "w-k-10", "name": "Corduroy Jacket", "sub": "Textured warmth", "price": 108, "colors": ["#4A3728", "#D4C5A9"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=400", "details": ["Cotton corduroy","Button front","Chest pockets","Cropped length"]},
                ],
            },
            "tops": {
                "display_name": "Tops",
                "products": [
                    {"id": "w-t-1", "name": "Relaxed Crew Tee", "sub": "Everyday basics", "price": 28, "colors": ["#FFFFFF", "#191919", "#C41230"], "sizes": ["XS","S","M","L","XL"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "details": ["100% Cotton","Crew neck","Relaxed fit","Short sleeve"]},
                    {"id": "w-t-2", "name": "Cropped Baby Tee", "sub": "Fitted crop", "price": 25, "colors": ["#FFFFFF", "#FFC0CB", "#191919"], "sizes": ["XS","S","M","L"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=400", "details": ["Cotton stretch","Cropped length","Slim fit","Short sleeve"]},
                    {"id": "w-t-3", "name": "Flowy Blouse", "sub": "Feminine drape", "price": 52, "colors": ["#FFFFFF", "#87CEEB", "#FFC0CB"], "sizes": ["XS","S","M","L"], "badge": "New", "img": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=400", "details": ["Lightweight fabric","V-neck","Billowy sleeves","Relaxed fit"]},
                    {"id": "w-t-4", "name": "Ribbed Tank Top", "sub": "Layering staple", "price": 22, "colors": ["#FFFFFF", "#191919", "#808080"], "sizes": ["XS","S","M","L","XL"], "img": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400", "details": ["Ribbed cotton","Scoop neck","Slim fit","Sleeveless"]},
                    {"id": "w-t-5", "name": "Graphic Logo Tee", "sub": "Statement print", "price": 32, "colors": ["#191919", "#FFFFFF"], "sizes": ["XS","S","M","L","XL"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400", "details": ["Cotton jersey","Screen print","Crew neck","Regular fit"]},
                    {"id": "w-t-6", "name": "Off-Shoulder Top", "sub": "Romantic neckline", "price": 38, "colors": ["#FFFFFF", "#C41230"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400", "details": ["Cotton blend","Off-shoulder","Elastic neckline","Relaxed fit"]},
                    {"id": "w-t-7", "name": "Bodysuit", "sub": "Sleek base layer", "price": 35, "colors": ["#191919", "#FFFFFF", "#808080"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400", "details": ["Stretch jersey","Snap closure","Scoop neck","Slim fit"]},
                    {"id": "w-t-8", "name": "Oversized Band Tee", "sub": "Music inspired", "price": 36, "colors": ["#191919", "#2C2C2C"], "sizes": ["XS","S","M","L","XL"], "img": "https://images.unsplash.com/photo-1503341504253-dff4f94032ef?w=400", "details": ["Cotton jersey","Vintage graphics","Oversized","Drop shoulders"]},
                    {"id": "w-t-9", "name": "Wrap Top", "sub": "Adjustable fit", "price": 45, "colors": ["#C41230", "#191919", "#0A1628"], "sizes": ["XS","S","M","L"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400", "details": ["Rayon blend","Wrap front","Tie waist","3/4 sleeves"]},
                    {"id": "w-t-10", "name": "Turtleneck Long Sleeve", "sub": "Elevated basic", "price": 42, "colors": ["#191919", "#FFFFFF", "#808080"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400", "details": ["Cotton blend","Turtleneck","Slim fit","Long sleeve"]},
                ],
            },
            "dresses": {
                "display_name": "Dresses",
                "products": [
                    {"id": "w-d-1", "name": "Denim Shirt Dress", "sub": "Button-down style", "price": 88, "colors": ["#1B3A5C", "#87CEEB"], "sizes": ["XS","S","M","L"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400", "details": ["Cotton denim","Button front","Belted waist","Knee length"]},
                    {"id": "w-d-2", "name": "Slip Midi Dress", "sub": "Satin elegance", "price": 68, "colors": ["#191919", "#D4C5A9", "#C41230"], "sizes": ["XS","S","M","L"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400", "details": ["Satin fabric","V-neck","Midi length","Adjustable straps"]},
                    {"id": "w-d-3", "name": "T-Shirt Dress", "sub": "Casual comfort", "price": 42, "colors": ["#191919", "#FFFFFF", "#808080"], "sizes": ["XS","S","M","L","XL"], "img": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400", "details": ["Cotton jersey","Crew neck","Above knee","Relaxed fit"]},
                    {"id": "w-d-4", "name": "Wrap Midi Dress", "sub": "Flattering fit", "price": 78, "colors": ["#C41230", "#0A1628"], "sizes": ["XS","S","M","L"], "badge": "New", "img": "https://images.unsplash.com/photo-1571908598047-1927ab498058?w=400", "details": ["Rayon blend","True wrap","Midi length","Flutter sleeve"]},
                    {"id": "w-d-5", "name": "Dungaree Dress", "sub": "Playful denim", "price": 72, "colors": ["#1B3A5C"], "sizes": ["XS","S","M","L"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1582418702059-97ebafb35d09?w=400", "details": ["Cotton denim","Overall style","Adjustable straps","Above knee"]},
                    {"id": "w-d-6", "name": "Maxi Boho Dress", "sub": "Free spirit", "price": 92, "colors": ["#D4C5A9", "#FFFFFF"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1508424757105-b6d5ad9329d0?w=400", "details": ["Lightweight cotton","Floor length","Tiered skirt","Boho print"]},
                    {"id": "w-d-7", "name": "Blazer Mini Dress", "sub": "Power dressing", "price": 108, "colors": ["#191919", "#D4C5A9"], "sizes": ["XS","S","M","L"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "details": ["Stretch blend","Double-breasted","Mini length","Padded shoulders"]},
                    {"id": "w-d-8", "name": "Sweater Dress", "sub": "Cozy knit", "price": 75, "colors": ["#808080", "#191919", "#D4C5A9"], "sizes": ["XS","S","M","L"], "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400", "details": ["Knit fabric","Crew neck","Above knee","Long sleeve"]},
                    {"id": "w-d-9", "name": "Utility Shirt Dress", "sub": "Pockets galore", "price": 82, "colors": ["#3D5A3D", "#4A3728"], "sizes": ["XS","S","M","L","XL"], "img": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=400", "details": ["Cotton twill","Button front","Multiple pockets","Belted waist"]},
                    {"id": "w-d-10", "name": "Bodycon Mini Dress", "sub": "Night out ready", "price": 58, "colors": ["#191919", "#C41230"], "sizes": ["XS","S","M","L"], "badge": "Limited", "img": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400", "details": ["Stretch jersey","Body-hugging","Mini length","Sleeveless"]},
                ],
            },
        },
    },
    "kids": {
        "name": "Kids",
        "subcategories": {
            "jeans": {
                "display_name": "Jeans",
                "products": [
                    {"id": "k-j-1", "name": "511 Slim Fit Kids", "sub": "Just like dad's", "price": 42, "colors": ["#1B3A5C", "#191919"], "sizes": ["4","6","8","10","12","14"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Cotton stretch","Adjustable waist","Slim fit","Durable denim"]},
                    {"id": "k-j-2", "name": "Pull-On Jeggings", "sub": "Easy on, easy off", "price": 35, "colors": ["#1B3A5C", "#191919", "#808080"], "sizes": ["4","6","8","10","12"], "badge": "New", "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Stretch denim","Elastic waist","Pull-on style","Skinny leg"]},
                    {"id": "k-j-3", "name": "Relaxed Fit Kids Jeans", "sub": "Room to play", "price": 38, "colors": ["#1B3A5C"], "sizes": ["4","6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1503944168849-8bf86875bbd8?w=400", "details": ["100% Cotton","Relaxed fit","Elastic waist","Reinforced knees"]},
                    {"id": "k-j-4", "name": "Carpenter Kids Jeans", "sub": "Mini workwear", "price": 44, "colors": ["#4A3728", "#1B3A5C"], "sizes": ["6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400", "details": ["Durable cotton","Carpenter pockets","Relaxed fit","Reinforced seams"]},
                    {"id": "k-j-5", "name": "Straight Leg Kids Jeans", "sub": "Classic cut", "price": 40, "colors": ["#1B3A5C", "#2C2C2C"], "sizes": ["4","6","8","10","12","14"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Cotton denim","Straight leg","Regular fit","Adjustable waist"]},
                    {"id": "k-j-6", "name": "Jogger Jeans", "sub": "Denim meets comfort", "price": 36, "colors": ["#191919", "#1B3A5C"], "sizes": ["4","6","8","10","12"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Knit denim","Elastic cuffs","Drawstring waist","Soft and stretchy"]},
                    {"id": "k-j-7", "name": "Distressed Kids Jeans", "sub": "Cool and casual", "price": 42, "colors": ["#87CEEB"], "sizes": ["6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400", "details": ["Cotton denim","Distressed details","Slim fit","Adjustable waist"]},
                    {"id": "k-j-8", "name": "Wide Leg Kids Jeans", "sub": "Trendy wide cut", "price": 40, "colors": ["#1B3A5C", "#808080"], "sizes": ["6","8","10","12"], "img": "https://images.unsplash.com/photo-1503944168849-8bf86875bbd8?w=400", "details": ["Cotton blend","Wide leg","High waist","Full length"]},
                    {"id": "k-j-9", "name": "Colored Skinny Jeans", "sub": "Fun colors", "price": 38, "colors": ["#C41230", "#0A1628", "#4A3728"], "sizes": ["4","6","8","10","12"], "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Colored denim","Skinny fit","Elastic waist","Stretch fabric"]},
                    {"id": "k-j-10", "name": "Overalls", "sub": "Classic dungarees", "price": 48, "colors": ["#1B3A5C"], "sizes": ["4","6","8","10","12"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Cotton denim","Adjustable straps","Multiple pockets","Snap buttons"]},
                ],
            },
            "tshirts": {
                "display_name": "T-Shirts",
                "products": [
                    {"id": "k-t-1", "name": "Logo Kids Tee", "sub": "Mini brand fan", "price": 22, "colors": ["#FFFFFF", "#191919", "#C41230"], "sizes": ["4","6","8","10","12","14"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["100% Cotton","Screen-print logo","Crew neck","Regular fit"]},
                    {"id": "k-t-2", "name": "Graphic Dino Tee", "sub": "Dinosaur print", "price": 24, "colors": ["#87CEEB", "#2E8B57"], "sizes": ["4","6","8","10"], "badge": "New", "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Cotton jersey","Fun graphic","Short sleeve","Regular fit"]},
                    {"id": "k-t-3", "name": "Striped Kids Tee", "sub": "Classic stripes", "price": 20, "colors": ["#0A1628", "#C41230"], "sizes": ["4","6","8","10","12"], "img": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400", "details": ["Cotton","Stripe pattern","Crew neck","Regular fit"]},
                    {"id": "k-t-4", "name": "Tie-Dye Kids Tee", "sub": "Colorful swirls", "price": 26, "colors": ["#C41230", "#87CEEB"], "sizes": ["4","6","8","10","12"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1503944168849-8bf86875bbd8?w=400", "details": ["Cotton","Tie-dye pattern","Crew neck","Unique wash"]},
                    {"id": "k-t-5", "name": "Pocket Tee Kids", "sub": "Simple and cool", "price": 20, "colors": ["#FFFFFF", "#808080", "#0A1628"], "sizes": ["4","6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Cotton jersey","Chest pocket","Crew neck","Regular fit"]},
                    {"id": "k-t-6", "name": "Long Sleeve Henley", "sub": "Button detail", "price": 28, "colors": ["#808080", "#0A1628"], "sizes": ["4","6","8","10","12"], "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Cotton waffle","3-button placket","Long sleeve","Regular fit"]},
                    {"id": "k-t-7", "name": "Space Print Tee", "sub": "Galaxy design", "price": 24, "colors": ["#0A1628", "#191919"], "sizes": ["4","6","8","10"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400", "details": ["Cotton jersey","Space graphic","Glow in dark","Short sleeve"]},
                    {"id": "k-t-8", "name": "Raglan Baseball Tee", "sub": "Two-tone sleeves", "price": 22, "colors": ["#FFFFFF", "#C41230"], "sizes": ["4","6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1503944168849-8bf86875bbd8?w=400", "details": ["Cotton blend","Raglan sleeves","Crew neck","3/4 length"]},
                    {"id": "k-t-9", "name": "Animal Print Tee", "sub": "Safari fun", "price": 22, "colors": ["#2E8B57", "#4A3728"], "sizes": ["4","6","8","10"], "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Cotton","Animal graphic","Short sleeve","Regular fit"]},
                    {"id": "k-t-10", "name": "Plain Essential Tee", "sub": "Wardrobe basics", "price": 18, "colors": ["#FFFFFF", "#191919", "#808080", "#0A1628"], "sizes": ["4","6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["100% Cotton","Crew neck","Pre-shrunk","Everyday wear"]},
                ],
            },
            "jackets": {
                "display_name": "Jackets",
                "products": [
                    {"id": "k-k-1", "name": "Kids Trucker Jacket", "sub": "Denim classic", "price": 58, "colors": ["#1B3A5C", "#87CEEB"], "sizes": ["4","6","8","10","12","14"], "badge": "Bestseller", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Cotton denim","Button front","Chest pockets","Classic fit"]},
                    {"id": "k-k-2", "name": "Puffer Jacket Kids", "sub": "Warm and cozy", "price": 68, "colors": ["#C41230", "#0A1628", "#191919"], "sizes": ["4","6","8","10","12"], "badge": "New", "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Nylon shell","Synthetic fill","Zip front","Hood"]},
                    {"id": "k-k-3", "name": "Sherpa Lined Kids Jacket", "sub": "Extra warmth", "price": 72, "colors": ["#1B3A5C"], "sizes": ["4","6","8","10","12"], "img": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400", "details": ["Denim exterior","Sherpa lining","Button front","Warm and cozy"]},
                    {"id": "k-k-4", "name": "Rain Jacket Kids", "sub": "Splash ready", "price": 48, "colors": ["#FFD700", "#C41230", "#0A1628"], "sizes": ["4","6","8","10","12"], "badge": "Trending", "img": "https://images.unsplash.com/photo-1503944168849-8bf86875bbd8?w=400", "details": ["Waterproof nylon","Zip front","Hood","Reflective details"]},
                    {"id": "k-k-5", "name": "Bomber Jacket Kids", "sub": "Cool street style", "price": 62, "colors": ["#191919", "#0A1628"], "sizes": ["6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Nylon shell","Ribbed cuffs","Zip front","Lightweight"]},
                    {"id": "k-k-6", "name": "Fleece Zip-Up", "sub": "Soft and warm", "price": 42, "colors": ["#808080", "#0A1628", "#C41230"], "sizes": ["4","6","8","10","12"], "badge": "Icon", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Polar fleece","Full zip","Stand collar","Side pockets"]},
                    {"id": "k-k-7", "name": "Varsity Jacket Kids", "sub": "School spirit", "price": 65, "colors": ["#0A1628", "#C41230"], "sizes": ["6","8","10","12","14"], "img": "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400", "details": ["Wool blend body","Faux leather sleeves","Snap front","Ribbed trim"]},
                    {"id": "k-k-8", "name": "Corduroy Jacket Kids", "sub": "Textured style", "price": 55, "colors": ["#4A3728", "#D4C5A9"], "sizes": ["4","6","8","10","12"], "img": "https://images.unsplash.com/photo-1503944168849-8bf86875bbd8?w=400", "details": ["Cotton corduroy","Button front","Chest pockets","Regular fit"]},
                    {"id": "k-k-9", "name": "Denim Vest Kids", "sub": "Sleeveless cool", "price": 38, "colors": ["#1B3A5C"], "sizes": ["4","6","8","10","12"], "img": "https://images.unsplash.com/photo-1543854589-fdd4d3a0d181?w=400", "details": ["Cotton denim","Button front","Chest pockets","Classic fit"]},
                    {"id": "k-k-10", "name": "Hoodie Jacket Kids", "sub": "Casual zip-up", "price": 45, "colors": ["#808080", "#191919", "#0A1628"], "sizes": ["4","6","8","10","12","14"], "badge": "Premium", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400", "details": ["Cotton blend","Full zip","Drawstring hood","Kangaroo pocket"]},
                ],
            },
        },
    },
}


async def seed_database():
    """Seed all products from the catalog."""
    from sqlalchemy import select as sa_select

    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(sa_select(Product).limit(1))
        if result.scalar_one_or_none():
            print("Database already seeded, skipping.")
            return

        print("Seeding product database...")
        for cat_slug, cat_data in CATALOG.items():
            category = Category(name=cat_data["name"], slug=cat_slug)
            session.add(category)
            await session.flush()

            for sub_slug, sub_data in cat_data["subcategories"].items():
                subcategory = Subcategory(
                    category_id=category.id,
                    name=sub_slug,
                    slug=sub_slug,
                    display_name=sub_data["display_name"],
                )
                session.add(subcategory)
                await session.flush()

                for p in sub_data["products"]:
                    product = Product(
                        id=p["id"],
                        subcategory_id=subcategory.id,
                        name=p["name"],
                        subtitle=p.get("sub", ""),
                        price=p["price"],
                        original_price=p.get("originalPrice"),
                        image_url=p.get("img", ""),
                        colors=p.get("colors", []),
                        sizes=p.get("sizes", []),
                        badge=p.get("badge"),
                        details=p.get("details", []),
                    )
                    session.add(product)

        await session.commit()
        print("Seeded 110 products successfully!")
