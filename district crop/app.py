from flask import Flask, render_template, request, jsonify, flash
from flask_caching import Cache
import pandas as pd
import joblib
import os
import logging
from datetime import datetime
import plotly.express as px
import plotly.utils
import json

# Configure logging
logging.basicConfig(
    filename='crop_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Define the relative path to the model file
model_path = os.path.join(os.path.dirname(__file__), 'model', 'crop_recommendation.pkl')

# Load the crop recommendation model
try:
    crop_model = joblib.load(model_path)
    logging.info("Model loaded successfully")
except FileNotFoundError:
    logging.error(f"Error: The model file {model_path} was not found.")
    raise

# Load the data for dropdown and results
try:
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'crop_data.csv'))
    logging.info("Data loaded successfully")
except FileNotFoundError:
    logging.error("Error: The data file was not found.")
    raise

@app.route('/')
def index():
    try:
        # Extract unique districts for selection
        districts = sorted(data['District'].unique())
        soil_types = sorted(data['Soil Type'].unique())
        seasons = sorted(data['Ideal Season'].unique())
        
        # Get statistics for the dashboard
        total_districts = len(districts)
        total_crops = len(data['Crop'].unique())
        avg_yield = data['Yield (tons/acre)'].mean()
        
        return render_template('index.html', 
                             districts=districts,
                             soil_types=soil_types,
                             seasons=seasons,
                             total_districts=total_districts,
                             total_crops=total_crops,
                             avg_yield=round(avg_yield, 2))
    except Exception as e:
        logging.error(f"Error in index route: {str(e)}")
        flash("An error occurred while loading the page. Please try again.", "error")
        return render_template('error.html'), 500

@app.route('/result', methods=['POST'])
def result():
    try:
        district = request.form.get('district')
        if not district:
            flash("Please select a district", "error")
            return render_template('index.html', districts=sorted(data['District'].unique()))

        # Filter data by district
        district_data = data[data['District'] == district]
        
        if district_data.empty:
            flash(f"No data found for district: {district}", "error")
            return render_template('index.html', districts=sorted(data['District'].unique()))

        crops_info = []
        
        # Create visualization data
        yield_data = district_data[['Crop', 'Yield (tons/acre)']].sort_values('Yield (tons/acre)', ascending=False)
        fig = px.bar(yield_data, x='Crop', y='Yield (tons/acre)', 
                    title=f'Crop Yields in {district}')
        yield_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        for _, row in district_data.iterrows():
            try:
                # Prepare input data for prediction
                model_input = pd.DataFrame(
                    [[row['Soil Type'], row['Ideal Season'], 
                      row['Average Temperature (°C)'], row['Average Rainfall (mm)']]],
                    columns=['Soil Type', 'Ideal Season', 'Average Temperature (°C)', 
                            'Average Rainfall (mm)']
                )

                # Preprocess the input (one-hot encoding)
                model_input_encoded = pd.get_dummies(model_input)
                model_input_encoded = model_input_encoded.reindex(
                    columns=crop_model.feature_names_in_, fill_value=0)

                # Predict the crop
                crop_prediction = crop_model.predict(model_input_encoded)[0]

                crops_info.append({
                    "crop": crop_prediction,
                    "soil_type": row['Soil Type'],
                    "ideal_season": row['Ideal Season'],
                    "temperature": row['Average Temperature (°C)'],
                    "rainfall": row['Average Rainfall (mm)'],
                    "yield": row['Yield (tons/acre)']
                })
            except Exception as e:
                logging.error(f"Error processing row for district {district}: {str(e)}")
                continue

        return render_template('result.html', 
                             district=district, 
                             crops_info=crops_info,
                             yield_chart=yield_chart)
    except Exception as e:
        logging.error(f"Error in result route: {str(e)}")
        flash("An error occurred while processing your request. Please try again.", "error")
        return render_template('error.html'), 500

@app.route('/compare', methods=['POST'])
def compare_districts():
    try:
        districts = request.form.getlist('districts[]')
        if len(districts) < 2:
            flash("Please select at least two districts to compare", "error")
            return render_template('index.html', districts=sorted(data['District'].unique()))

        comparison_data = []
        for district in districts:
            district_data = data[data['District'] == district]
            avg_yield = district_data['Yield (tons/acre)'].mean()
            comparison_data.append({
                'district': district,
                'avg_yield': round(avg_yield, 2),
                'total_crops': len(district_data['Crop'].unique())
            })

        return render_template('compare.html', comparison_data=comparison_data)
    except Exception as e:
        logging.error(f"Error in compare_districts route: {str(e)}")
        flash("An error occurred while comparing districts. Please try again.", "error")
        return render_template('error.html'), 500

@app.route('/search')
def search():
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify([])

        # Search in crops and districts
        results = data[
            data['Crop'].str.lower().str.contains(query) |
            data['District'].str.lower().str.contains(query)
        ].head(10)

        return jsonify(results.to_dict('records'))
    except Exception as e:
        logging.error(f"Error in search route: {str(e)}")
        return jsonify([])

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        feedback_data = request.form
        # Here you would typically save the feedback to a database
        logging.info(f"Received feedback: {feedback_data}")
        flash("Thank you for your feedback!", "success")
        return jsonify({"status": "success"})
    except Exception as e:
        logging.error(f"Error in feedback route: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
