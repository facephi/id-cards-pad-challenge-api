from fastapi import FastAPI, UploadFile
from PIL import Image
import numpy as np
from api.utils.processor import Example

evaluator = Example()
app = FastAPI()


@app.post("/evaluate/")
async def evaluate(sample: UploadFile):
    image = np.array(Image.open(sample.file))
    result = evaluator.run(image)
    result["filename"] = sample.filename
    return result
