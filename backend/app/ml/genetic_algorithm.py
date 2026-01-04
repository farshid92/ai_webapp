"""
Genetic Algorithm for Hyperparameter Optimization

Uses evolutionary algorithms to optimize model hyperparameters and architecture.
Based on DEAP (Distributed Evolutionary Algorithms in Python).
"""

import random
import numpy as np
from typing import List, Tuple, Dict, Callable, Any
from deap import base, creator, tools, algorithms
import torch
from app.ml.model import RegressionNet
from app.ml.unet import UNet


class GeneticOptimizer:
    """
    Genetic Algorithm optimizer for hyperparameter tuning
    
    Optimizes:
    - Learning rate
    - Hidden layer sizes
    - Activation functions
    - Dropout rates
    - Architecture parameters
    """
    
    def __init__(
        self,
        fitness_function: Callable,
        param_bounds: Dict[str, Tuple[float, float]],
        population_size: int = 50,
        generations: int = 20,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.7
    ):
        """
        Args:
            fitness_function: Function that evaluates a set of parameters
            param_bounds: Dictionary of parameter_name -> (min, max) bounds
            population_size: Size of population
            generations: Number of generations
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
        """
        self.fitness_function = fitness_function
        self.param_bounds = param_bounds
        self.param_names = list(param_bounds.keys())
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        # Setup DEAP
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        self.toolbox = base.Toolbox()
        self._setup_ga()
    
    def _setup_ga(self):
        """Setup genetic algorithm operators"""
        # Attribute generator
        for i, (param_name, (min_val, max_val)) in enumerate(self.param_bounds.items()):
            self.toolbox.register(
                f"attr_{i}",
                random.uniform,
                min_val,
                max_val
            )
        
        # Individual creator
        self.toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            [getattr(self.toolbox, f"attr_{i}") for i in range(len(self.param_bounds))],
            n=1
        )
        
        # Population creator
        self.toolbox.register(
            "population",
            tools.initRepeat,
            list,
            self.toolbox.individual
        )
        
        # Evaluation
        self.toolbox.register("evaluate", self._evaluate)
        
        # Genetic operators
        self.toolbox.register("mate", tools.cxBlend, alpha=0.5)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
    
    def _evaluate(self, individual: List[float]) -> Tuple[float]:
        """
        Evaluate fitness of an individual
        
        Args:
            individual: List of parameter values
            
        Returns:
            Fitness score (tuple for DEAP)
        """
        # Convert individual to parameter dictionary
        params = {
            name: individual[i]
            for i, name in enumerate(self.param_names)
        }
        
        # Ensure parameters are within bounds
        for i, (name, (min_val, max_val)) in enumerate(self.param_bounds.items()):
            params[name] = np.clip(params[name], min_val, max_val)
        
        # Evaluate fitness
        fitness = self.fitness_function(params)
        return (fitness,)
    
    def optimize(self) -> Dict[str, Any]:
        """
        Run genetic algorithm optimization
        
        Returns:
            Dictionary with best parameters and evolution history
        """
        # Create initial population
        population = self.toolbox.population(n=self.population_size)
        
        # Evaluate initial population
        fitnesses = list(map(self.toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # Evolution history
        history = {
            "best_fitness": [],
            "avg_fitness": [],
            "generations": []
        }
        
        # Evolution loop
        for generation in range(self.generations):
            # Select next generation
            offspring = self.toolbox.select(population, len(population))
            offspring = list(map(self.toolbox.clone, offspring))
            
            # Apply crossover and mutation
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.crossover_rate:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            
            for mutant in offspring:
                if random.random() < self.mutation_rate:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            # Evaluate offspring
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            # Replace population
            population[:] = offspring
            
            # Record statistics
            fits = [ind.fitness.values[0] for ind in population]
            history["best_fitness"].append(max(fits))
            history["avg_fitness"].append(np.mean(fits))
            history["generations"].append(generation)
        
        # Get best individual
        best_ind = tools.selBest(population, 1)[0]
        best_params = {
            name: best_ind[i]
            for i, name in enumerate(self.param_names)
        }
        
        return {
            "best_parameters": best_params,
            "best_fitness": best_ind.fitness.values[0],
            "history": history
        }


def create_model_fitness_function(
    model_class,
    train_data: Tuple[torch.Tensor, torch.Tensor],
    val_data: Tuple[torch.Tensor, torch.Tensor] = None
) -> Callable:
    """
    Create fitness function for model hyperparameter optimization
    
    Args:
        model_class: Model class to optimize
        train_data: (X_train, y_train) tuple
        val_data: Optional (X_val, y_val) tuple
        
    Returns:
        Fitness function
    """
    X_train, y_train = train_data
    
    def fitness_function(params: Dict[str, float]) -> float:
        """
        Fitness function: negative validation loss (higher is better)
        """
        try:
            # Create model with parameters
            if model_class == RegressionNet:
                model = RegressionNet(input_dim=int(params.get("input_dim", 4)))
            elif model_class == UNet:
                model = UNet(
                    in_channels=int(params.get("in_channels", 3)),
                    out_channels=int(params.get("out_channels", 1))
                )
            else:
                model = model_class()
            
            # Simple training (few epochs for speed)
            optimizer = torch.optim.Adam(
                model.parameters(),
                lr=params.get("learning_rate", 0.001)
            )
            criterion = torch.nn.MSELoss()
            
            model.train()
            for _ in range(5):  # Quick training
                optimizer.zero_grad()
                pred = model(X_train)
                loss = criterion(pred, y_train)
                loss.backward()
                optimizer.step()
            
            # Evaluate
            model.eval()
            with torch.no_grad():
                if val_data is not None:
                    X_val, y_val = val_data
                    pred = model(X_val)
                    loss = criterion(pred, y_val).item()
                else:
                    pred = model(X_train)
                    loss = criterion(pred, y_train).item()
            
            # Return negative loss (GA maximizes)
            return -loss
        
        except Exception as e:
            # Return very bad fitness for invalid parameters
            return -1e6
    
    return fitness_function


