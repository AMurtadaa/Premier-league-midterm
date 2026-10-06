from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, log_loss, brier_score_loss
from .data import chronological_split


def models():
    return {
        "Random Forest": RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1),
        "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=1)),
        "Gradient Boosting": GradientBoostingClassifier(random_state=1),
    }


def evaluate(model, data, features):
    train, test = chronological_split(data)
    if train.empty or test.empty:
        raise ValueError("Both chronological partitions must contain rows.")
    if train.date.max() >= test.date.min():
        raise AssertionError("Training and test dates overlap.")
    model.fit(train[features], train.target)
    prediction = model.predict(test[features])
    probability = model.predict_proba(test[features])[:, list(model.classes_).index(1)]
    return {
        "train_rows": len(train), "test_rows": len(test),
        "train_last_date": str(train.date.max().date()), "test_first_date": str(test.date.min().date()),
        "excluded_cutoff_day_rows": int(data.date.eq("2022-01-01").sum()),
        "accuracy": accuracy_score(test.target, prediction),
        "win_precision": precision_score(test.target, prediction, zero_division=0),
        "win_recall": recall_score(test.target, prediction, zero_division=0),
        "win_f1": f1_score(test.target, prediction, zero_division=0),
        "macro_f1": f1_score(test.target, prediction, average="macro", zero_division=0),
        "binary_log_loss": log_loss(test.target, probability, labels=[0, 1]),
        "binary_brier": brier_score_loss(test.target, probability),
        "confusion_matrix_actual_rows_predicted_columns": confusion_matrix(test.target, prediction, labels=[0, 1]).tolist(),
        "always_non_win_accuracy": float(test.target.eq(0).mean()),
        "features": features,
    }
