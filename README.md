# Student Performance Prediction System

A simple industrial training project using Django and Machine Learning. The system predicts a student's performance category from academic and lifestyle inputs.

## Features

- Home page with recent predictions
- Student prediction form
- Performance result page
- Improvement suggestion
- Admin dashboard for saved prediction records
- Analytics dashboard for records and model evaluation
- Teacher login for protected analytics access
- Downloadable PDF report for each prediction result
- CSS-based charts for model accuracy, feature importance, and prediction categories
- Automatic model comparison and best model selection
- Accuracy, precision, recall, F1-score, confusion matrix, and feature importance
- SQLite database

## Technology Used

- Python
- Django
- SQLite
- pandas
- scikit-learn
- joblib
- HTML and CSS

## Project Inputs

- Attendance percentage
- Study hours per day
- Previous marks percentage
- Assignment score percentage
- Sleep hours per day

## Prediction Output

- Excellent
- Good
- Average
- Needs Improvement

## Setup Steps

Open a terminal inside this folder:

```powershell
cd "C:\Users\hp\Documents\training\student_performance_prediction"
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
pip install -r requirements-ml.txt
```

Train the machine learning model:

```powershell
python ml_model\train_model.py
```

This command compares Decision Tree, Random Forest, Logistic Regression,
K-Nearest Neighbors, and Naive Bayes. It saves the best model as:

```text
ml_model/student_performance_model.pkl
```

It also saves model evaluation details as:

```text
ml_model/model_metrics.json
```

Create the database tables:

```powershell
python manage.py migrate
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

Run the Django server:

```powershell
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/
```

Open the analytics dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

## Project Explanation

This project collects student details through a Django form. The data is passed
to the best trained machine learning model selected during training. The model
predicts a performance category, and the system displays the result with a
useful suggestion. Each prediction is saved in the database and can be viewed
from the Django admin panel and analytics dashboard.

If the trained model file is not available, the project uses a simple fallback rule-based prediction so the application can still work during demonstrations.

## Major Project Upgrade Points

- Compares multiple machine learning algorithms instead of using only one.
- Selects the best model based on accuracy and F1-score.
- Uses an expanded 520-record training dataset with balanced performance categories.
- Stores training metrics in a JSON file for dashboard display.
- Shows charts, a confusion matrix, and feature importance for explainability.
- Summarizes saved prediction records with category counts and average input values.
- Protects analytics with teacher login.
- Generates a downloadable PDF report for student prediction results.
