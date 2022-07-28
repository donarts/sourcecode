import torch
import numpy as np
import torch_train_file_loader

if __name__ == '__main__':
    model = torch_train_file_loader.CustomModel()
    model.load_state_dict(torch.load("model.pt"))

    print(model.state_dict())

    # test
    model.eval()
    x_prd = np.array([0.1, 0.2, 0.1])  # y = 1 + 2*0.1*0.2*0.1
    print("expect:", 1 + 2 * 0.1 * 0.2 * 0.1)
    x_prd = torch.from_numpy(x_prd)
    x_prd = x_prd.float()
    x_prd = x_prd.to(torch_train_file_loader.device)
    print(model(x_prd))
