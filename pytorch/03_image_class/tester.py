import trainer
import torch
from PIL import Image

if __name__ == '__main__':
    model = trainer.CustomModel()
    model.load_state_dict(torch.load("model.pt"))
    print(model.state_dict())

    # test
    test_images = ["cats_and_dogs_filtered/train/cats/cat.1.jpg",
                   "cats_and_dogs_filtered/train/cats/cat.2.jpg",
                   "cats_and_dogs_filtered/train/dogs/dog.1.jpg",
                   "cats_and_dogs_filtered/train/dogs/dog.2.jpg",
                   "cats_and_dogs_filtered/validation/cats/cat.2001.jpg",
                   "cats_and_dogs_filtered/validation/dogs/dog.2001.jpg",
                   "cats_and_dogs_filtered/validation/cats/cat.2004.jpg",
                   "cats_and_dogs_filtered/validation/dogs/dog.2004.jpg",
                   ]

    model.eval()
    print(model)
    for test_image in test_images:
        print(test_image)
        x_prd = Image.open(test_image)
        x_prd = trainer.data_transforms['validation'](x_prd)
        print(x_prd.shape)
        x_prd = x_prd.unsqueeze(0)
        print(x_prd.shape)

        with torch.no_grad():
            x_prd = x_prd.to(trainer.device)
            y = model(x_prd)
            print("result:", y)
            if y[0][0] > y[0][1]:
                print("cat")
            else:
                print("dog")