import streamlit as st
import numpy as np
import pickle 

#Load model and training columns
with open("model.pkl",'rb') as f:
    model = pickle.load(f)

with open("columns.pkl",'rb') as f:
    model_columns = pickle.load(f)


#Extract dropdown values from the encoded columns
def extract_options(prefix):
    return sorted({col.replace(prefix,"") for col in model_columns if col.startswith(prefix)})

localities = extract_options('locality_')
property_types = extract_options('property_type_')
furnished_statuses = extract_options("furnished_status_")
user_types = extract_options("user_type_")

#Streamlit UI

st.set_page_config(page_title="🏠 Hyderabad House Price Estimator", layout="centered")
st.title("🏠 Hyderabad House Price Estimator")
st.markdown("🔍 Fill in the details below to get an estimated house price.")
st.markdown("---")

#Tier A premium localities
premium_areas = [
    "Kokapet", "Banjara Hills", "Jubilee Hills", "Gachibowli", "Kondapur",
    "Madhapur", "HiTech City", "Financial District"
]

#UI for input
with st.form("input_form"):
    st.markdown("### 🧾 Property Details")
    col1,col2,col3 = st.columns(3)
    with col1:
        area_sqft = st.text_input("📐 Total Square Feet", placeholder="e.g., 1500")
    with col2:
        bhk = st.selectbox("🛏 Bedrooms (BHK)", [1, 2, 3, 4, 5])
    with col3:
        brand_new = st.selectbox("🏗 Brand New Property", ["No", "Yes"])

    col4,col5 = st.columns(2)
    with col4:
        locality = st.selectbox("📍 Locality", localities)
    with col5:
        property_type = st.selectbox("🏢 Property Type", property_types)
    
    col6,col7 = st.columns(2)
    with col6:
        furnished_status = st.selectbox("🛋 Furnished Status", furnished_statuses)
    with col7:
        user_type = st.selectbox("👤 Listed By", user_types)
    
    submit = st.form_submit_button("🔮 Predict Price")

#Prepare input for prediction
def prepare_input(area_sqft,bhk,brand_new,locality,property_type,furnished_status,user_type):
    input_dict ={
        "area_sqft":float(area_sqft),
        "bhk":int(bhk),
        "brand_new": 1 if brand_new == "Yes" else 0,
        "room_density": float(area_sqft) / (int(bhk) + 1),
        "bhk_to_area": float(area_sqft) / (int(bhk) + 1),
        "is_luxury_flat": int(int(bhk) >= 4 and float(area_sqft) >= 1800),
        "is_compact_flat": int(float(area_sqft) <= 800),
        f"locality_{locality}": 1,
        f"property_type_{property_type}": 1,
        f"furnished_status_{furnished_status}": 1,
        f"user_type_{user_type}": 1
    }
    return [input_dict.get(col,0) for col in model_columns]


#Make prediction when user submits the form
if submit:
    try:
        #Validate square feet input
        if not area_sqft.strip():
            st.warning("⚠️ Please enter the square footage.")
            st.stop()
        elif not area_sqft.strip().replace('.','',1).isdigit():
            st.warning("⚠️ Square footage must be a number.")
            st.stop()
        elif float(area_sqft) < 200:
            st.warning("⚠️ Please enter at least 200 sqft — values below this are unrealistic.")
            st.stop()

        else:
            #Convert sqft to float
            area_val = float(area_sqft)
            #warn if small but valid
            if area_val < 400:
                st.warning("⚠️ Note: Small house sizes may show high price per sqft due to low area.")

            input_data= np.array([prepare_input(
                area_sqft,bhk,brand_new,locality,property_type,
                furnished_status,user_type)
            ])

            prediction = model.predict(input_data)[0]
            predicted_pps = prediction/area_val

            # Adjust if Tier A and price per sqft is unrealistically low
            price_adjusted = False
            
            if locality in premium_areas and predicted_pps < 12000:
                if bhk == 1:
                    prediction = area_val * 15000
                    predicted_pps = 15000
                elif bhk == 2:
                    prediction = area_val * 18000
                    predicted_pps = 18000
                else:
                    prediction = area_val * 20000
                    predicted_pps = 20000

                price_adjusted = True

            price = max(0,round(prediction))
            st.success(f"💰 Estimated Price: ₹ {price:,.0f}")
            st.info(f"📏 Estimated Price/Sqft: ₹ {predicted_pps:,.0f}")

            if price_adjusted:
                st.warning("⚠️ Prediction was adjusted to reflect premium locality pricing.")
    
    except ValueError:
        st.warning("⚠️ Please enter the square footage.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
