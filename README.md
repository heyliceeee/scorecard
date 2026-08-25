# **📘 Sustainability & Circularity Scorecard**

## **Overview**
This project is a Flask‑based web application that generates a **Sustainability & Circularity Scorecard** for any product scanned from the **OpenFoodFacts** database.  
It evaluates packaging materials, environmental impact, and circularity indicators using both OpenFoodFacts data and a custom **Circularity API**.

The result is displayed in a pastel‑styled dashboard showing:

- EcoScore  
- Packaging environmental score  
- Packaging materials  
- Circularity indicators (recyclability, circularity index, recovery rate, etc.)  
- Product image, brand, and quantity  

---

## **Features**
### **Main Application**
- Fetches product data from OpenFoodFacts using a barcode.
- Caches product JSON locally to avoid repeated API calls.
- Extracts packaging information and environmental scores.
- Requests circularity metrics from a local API.
- Renders a clean, anime‑inspired sustainability dashboard.

### **Circularity API**
A lightweight Flask API that provides circularity metrics for common packaging materials such as PET, PP, and HDPE.

It returns:
- Recyclability percentage  
- Circularity index  
- Recovery rate  
- Carbon footprint  
- Recycling energy  
- Reuse feasibility  

---

## **How It Works**

### **1. Product Fetching**
When a barcode is submitted:

1. The app checks if a cached JSON exists in `/data/<barcode>.json`.
2. If not, it fetches the product from OpenFoodFacts:
   ```
   https://world.openfoodfacts.org/api/v2/product/<barcode>.json
   ```
3. The JSON is saved locally for future use.

### **2. Packaging Extraction**
The app reads:
```
product.ecoscore_data.adjustments.packaging.packagings[]
```
Each packaging component includes:
- material  
- shape  
- environmental score  
- food contact  

### **3. Circularity Integration**
For each material, the app calls:
```
http://localhost:5001/circularity/<material>
```
The material name is normalized (e.g., `"en:pet-1-polyethylene-terephthalate"` → `"pet"`).

### **4. Scorecard Rendering**
The final scorecard includes:
- Product name  
- Brand  
- Image  
- EcoScore  
- Packaging score  
- Circularity metrics per material  
- Quantity  

The UI uses dynamic colors based on environmental scores.

---

## **Running the Project**

### **1. Start the Circularity API**
In one terminal:
```bash
python circularity_api.py
```
Runs at:
```
http://localhost:5001
```

### **2. Start the Main Application**
In another terminal:
```bash
python main.py
```
Runs at:
```
http://localhost:5000
```

### **3. Access the App**
Open:
```
http://localhost:5000
```

Enter a barcode (e.g., **5449000054227**) to generate the scorecard.

---

## **Technologies**
- Python  
- Flask  
- Jinja2  
- Bootstrap 5  
- OpenFoodFacts API  
- Custom Circularity API  
