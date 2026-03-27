"""
Real API Use Case #2
Currency Converter CLI (Beginner Friendly)

API used:
- https://open.er-api.com
"""

import requests


def fetch_supported_currencies() -> dict:
    # ye endpoint base currency ki tamam rates deta hai (codes yahan se mil jate hain).
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    rates = data.get("rates", {})

    # same interface rakhne ke liye code->code dict return kar rahe hain.
    currencies = {code: code for code in rates.keys()}
    currencies["USD"] = "USD"
    return currencies


def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
    # open.er-api per "latest/<base>" se target rates milti hain.
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(f"API conversion failed: {data.get('error-type', 'unknown')}")

    rates = data.get("rates", {})
    if to_currency not in rates:
        raise ValueError(f"Target currency '{to_currency}' not found in API rates.")

    # rates me 1 FROM = X TO hota hai, to amount multiply karte hain.
    return amount * float(rates[to_currency])


def main() -> None:
    print("Currency Converter CLI")
    print("-" * 30)

    try:
        currencies = fetch_supported_currencies()
    except requests.exceptions.RequestException as err:
        print("Currencies load nahi ho sakin:", err)
        return

    print("Example supported codes: USD, EUR, GBP, PKR, INR, AED")
    print("Total currencies available:", len(currencies))

    from_currency = input("From currency code (e.g. USD): ").strip().upper()
    to_currency = input("To currency code (e.g. PKR): ").strip().upper()
    amount_text = input("Amount (e.g. 100): ").strip()

    if from_currency not in currencies:
        print("Invalid 'from' currency code.")
        return
    if to_currency not in currencies:
        print("Invalid 'to' currency code.")
        return

    try:
        # ye text input ko number me convert kar raha hai.
        amount = float(amount_text)
    except ValueError:
        print("Amount number hona chahiye.")
        return

    if amount <= 0:
        print("Amount positive hona chahiye.")
        return

    try:
        converted = convert_amount(amount, from_currency, to_currency)
    except ValueError as err:
        print("Data/API error:", err)
        return
    except requests.exceptions.HTTPError as err:
        print("API HTTP error:", err)
        return
    except requests.exceptions.Timeout:
        print("Request timeout - phir try karo.")
        return
    except requests.exceptions.RequestException as err:
        print("Network/request issue:", err)
        return

    print("\nConversion Result")
    print(f"{amount:.2f} {from_currency} = {converted:.2f} {to_currency}")


if __name__ == "__main__":
    main()
