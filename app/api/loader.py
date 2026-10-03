import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

model = models.resnet50()
weights_path = "resnet50_encoder.pth"
state_dict = torch.load(weights_path, map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], # Standard ImageNet defaults
        std=[0.229, 0.224, 0.225]
    )
])
image_path = "your_image.jpg"
image = Image.open(image_path).convert('RGB')
input_tensor = preprocess(image)
input_batch = input_tensor.unsqueeze(0)
with torch.no_grad():
    output = model(input_batch)
probabilities = torch.nn.functional.softmax(output[0], dim=0)
predicted_class = torch.argmax(probabilities).item()

print(f"Predicted Class Index: {predicted_class}")
