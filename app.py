from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "ilj-secret-key-12345"

PRODUCTS = {
    1: {
        "title": "Футболка Oversize чёрная",
        "price": 2799,
        "image": "shirt01.jpg",
        "category": "Мужское",
        "article": "TS-001",
        "description": "Базовая футболка оверсайз из плотного хлопка премиум-класса (240 г/м²). Мягкая, дышащая ткань с лёгкой фактурой — не деформируется после стирок и сохраняет глубокий чёрный цвет. Свободный крой, аккуратные швы, усиленная горловина. Универсальная вещь на каждый день: отлично сочетается с джинсами, брюками и спортивными штанами.",
        "tags": ["мужское"],
    },
    2: {
        "title": "Джинсы чёрные",
        "price": 3999,
        "image": "jeans01.jpg",
        "category": "Мужское",
        "article": "JN-002",
        "description": "Классические джинсы прямого кроя из плотного итальянского денима (12 oz). Глубокий чёрный цвет с лёгким благородным блеском, матовые металлические пуговицы и фурнитура YKK. Идеальная посадка по фигуре за счёт эластана в составе — не сковывает движения и не растягивается.",
        "tags": ["мужское"],
    },
    3: {
        "title": "Платье чёрное",
        "price": 3499,
        "image": "dress01.jpg",
        "category": "Женское",
        "article": "DR-003",
        "description": "Элегантное платье миди из плотного костюмного трикотажа. Благородная матовость, мягкая посадка по фигуре, аккуратные вытачки и потайная молния. Ткань не просвечивает, не тянется и не образует катышков.",
        "tags": ["женское"],
    },
    4: {
        "title": "Лонгслив чёрный",
        "price": 3199,
        "image": "longsleeve01.jpg",
        "category": "Мужское",
        "article": "LS-004",
        "description": "Лонгслив из мягкого органического хлопка (95%) с добавлением эластана. Плотное полотно сохраняет форму после множества стирок, не скатывается и не теряет насыщенность цвета. Аккуратный крой, длинные рукава с манжетами, минималистичный дизайн без принтов.",
        "tags": ["мужское"],
    },
    5: {
        "title": "Джинсы синие",
        "price": 3999,
        "image": "jeans02.jpg",
        "category": "Мужское",
        "article": "JN-005",
        "description": "Джинсы классического синего цвета из плотного хлопкового денима (11 oz) с лёгкой потёртостью. Универсальный прямой крой, крепкие швы, надёжная фурнитура. Ткань с годами становится только мягче, приобретая благородный винтажный вид.",
        "tags": ["мужское", "новинки"],
    },
    6: {
        "title": "Платье фиолетовое",
        "price": 3499,
        "image": "dress02.jpg",
        "category": "Женское",
        "article": "DR-006",
        "description": "Платье насыщенного фиолетового оттенка из премиального вискозного полотна с лёгким сатиновым блеском. Драпируется мягкими волнами, подчёркивает фигуру и не сковывает движения. Дышащий материал комфортен даже в тёплый день.",
        "tags": ["женское", "новинки"],
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/category/<tag>")
def category(tag):
    filtered = {id: p for id, p in PRODUCTS.items() if tag in p.get("tags", [])}
    return render_template("category.html", products=filtered, tag=tag)

@app.route("/product/<int:product_id>")
def product(product_id):
    item = PRODUCTS.get(product_id)
    if not item:
        return "Товар не найден", 404
    return render_template("product.html", product=item, product_id=product_id)

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    if product_id not in PRODUCTS:
        return "Товар не найден", 404
    size = request.args.get("size", "")
    cart = session.get("cart", [])
    cart.append({"id": product_id, "size": size})
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [entry for entry in cart if entry.get("id") != product_id]
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_items = []
    total = 0
    for entry in session.get("cart", []):
        pid = entry.get("id")
        if pid in PRODUCTS:
            item = PRODUCTS[pid].copy()
            item["id"] = pid
            item["size"] = entry.get("size", "")
            cart_items.append(item)
            total += item["price"]
    return render_template("cart.html", items=cart_items, total=total)

@app.route("/checkout")
def checkout():
    session.pop("cart", None)
    return render_template("checkout.html")

if __name__ == "__main__":
    app.run(debug=True)