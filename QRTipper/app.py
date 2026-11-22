import os
from decimal import Decimal, InvalidOperation

import stripe
from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

# id (used in URLs and Stripe metadata) -> name shown on the page.
# The server only accepts ids from this dict.
RECIPIENTS = {
    "team": "The whole team",
    "alex": "Alex",
    "sam": "Sam",
    "jordan": "Jordan",
}

PRESET_AMOUNTS = [3, 5, 10, 20]  # whole Canadian dollars
MIN_CUSTOM = 2
MAX_CUSTOM = 200
CURRENCY = "cad"
BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "Tip Jar")


def amount_to_cents(form):
    """Return the tip in cents, or None if it isn't a preset or a valid custom amount."""
    choice = (form.get("amount") or "").strip()

    if choice == "other":
        raw = (form.get("custom_amount") or "").strip().replace("$", "").replace(",", ".")
        try:
            value = Decimal(raw)
        except InvalidOperation:
            return None
        if not value.is_finite() or value < MIN_CUSTOM or value > MAX_CUSTOM:
            return None
        if value != value.quantize(Decimal("0.01")):
            return None
        return int(value * 100)

    if choice.isdigit() and int(choice) in PRESET_AMOUNTS:
        return int(choice) * 100

    return None


def base_url():
    configured = os.environ.get("BASE_URL", "").strip().rstrip("/")
    return configured or request.url_root.rstrip("/")


@app.get("/")
def index():
    # /?to=alex preselects a recipient, so you can print one QR code per person.
    preselected = request.args.get("to", "")
    if preselected not in RECIPIENTS:
        preselected = ""
    return render_template(
        "index.html",
        business_name=BUSINESS_NAME,
        recipients=RECIPIENTS,
        presets=PRESET_AMOUNTS,
        preselected=preselected,
        min_custom=MIN_CUSTOM,
        max_custom=MAX_CUSTOM,
        error=request.args.get("error", ""),
    )


@app.post("/checkout")
def checkout():
    recipient_id = request.form.get("recipient", "")
    if recipient_id not in RECIPIENTS:
        return redirect(url_for("index", error="recipient"))

    cents = amount_to_cents(request.form)
    if cents is None:
        return redirect(url_for("index", to=recipient_id, error="amount"))

    recipient_name = RECIPIENTS[recipient_id]
    root = base_url()

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "quantity": 1,
                    "price_data": {
                        "currency": CURRENCY,
                        "unit_amount": cents,
                        "product_data": {"name": f"Tip for {recipient_name}"},
                    },
                }
            ],
            metadata={"recipient_id": recipient_id, "recipient_name": recipient_name},
            payment_intent_data={
                "metadata": {"recipient_id": recipient_id, "recipient_name": recipient_name},
                "description": f"Tip for {recipient_name}",
            },
            success_url=f"{root}/thanks?to={recipient_id}",
            cancel_url=f"{root}/?to={recipient_id}",
        )
    except stripe.StripeError:
        app.logger.exception("Stripe could not create a Checkout session")
        return redirect(url_for("index", to=recipient_id, error="stripe"))

    return redirect(session.url, code=303)


@app.get("/thanks")
def thanks():
    recipient_name = RECIPIENTS.get(request.args.get("to", ""))
    if recipient_name is None:
        abort(404)
    return render_template("thanks.html", business_name=BUSINESS_NAME, recipient_name=recipient_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)