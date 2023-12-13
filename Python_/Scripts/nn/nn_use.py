import torch
import PIL
from torchvision import transforms


labels = ['1', '2', '3', '4', '5', '6', '7', '8', 'x']

model = torch.load('C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\model.pt')

model.eval()
img = PIL.Image.open("C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\DATA_\\images\\captcha\\test against\\captcha_test_34.png")
#C:\Users\Jordan\Desktop\Programming\GIT\PESBot\DATA_\images\mineral\captcha_im8.png
transform = transforms.ToTensor()
x = transform(img)

with torch.inference_mode():
    output = model(x.unsqueeze(0))

_, index = torch.max(output, 1)
 
percentage = torch.nn.functional.softmax(output, dim=1)[0] * 100
 
print(labels[index], percentage[index[0]].item())