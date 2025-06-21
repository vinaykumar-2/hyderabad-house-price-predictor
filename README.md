# 🏠 Hyderabad House Price Estimator

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
  - 1 BHK minimum = ₹8,000/sqft  
  - 2 BHK minimum = ₹10,000/sqft  
  - 3+ BHK minimum = ₹12,000/sqft  

This makes sure the prices stay realistic and not undervalued for luxury areas.

---

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