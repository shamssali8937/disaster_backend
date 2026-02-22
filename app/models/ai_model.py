# import io
# import torch
# from torchvision import models, transforms
# from PIL import Image

# class AIModel:

#     def __init__(self):

#         self.model = models.resnet50()
#         # Uncomment after placing model
#         self.model.load_state_dict(torch.load("disaster_hybrid_model.pth", map_location="cpu"))
#         self.model.eval()

#         self.transform = transforms.Compose([
#             transforms.Resize((224, 224)),
#             transforms.ToTensor(),
#         ])

#         self.classes = ["Flood", "Fire", "Earthquake", "Accident"]

#     def analyze(self, image_bytes: bytes):

#         image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#         tensor = self.transform(image).unsqueeze(0)

#         with torch.no_grad():
#             output = self.model(tensor)
#             probs = torch.softmax(output, dim=1)
#             score = float(probs.max().item() * 100)
#             predicted = output.argmax(dim=1).item()

#         disaster = self.classes[predicted] if predicted < len(self.classes) else "Unknown"

#         return disaster, round(score, 2)

# ai_model = AIModel()

import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class AIModel:

    def __init__(self):
        # 1. Initialize base architecture
        self.model = models.resnet50()
        
        # 2. Modify the output layer to match your 12 Kaggle classes
        self.model.fc = nn.Linear(self.model.fc.in_features, 12)

        # 3. Load your downloaded weights (make sure 'my_model.pth' is in the root folder)
        self.model.load_state_dict(torch.load("disaster_hybrid_model.pth", map_location="cpu"))
        self.model.eval()

        # 4. Use the EXACT transforms from your Kaggle Validation script
        # Adding normalization here is critical, otherwise accuracy will drop
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # 5. The EXACT class list printed in your Kaggle output
        # WARNING: The order must match this exactly!
        self.classes = [
            'Earthquake', 'Infrastructure', 'Urban_Fire', 'Wild_Fire', 
            'Human_Damage', 'Drought', 'Land_Slide', 'Non_Damage_Buildings_Street', 
            'Non_Damage_Wildlife_Forest', 'human', 'sea', 'Water_Disaster'
        ]

    def analyze(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            output = self.model(tensor)
            probs = torch.softmax(output, dim=1)
            score = float(probs.max().item() * 100)
            predicted = output.argmax(dim=1).item()

        disaster_type = self.classes[predicted] if predicted < len(self.classes) else "Unknown"

        # 6. Smart Severity Filter
        # If the model detects a non-damage class, force severity to 0%
        safe_classes = ['Non_Damage_Buildings_Street', 'Non_Damage_Wildlife_Forest', 'human', 'sea']
        if disaster_type in safe_classes:
            severity = 0.0
        else:
            severity = round(score, 2)

        return disaster_type, severity

ai_model = AIModel()