import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision
from torch.utils.data import DataLoader
from dataset import CustomDataset


# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device.type)

in_channel = 3
num_classes = 2
learning_rate = 1e-3
batch_size = 32
num_epochs = 12

#Load the data
dataset = CustomDataset(
    csv_file='C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\minerals.csv',
    root_dir='C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\mineral_images',
    transform=transforms.ToTensor()
)

print(len(dataset))

train_set, test_set = torch.utils.data.random_split(dataset, [int(len(dataset)*0.8)+1, int(len(dataset)*0.2)])
train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)

model = torchvision.models.googlenet(pretrained=True)
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    losses = []

    for batch_idx, (data, targets) in enumerate(train_loader):

        data = data.to(device=device)
        targets = targets.to(device=device)

        scores = model(data)
        loss = criterion(scores, targets)

        losses.append(loss.item())

        optimizer.zero_grad()
        loss.backward()

        optimizer.step()

    print(f'Cost at epoch {epoch} is {sum(losses)/len(losses):.5f}')

def check_accuracy(loader, model):
    num_correct = 0
    num_samples = 0
    model.eval()

    with torch.no_grad():
        for x, y in loader:
            x = x.to(device=device)
            y = y.to(device=device)

            scores = model(x)
            _, predictions = scores.max(1)
            num_correct += (predictions == y).sum()
            num_samples += predictions.size(0)
        
        print(f'Got {num_correct} / {num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}')

    model.train()

print("Checking accuracy on Training Set")
check_accuracy(train_loader, model)

print("Checking accuracy on Test Set")
check_accuracy(test_loader, model)

torch.save(model, 'C:\\Users\\Jordan\\Desktop\\Programming\\GIT\\PESBot\\Python_\\Scripts\\nn\\mineral_model.pt')