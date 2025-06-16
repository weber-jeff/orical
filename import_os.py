import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import json
import random
import datetime

try:
    from astro_numerology_engine import load_user_feedback, USER_DATA_FILE, MODEL_FILE
except ImportError as e:
    print(f"Warning: Could not import from astro_numerology_engine: {e}. Using placeholders.")
    USER_DATA_FILE = "daily_user_feedback.json"
    MODEL_FILE = "trained_astro_numerology_model.joblib"
    def load_user_feedback():
        print("Warning: Using placeholder load_user_feedback().")
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r') as f:
                    content = f.read()
                    if not content: return []
                    return json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {USER_DATA_FILE} contains malformed JSON.")
                return []
            except Exception as ex:
                print(f"Error loading placeholder data: {ex}")
                return []
        return []

def get_numerological_insights(birth_month, birth_day, target_date_obj):
        return {"personal_day": 5, "personal_month": 1, "personal_year": 7}  # default mock

try:
    from backend.services.numerology_core.birthday  import parse_birthdate
except ImportError as e:
    print(f"Warning: Could not import get_numerological_insights: {e}. Using fallback.")   

def load_and_preprocess_data(json_file_path=USER_DATA_FILE):
    raw_data = load_user_feedback()
    if not raw_data:
        print("No raw data loaded from feedback. Cannot preprocess.")
        return None, None, None

    processed_data = []
    for entry in raw_data:
        astro = entry.get('astrology_snapshot', {}) or {}
        num = entry.get('numerology_snapshot', {}) or {}
        pd_val = str(num.get('personal_day', '0')).split(' ')[0]
        flat = {
            'personal_year': num.get('personal_year'),
            'personal_month': num.get('personal_month'),
            'personal_day': pd_val,
            'transiting_moon_sign': astro.get('transiting_moon_sign'),
            'mercury_retrograde': int(astro.get('mercury_retrograde', 0)),
            'dominant_element_today': astro.get('dominant_element_today'),
            'dominant_modality_today': astro.get('dominant_modality_today'),
            'harmonious_transit_count': astro.get('harmonious_transit_count'),
            'challenging_transit_count': astro.get('challenging_transit_count'),
            'key_transit_category': astro.get('key_transit_category'),
            'user_activity_category': entry.get('user_activity_category', entry.get('user_activity', 'Unknown')),
            'outcome_rating': entry.get('outcome_rating')
        }
        if flat['outcome_rating'] is not None:
            processed_data.append(flat)

    df = pd.DataFrame(processed_data)
    y = df['outcome_rating']
    X = df.drop('outcome_rating', axis=1)

    num_features = [
        'personal_year', 'personal_month', 'personal_day',
        'mercury_retrograde', 'harmonious_transit_count', 'challenging_transit_count']
    cat_features = [
        'transiting_moon_sign', 'dominant_element_today',
        'dominant_modality_today', 'key_transit_category',
        'user_activity_category']

    num_features = [f for f in num_features if f in X.columns]
    cat_features = [f for f in cat_features if f in X.columns]

    for col in num_features:
        X[col] = pd.to_numeric(X[col], errors='coerce')

    num_pipe = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    cat_pipe = Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
                         ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

    transformers = []
    if num_features: transformers.append(('num', num_pipe, num_features))
    if cat_features: transformers.append(('cat', cat_pipe, cat_features))

    if not transformers:
        print("No transformers to apply.")
        return X, y, None

    preprocessor = ColumnTransformer(transformers=transformers)
    return X, y, preprocessor

def train_outcome_model():
    X, y, preprocessor = load_and_preprocess_data()
    if X is None or y is None or preprocessor is None or X.empty or y.empty:
        print("Training aborted: invalid data or preprocessor.")
        return False
    if y.nunique() < 2:
        print(f"Training aborted: only one class '{y.unique()[0]}' present.")
        return False

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
    ])

    try:
        print("Training model...")
        pipeline.fit(X_train, y_train)
        print("Model trained.")
        y_pred = pipeline.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))
        joblib.dump(pipeline, MODEL_FILE)
        print(f"Model saved to {MODEL_FILE}")
        return True
    except Exception as e:
        print(f"Error during training: {e}")
        return False

def predict_outcome(numerology, astrology, activity):
    if not os.path.exists(MODEL_FILE):
        return "Model not available.", None

    try:
        model = joblib.load(MODEL_FILE)
        pd_val = str(numerology.get('personal_day', '0')).split(' ')[0]
        input_dict = {
            'personal_year': [numerology.get('personal_year')],
            'personal_month': [numerology.get('personal_month')],
            'personal_day': [pd_val],
            'transiting_moon_sign': [astrology.get('transiting_moon_sign')],
            'mercury_retrograde': [int(astrology.get('mercury_retrograde', 0))],
            'dominant_element_today': [astrology.get('dominant_element_today')],
            'dominant_modality_today': [astrology.get('dominant_modality_today')],
            'harmonious_transit_count': [astrology.get('harmonious_transit_count')],
            'challenging_transit_count': [astrology.get('challenging_transit_count')],
            'key_transit_category': [astrology.get('key_transit_category')],
            'user_activity_category': [activity]
        }
        df = pd.DataFrame.from_dict(input_dict)
        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0]
        labels = model.named_steps['classifier'].classes_
        proba_map = {str(lbl): proba[i] for i, lbl in enumerate(labels)}
        return prediction, proba_map
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error during prediction.", None

def generate_synthetic_entry(date):
    moon_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    elements = ["Fire", "Earth", "Air", "Water"]
    modalities = ["Cardinal", "Fixed", "Mutable"]
    keys = ["Dynamic", "Stable", "Growth", "Challenge", "Social", "Emotional", "Detailed", "Creative"]
    acts = ["Work", "Personal", "Social", "Creative", "Routine", "Learning"]
    outcomes = ["Positive", "Neutral", "Negative"]

    month = random.randint(1, 12)
    day = random.randint(1, 28)
    num = get_numerological_insights(month, day, date)
    astro = {
        "transiting_moon_sign": random.choice(moon_signs),
        "mercury_retrograde": random.choice([True, False]),
        "dominant_element_today": random.choice(elements),
        "dominant_modality_today": random.choice(modalities),
        "harmonious_transit_count": random.randint(0, 5),
        "challenging_transit_count": random.randint(0, 3),
        "key_transit_category": random.choice(keys)
    }
    score = astro['harmonious_transit_count'] - astro['challenging_transit_count'] - (2 if astro['mercury_retrograde'] else 0)
    weights = [0.6, 0.3, 0.1] if score > 1 else [0.1, 0.3, 0.6] if score < -1 else [0.3, 0.4, 0.3]
    outcome = random.choices(outcomes, weights=weights)[0]
    act = random.choice(acts)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "numerology_snapshot": {
            "personal_year": num.get('personal_year'),
            "personal_month": num.get('personal_month'),
            "personal_day": str(num.get('personal_day')).split(' ')[0]
        },
        "astrology_snapshot": astro,
        "user_activity_category": act,
        "user_activity": f"{act} task",
        "outcome_rating": outcome,
        "notes": "Synthetic feedback entry."
    }

if __name__ == '__main__':
    print("Testing ML pipeline...")

    needs_data = not os.path.exists(USER_DATA_FILE)
    if not needs_data:
        try:
            with open(USER_DATA_FILE, 'r') as f:
                data = json.load(f)
                needs_data = len(data) < 10
        except Exception as e:
            print(f"Error loading data: {e}")
            needs_data = True

    if needs_data:
        print("Generating synthetic data...")
        start = datetime.date(2023, 1, 1)
        synthetic = [generate_synthetic_entry(start + datetime.timedelta(days=i)) for i in range(100)]
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(synthetic, f, indent=4)
        print("Synthetic data saved.")

    if train_outcome_model():
        print("\nTesting prediction:")
        result, probs = predict_outcome(
            {"personal_year": "7", "personal_month": "1", "personal_day": "5 (Focus)"},
            {
                "transiting_moon_sign": "Aries",
                "mercury_retrograde": False,
                "dominant_element_today": "Fire",
                "dominant_modality_today": "Cardinal",
                "harmonious_transit_count": 2,
                "challenging_transit_count": 1,
                "key_transit_category": "Dynamic"
            },
            "Work"
        )
        print(f"Predicted: {result}\nProbabilities: {json.dumps(probs, indent=2)}")
    else:
        print("Model training failed. Skipping prediction.")

    print("Test complete.")
