"""
Inference module for HIndexPredictorNN.
Loads the trained model + scaler and predicts h-index in 5 years
for a given Researcher ORM object.
"""
import os
import glob
import pickle
import importlib.util
import torch

_model = None
_scaler = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NN_DIR   = BASE_DIR
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


def _load_model():
    global _model
    if _model is not None:
        return _model

    # Import NeuralNetwork class from generated code
    spec = importlib.util.spec_from_file_location(
        "pytorch_nn_subclassing",
        os.path.join(NN_DIR, "pytorch_nn_subclassing.py")
    )
    nn_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nn_module)
    NeuralNetwork = nn_module.NeuralNetwork

    # Find the latest .pth file
    pth_files = sorted(glob.glob(os.path.join(NN_DIR, "*.pth")))
    if not pth_files:
        raise FileNotFoundError("No trained model (.pth) found in nn/. Run pytorch_nn_subclassing.py first.")
    model_path = pth_files[-1]

    import sys
    sys.modules["__main__"].NeuralNetwork = NeuralNetwork
    _model = torch.load(model_path, map_location="cpu", weights_only=False)
    _model.eval()
    return _model


def _load_scaler():
    global _scaler
    if _scaler is not None:
        return _scaler
    scaler_path = os.path.join(DATA_DIR, "scaler.pkl")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError("scaler.pkl not found in data/. Run prepare_data.py first.")
    with open(scaler_path, "rb") as f:
        _scaler = pickle.load(f)
    return _scaler


def predict_hindex(researcher) -> float:
    """
    Predict h-index in 5 years for a Researcher ORM object.
    Feature order must match prepare_data.py:
      [hIndex, totalCitations, totalPapers, careerAge, citationsPerPaper]
    """
    model  = _load_model()
    scaler = _load_scaler()

    features = [[
        researcher.hIndex,
        researcher.totalCitations,
        researcher.totalPapers,
        researcher.careerAge,
        researcher.citationsPerPaper,
    ]]

    scaled = scaler.transform(features)
    with torch.no_grad():
        prediction = model(torch.tensor(scaled, dtype=torch.float32)).item()

    return max(0, round(prediction))