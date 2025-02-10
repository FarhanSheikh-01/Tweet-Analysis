# test_vectorizer.py
from joblib import load

vector = load("SaveModels/vector.joblib")
print("Loaded object type:", type(vector))

import ntscraper
print(dir(ntscraper))
