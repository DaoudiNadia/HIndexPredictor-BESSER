"""
H-Index 5-Year Prediction - Neural Network B-UML Model

Input Features (5 total):
  - author_hindex               current h-index
  - author_citation_count       total citations
  - author_papers               total papers published
  - author_age                  career age in years
  - author_mean_citations_per_paper  avg citations per paper

Output:
  - 1 continuous value: predicted h-index 5 years later (regression)

Architecture: 5 -> Linear(64,ReLU) -> Dropout(0.2)
                -> Linear(32,ReLU) -> Dropout(0.2)
                -> Linear(16,ReLU) -> Linear(1)
"""

import sys
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
except NameError:
    sys.path.insert(0, ".")

from besser.BUML.metamodel.nn import (
    NN, LinearLayer, DropoutLayer,
    Configuration, Dataset,
)

# ============ NEURAL NETWORK MODEL ============

hindex_nn: NN = NN(name="HIndexPredictorNN")

hindex_nn.add_layer(LinearLayer(name="l1", actv_func="relu", in_features=5,  out_features=64))
hindex_nn.add_layer(DropoutLayer(name="l2", rate=0.2))
hindex_nn.add_layer(LinearLayer(name="l3", actv_func="relu", in_features=64, out_features=32))
hindex_nn.add_layer(DropoutLayer(name="l4", rate=0.2))
hindex_nn.add_layer(LinearLayer(name="l5", actv_func="relu", in_features=32, out_features=16))
hindex_nn.add_layer(LinearLayer(name="l6", actv_func=None,   in_features=16, out_features=1))

# ============ TRAINING CONFIGURATION ============

config = Configuration(
    batch_size=64,
    epochs=100,
    learning_rate=1e-3,
    optimizer="adam",
    loss_function="mse",
    metrics=["mae"],
)

# ============ DATASET CONFIGURATION ============
# Run prepare_data.py first to produce these CSVs from the TSV source files.

train_data = Dataset(
    name="train_data",
    path_data="../data/train.csv",
    task_type="regression",
    input_format="csv",
)

test_data = Dataset(
    name="test_data",
    path_data="../data/test.csv",
    task_type="regression",
    input_format="csv",
)

hindex_nn.add_configuration(config)
hindex_nn.add_train_data(train_data)
hindex_nn.add_test_data(test_data)

# ============ CODE GENERATION ============

if __name__ == "__main__":
    from besser.generators.nn.pytorch.pytorch_code_generator import PytorchGenerator
    import os

    print(f"Model: {hindex_nn.name}")
    print(f"Layers: {[l.name for l in hindex_nn.layers]}")
    print(f"Config: batch={config.batch_size}, epochs={config.epochs}, lr={config.learning_rate}")

    output_dir = os.path.dirname(os.path.abspath(__file__))

    generator = PytorchGenerator(
        model=hindex_nn,
        output_dir=output_dir,
        generation_type="subclassing",
    )
    generator.generate()
    print(f"\nGenerated PyTorch code in: {output_dir}")