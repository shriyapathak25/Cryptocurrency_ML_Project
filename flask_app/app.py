from flask import Flask, request, render_template
import joblib
import numpy as np
import os
app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), "linear_regression_model.pkl")
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])  # Make sure this decorator exists above the function
def predict():
    try:
        # Retrieve form data and convert to float
        moving_avg = float(request.form['moving_average'])
        volatility = float(request.form['volatility'])
        liquidity_ratio = float(request.form['liquidity_ratio'])

        # Create DataFrame with correct feature names for the model
        features = pd.DataFrame(
            [[moving_avg, volatility, liquidity_ratio]],
            columns=['moving_average', 'volatility', 'liquidity_ratio']
        )

        # Predict using the trained model
        prediction = model.predict(features)[0]

        # Render result in the HTML template
        return render_template(
            'index.html',
            prediction_text=f"Predicted 24h Liquidity Volume: {prediction:.2f}"
        )

    except Exception as e:
        print("Prediction error:", str(e))
        return render_template('index.html', prediction_text="Invalid input. Please enter numbers.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
