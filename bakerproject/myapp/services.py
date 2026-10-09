import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)

def create_order(amount, receipt):
    return client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "receipt": str(receipt),
    })


def verify_payment(order_id, payment_id, signature, expected_amount):
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })

        payment = client.payment.fetch(payment_id)

        return (
            payment.get("order_id") == order_id
            and int(payment.get("amount", 0)) == int(expected_amount * 100)
            and payment.get("currency") == "INR"
            and payment.get("status") == "captured"
        )

    except (
        razorpay.errors.SignatureVerificationError,
        razorpay.errors.RazorpayError,
        ValueError,
        TypeError,
    ):
        return False