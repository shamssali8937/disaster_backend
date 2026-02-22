import io
import torch
from torchvision import models, transforms
from PIL import Image

class AIModel:

    def __init__(self):

        self.model = models.resnet50()
        # Uncomment after placing model
        self.model.load_state_dict(torch.load("disaster_hybrid_model.pth", map_location="cpu"))
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

        self.classes = ["Flood", "Fire", "Earthquake", "Accident"]

    def analyze(self, image_bytes: bytes):

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            output = self.model(tensor)
            probs = torch.softmax(output, dim=1)
            score = float(probs.max().item() * 100)
            predicted = output.argmax(dim=1).item()

        disaster = self.classes[predicted] if predicted < len(self.classes) else "Unknown"

        return disaster, round(score, 2)

ai_model = AIModel()