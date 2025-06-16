import os
import joblib # For saving and loading the model
import pandas as pd # For data manipulation
from sklearn.model_selection import train_test_split # For splitting data
from sklearn.ensemble import RandomForestClassifier # The ML algorithm
from sklearn.preprocessing import OneHotEncoder, StandardScaler # For feature scaling and encoding
from sklearn.impute import SimpleImputer # For handling missing values
from sklearn.compose import ColumnTransformer # For applying different transformations to different columns
from sklearn.pipeline import Pipeline # For chaining steps together
from sklearn.metrics import accuracy_score, classification_report # For evaluating the model
import json # For creating dummy data in the test block
import random # For generating random choices
import datetime # For generating dates

# Attempt to import shared constants and functions from astro_numerology_engine
try:
    from astro_numerology_engine import load_user_feedback, USER_DATA_FILE, MODEL_FILE
except ImportError as e:
    print(f"Warning: Could not import from astro_numerology_engine: {e}. Using placeholders.")
    USER_DATA_FILE = "daily_user_feedback.json"
    MODEL_FILE = "trained_astro_numerology_model.joblib"
    def load_user_feedback():
        print("Warning: Using placeholder load_user_feedback().")
        return [] # Simplified placeholder

# Import get_numerological_insights from utils
try:
    MODEL_FILE = "trained_astro_numerology_model.joblib"
    def load_user_feedback():
        print("Warning: Using placeholder load_user_feedback().")
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r') as f:
                    # Handle empty or malformed JSON
                    content = f.read()
                    if not content: return []
                    return json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {USER_DATA_FILE} contains malformed JSON.")
                return []
            except Exception as ex:
                print(f"Error loading placeholder data: {ex}")
                return []
except ImportError as e:
    print(f"Warning: Could not import get_numerological_insights from numerology.meanings.utils: {e}. Synthetic data generation may be limited.")
    # Define a placeholder if import fails
    def get_numerological_insights(birth_month, birth_day, target_date_obj):
        return {"personal_day": "Error", "personal_month": "Error", "personal_year": "Error"}
        return []

# --- ML Core Functions (load_and_preprocess_data, train_outcome_model, predict_outcome) ---
# These functions would be the same as in the version from immersive_id="ml_components_py_final_v1"
# For brevity, I will not repeat them here, but assume they are present.
# Please ensure you have the full, correct versions of these functions in your actual file.

def load_and_preprocess_data(json_file_path=USER_DATA_FILE):
    """
    Loads feedback data from the specified JSON file, flattens it,
    defines features based on snapshot data, and prepares it for machine learning.
    Returns X (features DataFrame), y (target Series), and a configured preprocessor.
    """
    raw_data = load_user_feedback()
    if not raw_data:
        print("No raw data loaded from feedback. Cannot preprocess.")
        return None, None, None

    processed_data = []
    for entry in raw_data:
        astro_snapshot = entry.get('astrology_snapshot', {})
        if not isinstance(astro_snapshot, dict): astro_snapshot = {}
        numerology_snapshot = entry.get('numerology_snapshot', {})
        if not isinstance(numerology_snapshot, dict): numerology_snapshot = {}
            
        personal_day_raw = numerology_snapshot.get('personal_day', '0')
        personal_day_val = str(personal_day_raw).split(' ')[0] if isinstance(personal_day_raw, str) else str(personal_day_raw)

        flat_entry = {
            'personal_year': numerology_snapshot.get('personal_year'),
            'personal_month': numerology_snapshot.get('personal_month'),
            'personal_day': personal_day_val,
            'transiting_moon_sign': astro_snapshot.get('transiting_moon_sign'),
            'mercury_retrograde': int(astro_snapshot.get('mercury_retrograde', 0) if pd.notna(astro_snapshot.get('mercury_retrograde')) else 0),
            'dominant_element_today': astro_snapshot.get('dominant_element_today'),
            'dominant_modality_today': astro_snapshot.get('dominant_modality_today'),
            'harmonious_transit_count': astro_snapshot.get('harmonious_transit_count'),
            'challenging_transit_count': astro_snapshot.get('challenging_transit_count'),
            'key_transit_category': astro_snapshot.get('key_transit_category'),
            'user_activity_category': entry.get('user_activity_category', entry.get('user_activity', 'Unknown')),
            'outcome_rating': entry.get('outcome_rating')
        }
        if flat_entry['outcome_rating'] is not None:
            processed_data.append(flat_entry)
{
  "FUSION_AST_SUN_ARIES__NUM_LP_7": {
    "type": "fusion",
    "description": "Bold visionary with deep inner wisdom. You act fast but reflect deeply.",
    "categories": ["leadership", "intuition", "fire-mind"]
  }
}
{
  "FUSION_AST_MOON_PISCES__NUM_LP_1": {
    "type": "fusion",
    "description": "Compassionate leader with a strong sense of self. You inspire others through empathy.",
    "categories": ["empathy", "leadership", "water-heart"]
  },
  "FUSION_AST_MERCURY_GEMINI__NUM_LP_7": {
    "type": "fusion",
    "description": "Curious communicator with a thirst for knowledge. You blend intellect with spiritual insight.",
    "categories": ["communication", "intellect", "air-mind"]
  }
}
{
  "FUSION_AST_VENUS_TAURUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Grounded and practical in love. You value stability and loyalty in relationships.",
    "categories": ["relationships", "stability", "earth-heart"]
  },
  "FUSION_AST_MARS_SCORPIO__NUM_LP_7": {
    "type": "fusion",
    "description": "Intense and transformative energy. You channel deep emotions into powerful actions.",
    "categories": ["transformation", "passion", "water-mind"]
  }
}
{
  "FUSION_AST_JUPITER_SAGITTARIUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Optimistic and adventurous leader. You inspire others with your vision and enthusiasm.",
    "categories": ["adventure", "leadership", "fire-heart"]
  },
  "FUSION_AST_SATURN_CAPRICORN__NUM_LP_7": {
    "type": "fusion",
    "description": "Disciplined and wise. You balance ambition with spiritual depth.",
    "categories": ["discipline", "wisdom", "earth-mind"]
  }
}
{
  "FUSION_AST_URANUS_AQUARIUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Innovative and independent leader. You challenge norms and inspire change.",
    "categories": ["innovation", "leadership", "air-heart"]
  },
  "FUSION_AST_NEPTUNE_PISCES__NUM_LP_7": {
    "type": "fusion",
    "description": "Dreamy and intuitive. You blend creativity with spiritual insight.",
    "categories": ["creativity", "intuition", "water-mind"]
  }
}
{
  "FUSION_AST_PLUTO_SCORPIO__NUM_LP_1": {
    "type": "fusion",
    "description": "Transformative and powerful. You lead with intensity and passion.",
    "categories": ["transformation", "leadership", "fire-heart"]
  },
  "FUSION_AST_CHIRON_ARIES__NUM_LP_7": {
    "type": "fusion",
    "description": "Healer with a warrior spirit. You blend courage with deep emotional insight.",
    "categories": ["healing", "courage", "fire-mind"]
  }
}
{
  "FUSION_AST_LILITH_TAURUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Grounded and sensual. You embrace your desires with confidence.",
    "categories": ["sensuality", "confidence", "earth-heart"]
  },
  "FUSION_AST_NORTH_NODE_GEMINI__NUM_LP_7": {
    "type": "fusion",
    "description": "Curious and adaptable. You seek knowledge and understanding in all things.",
    "categories": ["curiosity", "adaptability", "air-mind"]
  }
}
{
  "FUSION_AST_SOUTH_NODE_SAGITTARIUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Philosophical and expansive. You inspire others with your wisdom and vision.",
    "categories": ["philosophy", "expansion", "fire-heart"]
  },
  "FUSION_AST_PART_OF_FORTUNE_CAPRICORN__NUM_LP_7": {
    "type": "fusion",
    "description": "Disciplined and successful. You achieve your goals through hard work and perseverance.",
    "categories": ["success", "discipline", "earth-mind"]
  }
}
{
  "FUSION_AST_BLACK_MOON_LILITH_AQUARIUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Rebellious and visionary. You challenge societal norms with your unique perspective.",
    "categories": ["rebellion", "vision", "air-heart"]
  },
  "FUSION_AST_VERTEX_PISCES__NUM_LP_7": {
    "type": "fusion",
    "description": "Spiritual and compassionate. You connect deeply with others on an emotional level.",
    "categories": ["spirituality", "compassion", "water-mind"]
  }
}
{
  "FUSION_AST_IC_SCORPIO__NUM_LP_1": {
    "type": "fusion",
    "description": "Intense and transformative roots. You draw strength from deep emotional connections.",
    "categories": ["roots", "transformation", "water-heart"]
  },
  "FUSION_AST_DC_TAURUS__NUM_LP_7": {
    "type": "fusion",
    "description": "Stable and loyal partnerships. You value security and trust in relationships.",
    "categories": ["partnerships", "stability", "earth-mind"]
  }
}
{
  "FUSION_AST_MC_GEMINI__NUM_LP_1": {
    "type": "fusion",
    "description": "Communicative and adaptable career path. You thrive in dynamic environments.",
    "categories": ["career", "communication", "air-heart"]
  },
  "FUSION_AST_NORTH_NODE_SAGITTARIUS__NUM_LP_7": {
    "type": "fusion",
    "description": "Adventurous and philosophical life journey. You seek truth and expansion.",
    "categories": ["adventure", "philosophy", "fire-mind"]
  }
}
{
  "FUSION_AST_SOUTH_NODE_CAPRICORN__NUM_LP_1": {
    "type": "fusion",
    "description": "Disciplined and ambitious past. You learn from your experiences to build a solid foundation.",
    "categories": ["discipline", "ambition", "earth-heart"]
  },
  "FUSION_AST_PART_OF_FORTUNE_AQUARIUS__NUM_LP_7": {
    "type": "fusion",
    "description": "Innovative and humanitarian fortune. You find success through unique ideas and social causes.",
    "categories": ["innovation", "humanitarianism", "air-mind"]
  }
}
{
  "FUSION_AST_BLACK_MOON_LILITH_PISCES__NUM_LP_1": {
    "type": "fusion",
    "description": "Mystical and intuitive. You embrace your spiritual side with confidence.",
    "categories": ["mysticism", "intuition", "water-heart"]
  },
  "FUSION_AST_VERTEX_ARIES__NUM_LP_7": {
    "type": "fusion",
    "description": "Dynamic and pioneering connections. You inspire others with your boldness.",
    "categories": ["pioneering", "connections", "fire-mind"]
  }
}
{
  "FUSION_AST_IC_TAURUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Stable and nurturing roots. You find comfort in security and beauty.",
    "categories": ["roots", "nurturing", "earth-heart"]
  },
  "FUSION_AST_DC_GEMINI__NUM_LP_7": {
    "type": "fusion",
    "description": "Communicative and adaptable partnerships. You thrive in relationships that stimulate your mind.",
    "categories": ["partnerships", "communication", "air-mind"]
  }
}
{
  "FUSION_AST_MC_SAGITTARIUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Adventurous and philosophical career path. You seek truth and expansion in your professional life.",
    "categories": ["career", "adventure", "fire-heart"]
  },
  "FUSION_AST_NORTH_NODE_CAPRICORN__NUM_LP_7": {
    "type": "fusion",
    "description": "Disciplined and ambitious life journey. You achieve success through hard work and perseverance.",
    "categories": ["discipline", "ambition", "earth-mind"]
  }
}
{
  "FUSION_AST_SOUTH_NODE_AQUARIUS__NUM_LP_1": {
    "type": "fusion",
    "description": "Innovative and humanitarian past. You learn from your experiences to inspire change.",
    "categories": ["innovation", "humanitarianism", "air-heart"]
  },
  "FUSION_AST_PART_OF_FORTUNE_PISCES__NUM_LP_7": {
    "type": "fusion",
    "description": "Spiritual and compassionate fortune. You find success through empathy and creativity.",
    "categories": ["spirituality", "compassion", "water-mind"]
  }
}             
{
  "FUSION_AST_BLACK_MOON_LILITH_ARIES__NUM_LP_1": {
    "type": "fusion",
    "description": "Bold and assertive. You embrace your individuality with confidence.",
    "categories": ["individuality", "confidence", "fire-heart"]
  },
  "FUSION_AST_VERTEX_TAURUS__NUM_LP_7": {
    "type": "fusion",
    "description": "Stable and nurturing connections. You value security and loyalty in relationships.",
    "categories": ["nurturing", "stability", "earth-mind"]
  }
} 
{
  "FUSION_AST_IC_GEMINI__NUM_LP_1": {
    "type": "fusion",
    "description": "Communicative and adaptable roots. You find comfort in intellectual stimulation.",
    "categories": ["roots", "communication", "air-heart"]
  },
  "FUSION_AST_DC_SAGITTARIUS__NUM_LP_7": {
    "type": "fusion",
    "description": "Adventurous and philosophical partnerships. You thrive in relationships that expand your horizons.",
    "categories": ["partnerships", "adventure", "fire-mind"]
  }
}           
{
  "FUSION_AST_MC_CAPRICORN__NUM_LP_1": {
    "type": "fusion",
    "description": "Disciplined and ambitious career path. You achieve success through hard work and discipline.",
    "categories": ["career", "discipline", "earth-heart"]
  },
  "FUSION_AST_NORTH_NODE_AQUARIUS__NUM_LP_7": {
    "type": "fusion",
    "description": "Innovative and humanitarian life journey. You learn from your experiences to inspire change.",
    "categories": ["innovation", "humanitarianism", "air-heart"]
  }
}
{
  "FUSION_AST_SOUTH_NODE_PISCES__NUM_LP_1": {
    "type": "fusion",
    "description": "Spiritual and compassionate past. You draw strength from your emotional depth.",
    "categories": ["spirituality", "compassion", "water-heart"]
  },
  "FUSION_AST_PART_OF_FORTUNE_ARIES__NUM_LP_7": {
    "type": "fusion",
    "description": "Dynamic and pioneering fortune. You find success through bold actions and leadership.",
    "categories": ["pioneering", "success", "fire-mind"]
  }
}

        
    df = pd.DataFrame(processed_data)
    y = df['outcome_rating']
    X = df.drop('outcome_rating', axis=1)

    numerical_features = [
        'personal_year', 'personal_month', 'personal_day',
        'mercury_retrograde',
        'harmonious_transit_count', 'challenging_transit_count'
    ]
    categorical_features = [
        'transiting_moon_sign', 'dominant_element_today',
        'dominant_modality_today', 'key_transit_category',
        'user_activity_category'
    ]
    
    numerical_features = [col for col in numerical_features if col in X.columns]
    categorical_features = [col for col in categorical_features if col in X.columns]

    if not numerical_features and not categorical_features:
        print("No valid numerical or categorical features identified.")
        return X, y, None

    for col in numerical_features: X[col] = pd.to_numeric(X[col], errors='coerce')

    numerical_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    categorical_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')), ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

    transformers_list = []
    if numerical_features: transformers_list.append(('num', numerical_pipeline, numerical_features))
    if categorical_features: transformers_list.append(('cat', categorical_pipeline, categorical_features))
    
    if not transformers_list:
        print("No transformers to apply.")
        return X, y, None 

    preprocessor = ColumnTransformer(transformers=transformers_list, remainder='drop')
    return X, y, preprocessor

def train_outcome_model():
    X, y, preprocessor = load_and_preprocess_data()
    if X is None or y is None or preprocessor is None or X.empty or y.empty:
        print("Model training aborted: Invalid data or preprocessor.")
        return False
    if y.nunique() < 2:
        print(f"Model training aborted: Only one class ('{y.unique()[0]}') found. Need at least two classes.")
        return False
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    except ValueError as e:
        print(f"Warning: Could not stratify train-test split: {e}. Splitting without stratification.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
    ])
    try:
        print("Starting model training...")
        model_pipeline.fit(X_train, y_train)
        print("Model training complete.")
        y_pred = model_pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nModel Evaluation (Test Set): Accuracy: {accuracy:.4f}")
        target_names = sorted([str(cls) for cls in y.unique()])
        print("Classification Report:\n", classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
        joblib.dump(model_pipeline, MODEL_FILE)
        print(f"Trained model pipeline saved to {MODEL_FILE}")
        return True
    except Exception as e:
        print(f"An error occurred during model training or saving: {e}")
        import traceback
        traceback.print_exc()
        return False

def predict_outcome(numerology: dict, astrology: dict, user_activity_category: str):
    if not os.path.exists(MODEL_FILE):
        print(f"Prediction error: Model file '{MODEL_FILE}' not found.")
        return "Model not available. Please train first.", None
    try:
        model_pipeline = joblib.load(MODEL_FILE)
        personal_day_raw = numerology.get('personal_day', '0')
        personal_day_val = str(personal_day_raw).split(' ')[0] if isinstance(personal_day_raw, str) else str(personal_day_raw)
        input_features = {
            'personal_year': [numerology.get('personal_year')],
            'personal_month': [numerology.get('personal_month')],
            'personal_day': [personal_day_val],
            'transiting_moon_sign': [astrology.get('transiting_moon_sign')],
            'mercury_retrograde': [int(astrology.get('mercury_retrograde', 0) if pd.notna(astrology.get('mercury_retrograde')) else 0)],
            'dominant_element_today': [astrology.get('dominant_element_today')],
            'dominant_modality_today': [astrology.get('dominant_modality_today')],
            'harmonious_transit_count': [astrology.get('harmonious_transit_count')],
            'challenging_transit_count': [astrology.get('challenging_transit_count')],
            'key_transit_category': [astrology.get('key_transit_category')],
            'user_activity_category': [user_activity_category]
        }
        input_df = pd.DataFrame.from_dict(input_features)
        prediction = model_pipeline.predict(input_df)[0]
        probabilities = model_pipeline.predict_proba(input_df)[0]
        classifier = model_pipeline.named_steps['classifier']
        class_labels = [str(cls) for cls in classifier.classes_]
        probability_map = {class_labels[i]: prob for i, prob in enumerate(probabilities)}
        return str(prediction), probability_map
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        import traceback
        traceback.print_exc()
        return "Prediction error occurred", None
# --- Synthetic Data Generation Helper ---
def generate_synthetic_entry(entry_date):
    """Generates a single synthetic feedback entry."""
    import random
    import datetime

    moon_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", 
                  "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    elements = ["Fire", "Earth", "Air", "Water"]
    modalities = ["Cardinal", "Fixed", "Mutable"]
    key_categories = ["Dynamic", "Stable", "Growth", "Challenge", "Social", 
                      "Emotional", "Detailed", "Creative"]
    activity_categories = ["Work", "Personal", "Social", "Creative", "Routine", "Learning"]
    outcomes = ["Positive", "Neutral", "Negative"]

    # Dummy birth details for numerology engine
    dummy_birth_month = random.randint(1, 12)
    dummy_birth_day = random.randint(1, 28)  # Prevent invalid dates

    # Fetch numerology snapshot
    numerology_snapshot_raw = get_numerological_insights(dummy_birth_month, dummy_birth_day, entry_date)
    personal_day_val = str(numerology_snapshot_raw.get('personal_day', '0')).split(' ')[0]

    numerology_snapshot = {
        "personal_year": numerology_snapshot_raw.get('personal_year'),
        "personal_month": numerology_snapshot_raw.get('personal_month'),
        "personal_day": personal_day_val
    }

    harmonious_transits = random.randint(0, 5)
    challenging_transits = random.randint(0, 3)
    mercury_retro = random.choice([True, False])

    astrology_snapshot = {
        "transiting_moon_sign": random.choice(moon_signs),
        "mercury_retrograde": mercury_retro,
        "dominant_element_today": random.choice(elements),
        "dominant_modality_today": random.choice(modalities),
        "harmonious_transit_count": harmonious_transits,
        "challenging_transit_count": challenging_transits,
        "key_transit_category": random.choice(key_categories)
    }

    user_activity = random.choice(activity_categories)

    outcome_score = harmonious_transits - challenging_transits - (2 if mercury_retro else 0)
    if outcome_score > 1:
        outcome_rating = random.choices(outcomes, weights=[0.6, 0.3, 0.1])[0]
    elif outcome_score < -1:
        outcome_rating = random.choices(outcomes, weights=[0.1, 0.3, 0.6])[0]
    else:
        outcome_rating = random.choices(outcomes, weights=[0.3, 0.4, 0.3])[0]

    return {
        "date": entry_date.strftime("%Y-%m-%d"),
        "numerology_snapshot": numerology_snapshot,
        "astrology_snapshot": astrology_snapshot,
        "user_activity_category": user_activity,
        "user_activity": f"{user_activity} task",
        "outcome_rating": outcome_rating,
        "notes": "Synthetic feedback entry."
    }


# --- Main Execution Block ---
if __name__ == '__main__':
    print("Running ML Components Test Block...")

    generate_new_data = False
    if not os.path.exists(USER_DATA_FILE):
        print(f"'{USER_DATA_FILE}' not found. Will generate synthetic data.")
        generate_new_data = True
    else:
        try:
            with open(USER_DATA_FILE, 'r') as f:
                content = f.read()
                if not content:
                    print(f"'{USER_DATA_FILE}' is empty. Will generate synthetic data.")
                    generate_new_data = True
                else:
                    existing_data = json.loads(content)
                    if not existing_data or len(existing_data) < 10:
                        print(f"'{USER_DATA_FILE}' has only {len(existing_data)} entries. Will regenerate.")
                        generate_new_data = True
                    else:
                        print(f"Found {len(existing_data)} existing entries in '{USER_DATA_FILE}'. Using this data.")
        except Exception as e:
            print(f"Error reading or parsing '{USER_DATA_FILE}': {e}. Will generate new synthetic data.")
            generate_new_data = True

    if generate_new_data:
        num_entries_to_generate = 100
        print(f"Generating {num_entries_to_generate} synthetic feedback entries...")

        synthetic_feedback_data = []
        start_date = datetime.date(2023, 1, 1)
        for i in range(num_entries_to_generate):
            current_date = start_date + datetime.timedelta(days=i)
            synthetic_feedback_data.append(generate_synthetic_entry(current_date))

        try:
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(synthetic_feedback_data, f, indent=4)
            print(f"Successfully wrote {num_entries_to_generate} synthetic entries to '{USER_DATA_FILE}'")
        except Exception as e_write:
            print(f"Error writing synthetic data to '{USER_DATA_FILE}': {e_write}")
            synthetic_feedback_data = [generate_synthetic_entry(datetime.date.today()) for _ in range(5)]

    # --- Training Phase ---
    print("\n--- Attempting to Train Model ---")
    training_successful = train_outcome_model()

    # --- Prediction Phase ---
    if training_successful:
        print("\n--- Attempting a Test Prediction ---")
        sample_numerology = {
            "personal_year": "7",
            "personal_month": "1",
            "personal_day": "5 (Focus)"
        }
        sample_astrology = {
            "transiting_moon_sign": "Aries",
            "mercury_retrograde": False,
            "dominant_element_today": "Fire",
            "dominant_modality_today": "Cardinal",
            "harmonious_transit_count": 2,
            "challenging_transit_count": 1,
            "key_transit_category": "Dynamic"
        }
        sample_activity_cat = "Work"

        prediction, probabilities = predict_outcome(
            sample_numerology, sample_astrology, sample_activity_cat
        )

        print(f"\nTest Prediction for Activity Category '{sample_activity_cat}':")
        print(f"  Predicted Outcome: {prediction}")
        if probabilities:
            formatted_probs = {k: f"{v:.2%}" for k, v in probabilities.items()}
            print(f"  Probabilities: {formatted_probs}")
    else:
        print("\nSkipping test prediction due to unsuccessful model training.")

    print("\nML Components Test Block Finished.")
