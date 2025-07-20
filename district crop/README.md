# Crop Recommendation System

A data-driven web application that provides crop recommendations based on district-specific conditions, soil type, and climate data.

## Features

- District-wise crop recommendations
- Interactive data visualizations
- District comparison functionality
- Search functionality for districts and crops
- User feedback system
- Modern, responsive UI

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd district-crop
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirement.txt
```

## Project Structure

```
district-crop/
├── app.py                 # Main application file
├── data/
│   └── crop_data.csv      # Dataset for crop recommendations
├── model/
│   ├── crop_recommendation.pkl  # Trained model for crop recommendations
│   └── yield_prediction.pkl     # Trained model for yield prediction
├── static/
│   └── images/
│       └── agriculture-bg.jpg   # Background image for the hero section
├── templates/
│   ├── index.html         # Home page template
│   ├── result.html        # Results page template
│   ├── compare.html       # District comparison template
│   └── error.html         # Error page template
└── requirement.txt        # Python package dependencies
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the interface to:
   - Select a district to get crop recommendations
   - Compare multiple districts
   - Search for specific districts or crops
   - View detailed statistics and visualizations

## Features in Detail

### Crop Recommendations
- Select a district to view recommended crops
- Filter by soil type and season
- View detailed information about each crop
- See yield predictions and historical data

### District Comparison
- Compare multiple districts side by side
- View yield comparisons
- Analyze crop diversity across districts

### Search Functionality
- Quick search for districts and crops
- Real-time search results
- Easy navigation to specific recommendations

### Data Visualization
- Interactive charts for yield analysis
- Visual comparison of district performance
- Progress indicators for crop yields

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or feedback, please contact:
- Email: info@croprecommendation.com
- Phone: +1 234 567 890 