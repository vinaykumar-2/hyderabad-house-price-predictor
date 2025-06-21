# 🏠 Hyderabad House Price Estimator


[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hyderabad-house-price-predictor-bmradqhawgfhttieabpsf3.streamlit.app/)  


This is a machine learning web app that predicts house prices in Hyderabad based on user inputs like area, number of bedrooms (BHK), locality, property type, and more.

---

## 📌 Key Features

- Predicts house prices using a trained Random Forest model
- Built with Python and Streamlit
- **Adjusts price predictions in premium localities if they are too low**
- User-friendly form to input property details

---

## 💡 Important Model Logic

To make predictions more realistic, especially in **premium areas like Banjara Hills, Jubilee Hills, Kokapet**, etc.:

- If the model predicts **very low price per square foot**, a **correction is applied** based on BHK
- Example:
  - 1 BHK minimum = ₹15,000/sqft  
  - 2 BHK minimum = ₹18,000/sqft  
  - 3+ BHK minimum = ₹20,000/sqft  

This makes sure the prices stay realistic and not undervalued for luxury areas.

---

📈 Example Output  
💰 Estimated Price: ₹ 24,00,000  
📏 Price per Sqft: ₹ 12,000  
⚠️ Prediction adjusted due to premium locality  

## 🛠 Tech Stack

- Python
- scikit-learn (Random Forest)
- Streamlit (for web UI)
- Pandas & NumPy
- Pickle (for saving model and columns)

---

## 🚀 How to Run

1. Install required libraries:
   ```bash
   pip install streamlit scikit-learn pandas numpy
2. streamlit run app.py  

🌐 Live App
Click below to try the app online (no installation needed):
🔗 Open App in Streamlit →  