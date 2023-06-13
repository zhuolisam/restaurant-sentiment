import sys
from typing import List
import numpy as np
from time import perf_counter
import logging

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

class ResumeRanker:
    # Class variable for the model pipeline
    ranker = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.classifier is None:
            t0 = perf_counter()
            #load model and download stuff
            elapsed = 1000 * (perf_counter() - t0)
            log.info("Model warm-up time: %d ms.", elapsed)

    @classmethod
    def predict(cls, text: str, candidate_labels: List[str]):
        results= []
        return cls.classifier(results)