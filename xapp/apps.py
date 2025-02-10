from django.apps import AppConfig
from joblib import load
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class XappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "xapp"

    def ready(self):
        """Loads the model and vectorizer when the app starts."""
        save_models_dir = os.path.join(settings.BASE_DIR, 'SaveModels')
        model_path = os.path.join(save_models_dir, 'model.joblib')
        vector_path = os.path.join(save_models_dir, 'vector.joblib')

        try:
            if os.path.exists(model_path):
                self.model = load(model_path)
                logger.info("Model loaded successfully.")
            else:
                raise FileNotFoundError(f"Model file not found: {model_path}")

            if os.path.exists(vector_path):
                self.vector = load(vector_path)
                logger.info("Vectorizer loaded successfully.")
            else:
                raise FileNotFoundError(f"Vectorizer file not found: {vector_path}")

        except Exception as e:
            logger.error(f"Error loading model or vectorizer: {e}")
            self.model, self.vector = None, None  # Prevents crashes if files are missing
