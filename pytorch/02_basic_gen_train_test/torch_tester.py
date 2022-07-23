import torch
import torch.nn as nn
import numpy as np
import pickle

device = 'cuda' if torch.cuda.is_available() else 'cpu'


class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.main = nn.Sequential(
            nn.Linear(3, 6),
            nn.Linear(6, 1)
        )

    def forward(self, x):
        return self.main(x)


with open("model.pickle", "rb") as f:
    model = pickle.load(f)

print(model.state_dict())

# test
model.eval()
x_prd = np.array([0.1, 0.2, 0.1])  # y = 1 + 2*0.1*0.2*0.1
print("expect:", 1 + 2 * 0.1 * 0.2 * 0.1)
x_prd = torch.from_numpy(x_prd)
x_prd = x_prd.float()
x_prd = x_prd.to(device)
print(model(x_prd))
