---
name: ml_basics
description: Machine learning basics using scikit-learn (regression, classification, clustering, model evaluation).
allowed-tools:
  - train_regression
  - train_classification
  - train_clustering
  - predict
  - evaluate_model
  - save_model
  - load_model
  - split_data
---

# Machine Learning Basics Skill

This skill enables the agent to perform basic machine learning tasks using scikit-learn.

## Tools

### train_regression
Train a linear regression model.

- `data_file`: Path to CSV file containing training data.
- `target_column`: Name of the target column.
- `feature_columns`: List of feature column names (optional). If not provided, use all columns except target.
- `test_size`: Proportion of data to use for testing (default 0.2).
- `random_state`: Random seed for reproducibility (default 42).
- `output_model_path`: Optional path to save the trained model (as .pkl). If not provided, model is kept in memory.

### train_classification
Train a classification model (logistic regression or decision tree).

- `data_file`: Path to CSV file.
- `target_column`: Name of the target column.
- `feature_columns`: List of feature column names (optional).
- `model_type`: "logistic_regression" or "decision_tree" (default "logistic_regression").
- `test_size`: Proportion for testing (default 0.2).
- `random_state`: Random seed (default 42).
- `output_model_path`: Optional path to save the model.

### train_clustering
Perform K‑Means clustering on numeric data.

- `data_file`: Path to CSV file.
- `feature_columns`: List of feature columns to use (optional, default all numeric columns).
- `n_clusters`: Number of clusters (default 3).
- `random_state`: Random seed (default 42).
- `output_labels_path`: Optional path to save the cluster labels as CSV.

### predict
Make predictions using a trained model.

- `model_file`: Path to saved model (.pkl file).
- `data_file`: Path to CSV file with feature data.
- `output_predictions_path`: Optional path to save predictions as CSV.

### evaluate_model
Evaluate a model's performance.

- `model_file`: Path to saved model (.pkl).
- `data_file`: Path to CSV file with ground truth.
- `target_column`: Name of target column.
- `metric`: Evaluation metric: "mse" (regression), "accuracy" (classification), "silhouette" (clustering). Default depends on task.

### save_model
Save a trained model to disk.

- `model_object`: The model object (passed as reference, not usable in this context). This tool is mainly for internal use; prefer saving via train_* tools.
- `file_path`: Path where to save the model (.pkl).

### load_model
Load a model from disk.

- `file_path`: Path to the .pkl file.
- Returns: Model object (reference).

### split_data
Split a dataset into training and testing sets.

- `data_file`: Path to CSV file.
- `target_column`: Name of target column.
- `test_size`: Proportion for testing (default 0.2).
- `random_state`: Random seed (default 42).
- `output_train_path`: Optional path to save training data CSV.
- `output_test_path`: Optional path to save test data CSV.

## Dependencies

- scikit-learn (must be installed via pip)
- pandas (already installed)
- numpy (already installed)
- joblib (for model serialization, usually included with scikit-learn)
