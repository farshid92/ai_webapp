"""
Ensemble Learning Implementation

Combines multiple models to improve prediction accuracy and robustness.
Supports voting, weighted averaging, and stacking methods.
"""

import torch
from typing import List, Dict, Union, Callable
from app.ml.base import BaseModel
import numpy as np


class EnsemblePredictor:
    """
    Ensemble predictor that combines multiple models
    
    Methods:
    - Voting: Majority vote for classification
    - Averaging: Mean prediction for regression
    - Weighted Averaging: Weighted mean based on model performance
    - Stacking: Meta-learner on top of base models
    """
    
    def __init__(
        self,
        models: List[BaseModel],
        weights: List[float] = None,
        method: str = "weighted_average"
    ):
        """
        Args:
            models: List of models to ensemble
            weights: Optional weights for each model (default: equal weights)
            method: Ensemble method ('voting', 'average', 'weighted_average', 'stacking')
        """
        self.models = models
        self.method = method
        
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
        
        if len(weights) != len(models):
            raise ValueError("Number of weights must match number of models")
        
        self.weights = np.array(weights)
        self.weights = self.weights / self.weights.sum()  # Normalize
    
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """
        Make ensemble prediction
        
        Args:
            x: Input tensor
            
        Returns:
            Ensemble prediction
        """
        predictions = []
        
        for model in self.models:
            with torch.no_grad():
                pred = model.predict(x)
                predictions.append(pred.cpu())
        
        predictions = torch.stack(predictions)
        
        if self.method == "average":
            return predictions.mean(dim=0)
        elif self.method == "weighted_average":
            weights_tensor = torch.tensor(self.weights, dtype=torch.float32)
            weights_tensor = weights_tensor.view(-1, *([1] * (predictions.dim() - 1)))
            return (predictions * weights_tensor).sum(dim=0)
        elif self.method == "voting":
            # For classification, use majority vote
            if predictions.dim() > 2:
                # For segmentation/classification maps
                return torch.mode(predictions.long(), dim=0)[0].float()
            else:
                # For single predictions
                return torch.mode(predictions.long(), dim=0)[0].float()
        else:
            raise ValueError(f"Unknown ensemble method: {self.method}")
    
    def predict_with_uncertainty(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Predict with uncertainty estimation
        
        Args:
            x: Input tensor
            
        Returns:
            Dictionary with 'prediction' and 'uncertainty' (std across models)
        """
        predictions = []
        
        for model in self.models:
            with torch.no_grad():
                pred = model.predict(x)
                predictions.append(pred.cpu())
        
        predictions = torch.stack(predictions)
        mean_pred = predictions.mean(dim=0)
        std_pred = predictions.std(dim=0)
        
        return {
            "prediction": mean_pred,
            "uncertainty": std_pred,
            "std": std_pred
        }


class ModelComparator:
    """
    Compare performance of multiple models
    """
    
    def __init__(self, models: Dict[str, BaseModel]):
        """
        Args:
            models: Dictionary of model_name -> model
        """
        self.models = models
    
    def compare_predictions(
        self,
        x: torch.Tensor,
        ground_truth: torch.Tensor = None
    ) -> Dict[str, Dict]:
        """
        Compare predictions from all models
        
        Args:
            x: Input tensor
            ground_truth: Optional ground truth for evaluation
            
        Returns:
            Dictionary with predictions and metrics for each model
        """
        results = {}
        
        for name, model in self.models.items():
            with torch.no_grad():
                pred = model.predict(x)
            
            result = {"prediction": pred.cpu().numpy()}
            
            if ground_truth is not None:
                # Calculate metrics
                if pred.shape == ground_truth.shape:
                    mse = torch.mean((pred - ground_truth) ** 2).item()
                    mae = torch.mean(torch.abs(pred - ground_truth)).item()
                    result["mse"] = mse
                    result["mae"] = mae
                    result["rmse"] = np.sqrt(mse)
            
            results[name] = result
        
        return results


