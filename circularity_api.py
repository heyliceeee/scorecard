from flask import Flask, jsonify
import json

app = Flask(__name__)

with open("data/circularity_data.json", "r") as f:
    CIRCULARITY = json.load(f)

@app.route("/circularity/<material>")
def get_material(material):
    material = material.lower()
    return jsonify(CIRCULARITY.get(material, {}))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
