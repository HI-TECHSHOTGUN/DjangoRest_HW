import stripe


def create_stripe_product(name):
    """Создание продукта"""
    product = stripe.Product.create(name=name)
    return product["id"]


def create_stripe_price(product_id, amount):
    """Создание цена"""
    price = stripe.Price.create(
        product=product_id, unit_amount=amount * 100, currency="rub"
    )
    return price["id"]


def create_stripe_session(price_id):
    """Создание платежной сессии"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session["id"], session["url"]
