# DarkPattern – Web Usage Mining for Clickstream Analysis

DarkPattern is a Flask and MongoDB based Web Usage Mining project that detects suspicious website dark patterns using clickstream analysis and Decision Tree Machine Learning.

The system analyzes user navigation behavior to identify manipulative UI patterns such as:

* Forced Actions
* Confirmation Loops
* Hidden Opt-Outs
* Subscription Traps

## Features

* Clickstream dataset preprocessing
* Decision Tree Machine Learning integration
* Dark pattern detection engine
* MongoDB database storage
* Interactive analytics dashboard
* Session analysis and alerts
* User ID search and filtering
* Charts and clickstream visualization
* Manual event ingestion support
* CSV dataset upload support

## Technologies Used

* Python
* Flask
* MongoDB
* Scikit-learn
* Pandas
* Chart.js
* HTML/CSS/JavaScript

## Project Structure

```bash
darkminingproject/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── db.py
│
├── services/
│   ├── dataset_loader.py
│   ├── detection_engine.py
│   ├── analytics.py
│   └── ml_model.py
│
├── routes/
│   ├── stats_routes.py
│   ├── session_routes.py
│   ├── chart_routes.py
│   ├── alert_routes.py
│   ├── clickstream_routes.py
│   ├── ingest_routes.py
│   └── upload_routes.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
│
└── static/
```

## Machine Learning Model

The project uses a Decision Tree Classifier to classify sessions as suspicious or normal based on clickstream behavior features such as:

* Bounce Rate
* Exit Rate
* Product Related Duration
* Session Length
* Visitor Type

## How to Run

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run MongoDB

Make sure MongoDB is running locally or use MongoDB Atlas.

### 3. Start Flask Server

```bash
python app.py
```

### 4. Open Browser

```bash
http://127.0.0.1:5000
```

## Dashboard Modules

* Overview Dashboard
* Alerts Page
* Sessions Analysis
* Charts Visualization
* Raw Clickstream Monitoring
* Ingest Event Page
* API Reference

## Future Scope

* Real-time website tracking
* SaaS deployment
* Advanced ML algorithms
* Automated dark pattern auditing
* Multi-company dashboard support

## Author

Harshitha Manjunath

## License

This project is developed for academic and educational purposes.
