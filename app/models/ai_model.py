import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class AIModel:

    def __init__(self):
        self.model = models.resnet50()
        self.model.fc = nn.Linear(self.model.fc.in_features, 12)

        self.model.load_state_dict(
            torch.load("disaster_hybrid_model.pth", map_location="cpu")
        )


        
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        self.classes = [
            'Earthquake', 'Infrastructure', 'Urban_Fire', 'Wild_Fire',
            'Human_Damage', 'Drought', 'Land_Slide',
            'Non_Damage_Buildings_Street',
            'Non_Damage_Wildlife_Forest',
            'human', 'sea', 'Water_Disaster'
        ]

    def analyze(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            output = self.model(tensor)
            probs = torch.softmax(output, dim=1)
            score = float(probs.max().item() * 100)
            predicted = output.argmax(dim=1).item()

        disaster = self.classes[predicted]

        safe_classes = [
            'Non_Damage_Buildings_Street',
            'Non_Damage_Wildlife_Forest',
            'human', 'sea'
        ]

        severity = 0.0 if disaster in safe_classes else round(score, 2)

        return disaster, severity


ai_model = AIModel()