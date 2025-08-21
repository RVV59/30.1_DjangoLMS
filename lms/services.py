import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(course):
    """Создает продукт в Stripe."""
    return stripe.Product.create(name=course.title)

def create_stripe_price(product, amount):
    """Создает цену для продукта в Stripe."""
    return stripe.Price.create(
        product=product.id,
        unit_amount=int(amount * 100),
        currency='rub',
    )

def create_stripe_session(price):
    """Создает сессию для оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/success", # URL для успешной оплаты
        cancel_url="https://127.0.0.1:8000/cancel",   # URL для отмены
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session