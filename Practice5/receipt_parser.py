import re
import json

def read_receipt(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

# Extract all prices 
def extract_prices(text):
    pattern = r'\n([\d\s]+,\d{2})\nСтоимость'
    matches = re.findall(pattern, text)
    prices = [float(p.replace(" ", "").replace(",", ".")) for p in matches]
    return prices

# Extract names 
def extract_names(text):
    pattern = r'\d+\.\n(.+?)\n[\d\s,]+\s*x\s*[\d\s,]+\n[\d\s]+,\d{2}\nСтоимость'
    matches = re.findall(pattern, text, re.DOTALL)
    return [name.strip() for name in matches]

# Extract total
def extract_total(text):
    match = re.search(r'ИТОГО:\n([\d\s]+,\d{2})', text)
    if match:
        return float(match.group(1).replace(" ", "").replace(",", "."))
    return None

# Extract date & time
def extract_datetime(text):
    match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)
    if match:
        return {"date": match.group(1), "time": match.group(2)}
    return None

# Extract payment method
def extract_payment_method(text):
    if "Банковская карта" in text:
        return "Bank Card"
    elif "Наличные" in text:
        return "Cash"
    return "Unknown"



def parse_receipt(filename):
    text = read_receipt(filename)
    return {
        "names": extract_names(text),
        "prices": extract_prices(text),
        "total": extract_total(text),
        "date_time": extract_datetime(text),
        "payment_method": extract_payment_method(text)
    }

if __name__ == "__main__":
    receipt_data = parse_receipt("raw.txt")
    print("\n--- Parsed Receipt Data ---\n")
    print(json.dumps(receipt_data, indent=4, ensure_ascii=False))