import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("dataset.csv")

# ==========================================
# 2. SELECT FEATURES
# ==========================================

features = [
    "attendance",
    "internal_marks",
    "assignment_marks",
    "study_hours",
    "previous_score"
]

X = data[features]
y = data["final_score"]

# ==========================================
# 3. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# 4. CREATE RANDOM FOREST MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# ==========================================
# 5. TRAIN MODEL
# ==========================================

model.fit(X_train, y_train)

# ==========================================
# 6. TEST MODEL
# ==========================================

test_predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    test_predictions
)

print("Model trained successfully!")
print("Mean Absolute Error:", round(mae, 2))


# ==========================================
# 7. PREDICTION FUNCTION
# ==========================================

def predict_score(
    attendance,
    internal_marks,
    assignment_marks,
    study_hours,
    previous_score
):

    student = pd.DataFrame([{
        "attendance": attendance,
        "internal_marks": internal_marks,
        "assignment_marks": assignment_marks,
        "study_hours": study_hours,
        "previous_score": previous_score
    }])

    prediction = model.predict(student)[0]

    # Keep prediction between 0 and 100
    prediction = max(0, min(100, prediction))

    return round(prediction, 1)


# ==========================================
# 8. RISK LEVEL
# ==========================================

def get_risk(score):

    if score >= 75:
        return "LOW"

    elif score >= 60:
        return "MEDIUM"

    else:
        return "HIGH"


# ==========================================
# 9. RECOMMENDATIONS
# ==========================================

def get_recommendations(
    attendance,
    internal_marks,
    assignment_marks,
    study_hours,
    previous_score
):

    recommendations = []

    if attendance < 75:
        recommendations.append(
            "Improve attendance to at least 75%."
        )

    elif attendance < 85:
        recommendations.append(
            "Try to maintain attendance above 85%."
        )

    else:
        recommendations.append(
            "Good attendance. Keep maintaining it."
        )

    if internal_marks < 60:
        recommendations.append(
            "Focus more on internal exam preparation."
        )

    elif internal_marks < 75:
        recommendations.append(
            "Improve internal marks through regular revision."
        )

    else:
        recommendations.append(
            "Your internal marks are good. Keep practicing."
        )

    if assignment_marks < 60:
        recommendations.append(
            "Complete assignments regularly."
        )

    if study_hours < 2:
        recommendations.append(
            "Increase daily study time to at least 2-3 hours."
        )

    elif study_hours < 3:
        recommendations.append(
            "Try increasing study time to around 3 hours per day."
        )

    else:
        recommendations.append(
            "Good study routine. Maintain consistency."
        )

    if previous_score < 60:
        recommendations.append(
            "Focus on improving your weak subjects."
        )

    return recommendations


# ==========================================
# 10. TEST THE MODEL
# ==========================================

if __name__ == "__main__":

    print("\n-----------------------------")
    print("AI STUDENT PERFORMANCE TEST")
    print("-----------------------------")

    score = predict_score(
        attendance=72,
        internal_marks=68,
        assignment_marks=75,
        study_hours=2,
        previous_score=70
    )

    risk = get_risk(score)

    recommendations = get_recommendations(
        attendance=72,
        internal_marks=68,
        assignment_marks=75,
        study_hours=2,
        previous_score=70
    )

    print("Predicted Score:", score)
    print("Risk Level:", risk)

    print("\nRecommendations:")

    for recommendation in recommendations:
        print("-", recommendation)
