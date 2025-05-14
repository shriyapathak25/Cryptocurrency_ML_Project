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
def predict():
    # Get form data and convert to float
    try:
        print(request.form)  # debug what you're actually receiving

        # Get and convert inputs
        moving_avg = float(request.form['moving_average'])
        volatility = float(request.form['volatility'])
        liquidity_ratio = float(request.form['liquidity_ratio'])

        # Create a NumPy array with the inputs
        features = np.array([[moving_avg, volatility, liquidity_ratio]])

        # Predict using the loaded model
        prediction = model.predict(features)[0]

        # Send result to the HTML template
        return render_template('index.html',
                               prediction_text=f"Predicted 24h Liquidity Volume: {prediction:.2f}")
    except Exception as e:
        print("Error:", e)  # helpful for debugging in logs
        return render_template('index.html', prediction_text=" Invalid input. Please enter numbers.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
