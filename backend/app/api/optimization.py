"""
Genetic Algorithm Optimization API Endpoints

Provides endpoints for hyperparameter optimization using genetic algorithms.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.ml.genetic_algorithm import GeneticOptimizer, create_model_fitness_function
from app.ml.model import RegressionNet
import torch
import numpy as np

router = APIRouter(prefix="/optimization", tags=["optimization"])


class OptimizationRequest(BaseModel):
    """Request for hyperparameter optimization"""
    param_bounds: Dict[str, List[float]]  # {"param_name": [min, max]}
    population_size: int = 50
    generations: int = 20
    mutation_rate: float = 0.2
    crossover_rate: float = 0.7
    model_type: str = "regression"  # "regression" or "unet"


@router.post("/optimize")
def optimize_hyperparameters(request: OptimizationRequest):
    """
    Optimize hyperparameters using genetic algorithm
    
    Args:
        request: Optimization request with parameter bounds
        
    Returns:
        Optimization results with best parameters
    """
    try:
        # Convert bounds to tuples
        param_bounds = {
            name: (bounds[0], bounds[1])
            for name, bounds in request.param_bounds.items()
        }
        
        # Create dummy fitness function (in production, use real training data)
        def dummy_fitness(params: Dict) -> float:
            """Dummy fitness function for demonstration"""
            # In real scenario, this would train and evaluate a model
            # For demo, return a simple function of parameters
            score = 0.0
            for name, value in params.items():
                if "learning_rate" in name.lower():
                    # Optimal around 0.001
                    score -= abs(value - 0.001) * 1000
                elif "hidden" in name.lower() or "dim" in name.lower():
                    # Optimal around 64
                    score -= abs(value - 64) * 0.1
                else:
                    score -= abs(value) * 0.01
            return score
        
        # Create optimizer
        optimizer = GeneticOptimizer(
            fitness_function=dummy_fitness,
            param_bounds=param_bounds,
            population_size=request.population_size,
            generations=request.generations,
            mutation_rate=request.mutation_rate,
            crossover_rate=request.crossover_rate
        )
        
        # Run optimization
        results = optimizer.optimize()
        
        return {
            "success": True,
            "best_parameters": results["best_parameters"],
            "best_fitness": results["best_fitness"],
            "evolution_history": {
                "generations": results["history"]["generations"],
                "best_fitness": results["history"]["best_fitness"],
                "avg_fitness": results["history"]["avg_fitness"]
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )


@router.get("/example-bounds")
def get_example_bounds():
    """
    Get example parameter bounds for common models
    
    Returns:
        Example parameter bounds for different model types
    """
    return {
        "regression_net": {
            "learning_rate": [0.0001, 0.01],
            "hidden_dim_1": [32, 128],
            "hidden_dim_2": [32, 128],
            "dropout_rate": [0.0, 0.5]
        },
        "unet": {
            "learning_rate": [0.0001, 0.01],
            "features_0": [32, 128],
            "features_1": [64, 256],
            "features_2": [128, 512]
        }
    }


