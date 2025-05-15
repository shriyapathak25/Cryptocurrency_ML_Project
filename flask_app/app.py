from flask import Flask, request, render_template
import joblib
import os
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "linear_regression_model.pkl")
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Safely convert input values to float
        def clean_input(val):
            return float(val.strip().replace(",", ""))

        # Collect and clean inputs
        moving_avg = clean_input(request.form['moving_average'])
        volatility = clean_input(request.form['volatility'])
        liquidity_ratio = clean_input(request.form['liquidity_ratio'])

        # Prepare input for prediction
        input_data = pd.DataFrame([[moving_avg, volatility, liquidity_ratio]],
                                  columns=['moving_average', 'volatility', 'liquidity_ratio'])

        prediction = model.predict(input_data)[0]

        return render_template('index.html',
                               prediction_text=f"🔮 Predicted 24h Liquidity Volume: {prediction:.2f}")

    except ValueError:
        return render_template('index.html',
                               prediction_text="⚠️ Please enter valid numeric inputs.")
    except Exception as e:
        return render_template('index.html',
                               prediction_text=f"⚠️ Unexpected error: {str(e)}")

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)