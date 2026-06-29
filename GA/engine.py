# ga/engine.py
# The main Genetic Algorithm loop.
# Runs for a fixed number of generations, applying selection, crossover,
# and mutation each round. Uses elitism to preserve the top performers.

import random
from ga.chromosome import Chromosome
from ga.fitness import compute_fitness
from ga.operators import selection, crossover, mutate
from simulator.evaluator import evaluate_firewall


def run_ga(packets, population_size=50, generations=200, elite_count=10):
    """
    Runs the full Genetic Algorithm.

    Args:
        packets         (list[dict]): Test packets from sample_packets.json.
        population_size (int):        Number of chromosomes per generation.
        generations     (int):        How many generations to evolve.
        elite_count     (int):        How many top performers carry over unchanged.

    Returns:
        dict with:
            best_chromosome (Chromosome): The best firewall found.
            history (list[dict]):         Per-generation stats:
                                          generation, best_fitness, avg_fitness, avg_rule_count
    """
    # Initialize random population
    population = [Chromosome() for _ in range(population_size)]
    history = []

    for gen in range(generations):
        # Score everyone
        fitnesses = [compute_fitness(c, packets) for c in population]

        # Track stats for this generation
        best_fitness = max(fitnesses)
        avg_fitness  = sum(fitnesses) / len(fitnesses)
        avg_rules    = sum(len(c.rules) for c in population) / len(population)
        best_idx     = fitnesses.index(best_fitness)
        best_stats   = evaluate_firewall(population[best_idx].rules, packets)
        history.append({
            "generation":     gen + 1,
            "best_fitness":   best_fitness,
            "avg_fitness":    avg_fitness,
            "avg_rule_count": avg_rules,
            "best_accuracy":  best_stats["accuracy"],
        })

        if (gen + 1) % 50 == 0:
            print(f"Gen {gen+1}: best={best_fitness:.2f}, avg_rules={avg_rules:.1f}")

        # Elitism: carry the top `elite_count` chromosomes unchanged
        sorted_pairs = sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)
        elites = [c for _, c in sorted_pairs[:elite_count]]

        # Fill the rest of the new population via selection + crossover + mutation
        new_population = elites[:]
        while len(new_population) < population_size:
            parent_a = selection(population, fitnesses)
            parent_b = selection(population, fitnesses)
            child    = crossover(parent_a, parent_b)
            child    = mutate(child)
            new_population.append(child)

        population = new_population

    # Return the best chromosome and the full history
    final_fitnesses = [compute_fitness(c, packets) for c in population]
    best_idx = final_fitnesses.index(max(final_fitnesses))
    return {
        "best_chromosome": population[best_idx],
        "history":         history,
    }