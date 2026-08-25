from flask import Flask, render_template, request
import requests
import os
import json

app = Flask(__name__)

DATA_DIR = "data"

def load_or_fetch_product(barcode):
    """
    Se existir um ficheiro JSON com o produto, usa-o.
    Caso contrário, faz a chamada à API e guarda o ficheiro.
    """

    filepath = os.path.join(DATA_DIR, f"{barcode}.json")

    # 1) Se já existe o ficheiro → usar cache
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    # 2) Caso contrário → chamar API
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)
    data = response.json()

    # 3) Guardar JSON para evitar chamadas futuras
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product", methods=["POST"])
def product_redirect():
    barcode = request.form.get("barcode")
    return render_template("loading.html", barcode=barcode)

@app.route("/product/<barcode>")
def product_page(barcode):
    data = load_or_fetch_product(barcode)

    if not data or "product" not in data:
        return render_template("error.html", barcode=barcode)

    product = data["product"]

    # Extrair packagings
    packaging_data = (
        product.get("ecoscore_data", {})
               .get("adjustments", {})
               .get("packaging", {})
    )

    packagings = packaging_data.get("packagings", [])
    packaging_score = packaging_data.get("score", None)

    # Transformar packagings em lista limpa para o frontend
    materials = []
    for p in packagings:
        mat = p.get("material", "")
        circularity = get_circularity(mat)

        materials.append({
            "material": p.get("material", "unknown"),
            "shape": p.get("shape", "unknown"),
            "score": p.get("environmental_score_material_score", None),
            "food_contact": p.get("food_contact", None),
            "circularity": circularity
        })

    # Construir scorecard limpo
    scorecard = {
        "title": product.get("generic_name_en", "Unknown Product"),
        "brand": product.get("brands", "Unknown"),
        "image": product.get("image_url"),

        # EcoScore
        "ecoscore": product.get("ecoscore_grade", "unknown").upper(),

        # Packaging
        "packaging_score": packaging_score,
        "materials": materials,

        # Quantity
        "quantity": product.get("quantity", "Unknown")
    }

    return render_template("product.html", scorecard=scorecard)

def get_circularity(material):
    clean = material.replace("en:", "").split("-")[0]
    url = f"http://localhost:5001/circularity/{clean}"
    try:
        return requests.get(url).json()
    except:
        return None

if __name__ == "__main__":
    app.run(debug=True)