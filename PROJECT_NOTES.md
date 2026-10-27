# Project Notes

## Title

Student Performance Prediction System Using Machine Learning

## Abstract

This project predicts the academic performance category of a student using basic input values such as attendance, study hours, previous marks, assignment score, and sleep hours. The system is developed using Django for the web application and a Decision Tree Classifier for the machine learning prediction. The predicted output helps identify whether a student is Excellent, Good, Average, or Needs Improvement.

## Objective

- To build a simple web-based prediction system.
- To use machine learning for student performance classification.
- To store prediction records in a database.
- To provide improvement suggestions based on the predicted category.

## Modules

1. Home Module
2. Prediction Form Module
3. Machine Learning Prediction Module
4. Result and Suggestion Module
5. Admin Dashboard Module
6. Analytics Dashboard Module
7. Model Evaluation Module

## Algorithm

The training script compares:

- Decision Tree Classifier
- Random Forest Classifier
- Logistic Regression
- K-Nearest Neighbors
- Naive Bayes

The best model is selected using accuracy and F1-score, then saved for prediction.

## Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Feature importance

## Future Scope

- Add student login.
- Add a separate student login and student history page.
- Replace the generated training data with a larger real institution dataset.
- Add more advanced graphs and downloadable reports.
- Send improvement suggestions by email.
