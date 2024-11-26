# -*- coding: utf-8 -*-
"""NLP Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WPdh9HKyad8XLU1a5UlS7wupz91h53W6
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from time import time

class SentimentAnalysisExperiment:
    def __init__(self):
        # Initialize different vectorizers
        self.vectorizers = {
            'unigram_tfidf': TfidfVectorizer(ngram_range=(1, 1), max_features=50000),
            'bigram_tfidf': TfidfVectorizer(ngram_range=(2, 2), max_features=50000),
            'unigram_bigram_tfidf': TfidfVectorizer(ngram_range=(1, 2), max_features=50000),
            'unigram_count': CountVectorizer(ngram_range=(1, 1), max_features=50000),
            'bigram_count': CountVectorizer(ngram_range=(2, 2), max_features=50000),
            'unigram_bigram_count': CountVectorizer(ngram_range=(1, 2), max_features=50000)
        }

        # Initialize different models
        self.models = {
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
            'LinearSVM': LinearSVC(random_state=42, max_iter=1000),
            'MultinomialNB': MultinomialNB()
        }

        self.results = []

    def run_experiment(self, train_df, test_df, text_column, label_column):
        """Run experiments with different feature extractors and models"""

        # Store results
        for vectorizer_name, vectorizer in self.vectorizers.items():
            print(f"\nExtracting features using {vectorizer_name}")

            # Transform the text data
            X_train = vectorizer.fit_transform(train_df[text_column])
            X_test = vectorizer.transform(test_df[text_column])

            y_train = train_df[label_column]
            y_test = test_df[label_column]

            # Try each model
            for model_name, model in self.models.items():
                print(f"Training {model_name}...")

                # Train and predict
                start_time = time()
                model.fit(X_train, y_train)
                train_time = time() - start_time

                start_time = time()
                y_pred = model.predict(X_test)
                predict_time = time() - start_time

                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                report = classification_report(y_test, y_pred)

                # Store results
                result = {
                    'Vectorizer': vectorizer_name,
                    'Model': model_name,
                    'Accuracy': accuracy,
                    'Training Time': train_time,
                    'Prediction Time': predict_time,
                    'Classification Report': report
                }
                self.results.append(result)

                print(f"Accuracy: {accuracy:.4f}")
                print(f"Training time: {train_time:.2f} seconds")
                print(f"Prediction time: {predict_time:.2f} seconds")
                print("\nClassification Report:")
                print(report)
                print("-" * 80)

    def get_best_model(self):
        """Return the best performing model based on accuracy"""
        best_result = max(self.results, key=lambda x: x['Accuracy'])
        return best_result

    def save_results(self, filepath):
        """Save results to CSV"""
        results_df = pd.DataFrame(self.results)
        results_df.to_csv(filepath, index=False)
        print(f"Results saved to {filepath}")

# Read the datasets
train_df = pd.read_csv('Train.csv')
test_df = pd.read_csv('Test.csv')

train_df.head()

# Initialize and run experiments
experiment = SentimentAnalysisExperiment()
experiment.run_experiment(
    train_df=train_df,
    test_df=test_df,
    text_column='Data',  # replace with your text column name
    label_column='Label'  # replace with your label column name
)



experiment.save_results('sentiment_analysis_results.csv')