import torch
from torch import nn
import matplotlib.pyplot as plt


X = torch.arange(0, 1, .02).unsqueeze(dim=1)
weight = 0.7
bias = 0.3
y = weight * X + bias

#80% data is training
trainingData = X[:int(.8*len(X))]
trainingLabels = y[:int(.8*len(y))]

#20% data is test
testData = X[int(.8*len(X)):]
testLabels = y[int(.8*len(y)):]

def VisualizePredictions(trainingData, traininglabels, testData, testLabels, predictions = None):
    plt.figure(figsize=(10,7))
    plt.scatter(trainingData, traininglabels, c='b', s=4, label="Lipa (training)")
    plt.scatter(testData, testLabels, c='g', s=4, label="Dua (testing)")

    if predictions is not None:
        plt.scatter(testData, predictions, c='r', s=4, label="Chunk (prediction)")
    
    plt.legend(prop={"size": 14})
    plt.show()

class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__() 

        
        self.weights = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float))
        self.bias = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float)) 

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.weights * x + self.bias

torch.manual_seed(67)

model0 = LinearRegressionModel()

lossFunction = nn.L1Loss()

optimizer = torch.optim.SGD(params=model0.parameters(), lr=0.01) 

epochs = 10000

for epoch in range(epochs):
    model0.train() #starts training mode

    prediction = model0(trainingData) 
    loss = lossFunction(prediction, trainingLabels) 

    optimizer.zero_grad()
    loss.backward()
    optimizer.step() 

    model0.eval() #disabled training mode

    if epoch % 100 == 0: print(loss)

with torch.inference_mode():
    labelPrediction = model0(testData)

    testLoss = lossFunction(labelPrediction, testLabels)

VisualizePredictions(trainingData=trainingData, traininglabels= trainingLabels, testData=testData, testLabels=testLabels, predictions=labelPrediction)


