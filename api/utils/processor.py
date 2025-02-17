from typing import Any, Dict
import numpy as np
import random
from abc import ABC, abstractmethod


class IEvaluator(ABC):
    """Interface used to perform predictions on models so that can be used inside the API."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # add your initialization code, i.e., load model weights

    @abstractmethod
    def run(self, image: np.ndarray) -> Dict[str, Any]:
        """Performs a prediction over the specified image and returns a dictionary with
        prediction score and additional metadata.

        Args:
            image (np.ndarray): A numpy array containing the input image in RGB format and uint8 data type.

        Returns:
            Dict[str, Any]: A dictionary that should contain the prediction score and additional metadata.
        """
        # add your evaluation code, i.e., call your model's predict method with the image
        # return a dictionary with score and additional metadata
        pass


class Example(IEvaluator):
    """Example implementation of the IEvaluator interface.
    This implementation uses a random prediction model.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize random prediction model
        random.seed(0)

    def run(self, image: np.ndarray) -> Dict[str, Any]:
        # perform random prediction
        score = random.randint(0, 100)
        height, width = image.shape[:2]

        # return dictionary
        return {"score": score, "width": width, "height": height}
