# visualizer/dashboard.py
# Visualizes how the GA improved the firewall over generations.
# Requires matplotlib: pip install matplotlib

import matplotlib.pyplot as plt


def show_dashboard(history):
    """
    Plots three charts from the GA's generation history:
        1. Best fitness over generations
        2. Average rule count over generations
        3. (Derived) Security accuracy trend via best fitness

    Args:
        history (list[dict]): The history list returned by engine.run_ga().
    """
    generations  = [h["generation"]     for h in history]
    best_fitness = [h["best_fitness"]   for h in history]
    avg_fitness  = [h["avg_fitness"]    for h in history]
    avg_rules    = [h["avg_rule_count"] for h in history]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("Firewall GA Optimization Results", fontsize=14)

    # Chart 1: Fitness over time
    axes[0].plot(generations, best_fitness, label="Best", color="green")
    axes[0].plot(generations, avg_fitness,  label="Avg",  color="blue", linestyle="--")
    axes[0].set_title("Fitness Over Generations")
    axes[0].set_xlabel("Generation")
    axes[0].set_ylabel("Fitness Score")
    axes[0].legend()

    # Chart 2: Rule count shrinking
    axes[1].plot(generations, avg_rules, color="orange")
    axes[1].set_title("Avg Rule Count Over Generations")
    axes[1].set_xlabel("Generation")
    axes[1].set_ylabel("Number of Rules")

    # Chart 3: Real accuracy stored directly in history
    best_accuracy = [h["best_accuracy"] for h in history]
    axes[2].plot(generations, best_accuracy, color="purple")
    axes[2].set_ylim(0, 1.05)
    axes[2].set_title("Best Accuracy Over Generations")
    axes[2].set_xlabel("Generation")
    axes[2].set_ylabel("Accuracy")

    plt.tight_layout()
    plt.show()