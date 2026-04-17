# H-Index Predictor (Generated Output)

An academic impact forecasting tool that predicts a researcher's H-Index 5 years ahead. Generated with BESSER's WebApp and PytorchGenerator, with minimal modifications to the generated code.

> **See also:** The [v2-improved branch](https://github.com/daoudinadia/HIndexPredictor-BESSER/tree/v2-improved) extends this generated output with UI enhancements.

## What is this?

This project demonstrates how BESSER's code generation can be combined with its neural network modeling capabilities. Starting from a **B-UML class diagram** and a **B-UML NN model**, BESSER generated:

- A **FastAPI backend** with full CRUD endpoints, SQLAlchemy ORM models, and Pydantic validation schemas
- A **React + TypeScript frontend** with data tables, forms, and instance method buttons
- **PyTorch training code** from the NN model via BESSER's PytorchGenerator, then manually integrated into the API as an instance method on `Researcher`

## How it Works

1. A `Researcher` record is created with current academic metrics (H-Index, citations, papers, career age)
2. Clicking **Predict My H-Index in 5 Years** calls the `/researcher/{id}/methods/predict/` endpoint
3. The backend loads the trained PyTorch model and sklearn scaler, runs inference, and returns the predicted H-Index alongside the average for the researcher's field

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Frontend | React 18, TypeScript, Vite |
| ML | PyTorch, scikit-learn |
| Database | SQLite |
| Deployment | Docker Compose |

## BESSER Features Used

| Feature | Purpose |
|---------|---------|
| WebApp Generator | Full-stack CRUD app from B-UML class diagram |
| PytorchGenerator | MLP regression model code from B-UML NN model |

## Domain Model

The application models `Researcher` entities linked to `ResearchField`, generated from B-UML class diagram in the [BESSER online editor](https://editor.besser-pearl.org/).

## Data

The neural network is trained on the [Lucaweihs/impact-prediction](https://github.com/lucaweihs/impact-prediction) dataset from Semantic Scholar (1975-2015).

The TSV source files are not included in this repository due to their size. Download them and place them in `backend/data/` before running `prepare_data.py`:

- https://s3-us-west-2.amazonaws.com/ai2-s2/lucaw/authorFeatures-1975-2005-2015-2.tsv.gz
- https://s3-us-west-2.amazonaws.com/ai2-s2/lucaw/authorResponses-1975-2005-2015-2.tsv.gz

Features used: current h-index, total citations, total papers, career age, and mean citations per paper. Target: h-index 5 years later.

The trained model achieves a Mean Absolute Error (MAE) of ~0.9, meaning predictions are typically within 1 h-index point.

## Getting Started

### With Docker

```bash
docker compose up --build
```

Once the containers are running, seed the database once by running:

```bash
docker compose exec backend python seed.py
```

Frontend: http://localhost:3000
Backend API docs: http://localhost:8000/docs

### Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main_api:app --host 0.0.0.0 --port 8000
```

Once the backend is running for the first time, the database is created automatically. Then run the seed script once to populate the research fields:
```bash
python seed.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Training the Neural Network (optional)

The trained model is included. To retrain from scratch:
```bash
cd backend/nn
python prepare_data.py       # normalise raw data → train/test CSVs + scaler
python pytorch_nn_subclassing.py    # train and save the .pth model
```

## Project Structure

```
HIndexPredictor_generated/
├── backend/
│   ├── main_api.py              # FastAPI app with all CRUD and predict endpoints
│   ├── sql_alchemy.py
│   ├── pydantic_classes.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── nn/
│   │   ├── nn_model.py          # B-UML NN model (BESSER PytorchGenerator input)
│   │   ├── pytorch_nn_subclassing.py  # Generated training code
│   │   ├── nn_inference.py      # Inference helper used by the API
│   │   └── *.pth                # Trained model weights
│   ├── data/
│   │   ├── train.csv / test.csv
│   │   └── scaler.pkl
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/Home.tsx
│   │   ├── components/
│   └── Dockerfile
└── docker-compose.yml
```

## About BESSER

[BESSER](https://github.com/BESSER-PEARL/BESSER) is a low-code platform for smart software modeling that uses model-driven engineering to generate full-stack applications and ML pipelines from visual domain models.

- Documentation: https://besser.readthedocs.io/
- Online Editor: https://editor.besser-pearl.org/