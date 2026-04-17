"""PyTorch code generated based on BUML."""
import torch
from datetime import datetime

import pandas as pd
from torch import nn

from sklearn.metrics import mean_absolute_error


# Define the network architecture
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(in_features=5, out_features=64)
        self.actv_func_relu = nn.ReLU()
        self.l2 = nn.Dropout(p=0.2)
        self.l3 = nn.Linear(in_features=64, out_features=32)
        self.l4 = nn.Dropout(p=0.2)
        self.l5 = nn.Linear(in_features=32, out_features=16)
        self.l6 = nn.Linear(in_features=16, out_features=1)


    def forward(self, x):
        x = self.l1(x)
        x = self.actv_func_relu(x)
        x = self.l2(x)
        x = self.l3(x)
        x = self.actv_func_relu(x)
        x = self.l4(x)
        x = self.l5(x)
        x = self.actv_func_relu(x)
        x = self.l6(x)
        return x


# Dataset preparation
def load_dataset(csv_file):
    # Load data from CSV file
    data = pd.read_csv(csv_file)
    # Extract features and targets
    features = data.iloc[:, :-1].values.astype("float32")
    targets = data.iloc[:, -1].values.astype("float32")
    # Convert to PyTorch tensors
    features_tensor = torch.tensor(features)
    targets_tensor = torch.tensor(targets)
    # Create a TensorDataset
    dataset = torch.utils.data.TensorDataset(features_tensor, targets_tensor)
    return dataset

def main():
    # Loading data
    train_dataset = load_dataset("../data/train.csv")
    test_dataset = load_dataset("../data/test.csv")

    # Create data loaders
    train_loader = torch.utils.data.DataLoader(
        dataset=train_dataset, batch_size=64, shuffle=True)
    test_loader = torch.utils.data.DataLoader(
        dataset=test_dataset, batch_size=64, shuffle=False)

    # Define the network, loss function, and optimizer
    HIndexPredictorNN = NeuralNetwork()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(HIndexPredictorNN.parameters(), lr=0.001)

    # Train the neural network
    print('##### Training the model')
    for epoch in range(100):
        # Initialize the running loss for the current epoch
        running_loss = 0.0
        total_loss = 0.0
        # Iterate over mini-batches of training data
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            # Zero the gradients to prepare for backward pass
            optimizer.zero_grad()
            outputs = HIndexPredictorNN(inputs)
            # Compute the loss
            labels = labels.unsqueeze(1)

            loss = criterion(outputs, labels)
            loss.backward()
            # Update model parameters based on computed gradients
            optimizer.step()
            running_loss += loss.item()
            total_loss += loss.item()
            if i % 200 == 199:    # Print every 200 mini-batches
                print(
                    f"[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 200:.3f}"
                )
                running_loss = 0.0
        print(
            f"[{epoch + 1}] overall loss for epoch: "
            f"{total_loss / len(train_loader):.3f}"
        )
    print('Training finished')

    # Evaluate the neural network
    print('##### Evaluating the model')
    # Disable gradient calculation during inference
    with torch.no_grad():
        # Initialize lists to store predicted and true labels
        predicted_labels = []
        true_labels = []
        test_loss = 0.0
        for data in test_loader:
            # Extract inputs and labels from the data batch
            inputs, labels = data
            true_labels.extend(labels)
            # Forward pass
            outputs = HIndexPredictorNN(inputs)
            predicted = outputs.numpy()
            labels = labels.unsqueeze(1)
            predicted_labels.extend(predicted)
            test_loss += criterion(outputs, labels).item()

    average_loss = test_loss / len(test_loader)
    print(f"Test Loss: {average_loss:.3f}")

    # Calculate the metrics
    metrics = ['mae']
    mae = mean_absolute_error(true_labels, predicted_labels)
    print(f"Mean Absolute Error (MAE): {mae}")

    # Save the neural network
    print('##### Saving the model')
    torch.save(HIndexPredictorNN, f"hindexpredictornn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pth")
    print("The model is saved successfully")


if __name__ == "__main__":
    main()