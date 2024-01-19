from fastapi import FastAPI, Query
from http import HTTPStatus
from enum import Enum
from fastapi import UploadFile, File
from typing import Optional
import torch
from torchvision import models, transforms
from PIL import Image
import cv2
from models.model import MyNeuralNet

def load_image(img):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(img).unsqueeze(0)

def predict(img, model):
    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs, 1)
    return predicted.item()

app = FastAPI()

# Load the model once, outside of the endpoint function

model = MyNeuralNet()
model.load_state_dict(torch.load('models/checkpoints/best.pth'))
model.eval()

class ItemEnum(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
def root():
    """ Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/restric_items/{item_id}")
def read_item(item_id: ItemEnum):
    return {"item_id": item_id}

@app.get("/query_items")
def read_item(item_id: int = Query(..., description="The item ID")):
    return {"item_id": item_id}


@app.post("/cv_model/")
async def cv_model(data: UploadFile = File(...)):
    with open('image.jpg', 'wb') as image:
        content = await data.read()
        image.write(content)

        img = cv2.imread("image.jpg")
        loaded = load_image(img)
        prediction = predict(loaded, model)
        pred_srting = ""
        if (prediction==1):
            pred_srting = "That is a smoker"
        else:
            pred_srting = "That is not a smoker"

        image.close()

    response = {
        "input": data.filename,
        "prediction": pred_srting,  # Added prediction here
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response

