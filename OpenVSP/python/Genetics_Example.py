"""
    This function is for illustration of the workings of a genetic algorithm.

    The central idea is to iterate a comparative process, reproducing objects with the best
    performance introducing a random variation and stopping the loop when a
    satisfying performance is achieved.
"""

import random
import plotly.express as px
from math import log, floor, ceil


def genetic_selection(population_size, background_color, max_iterations):
    """
  Implements a genetic selection process for color individuals.

  Args:
    population_size: The number of individuals in the population.
    background_color: The background color against which individuals are compared.
    max_iterations: The maximum number of iterations to run the algorithm.

  Returns:
    A list of final individuals and the number of iterations taken.
  """

    # Initialize population and variations
    population = [random.randint(0, 255) for _ in range(population_size)]
    variations = [abs(individual - background_color) for individual in population]

    # Initialize lists for storing data across iterations
    iterations = []
    less_than_10_count = []
    mean_survivor_colors = []

    for iteration in range(max_iterations):
        # Kill half with highest variation
        sorted_variations = sorted(enumerate(variations), key=lambda x: x[1], reverse=True)
        death_line = floor(population_size * 0.5)
        survivors = [population[i] for i, _ in sorted_variations[death_line:]]
        variations = [variations[i] for i, _ in sorted_variations[death_line:]]

        # Create new individuals and update variations
        new_individuals = []
        new_variations = []

        for survivor in survivors:
            # New genetics (mutation) algorithm
            variation = random.uniform(-0.01, 0.01) * 255
            new_individual = survivor + variation
            new_individual = min(255, max(0, new_individual))  # enforcing the color to stay withing the range
            new_individuals.append(new_individual)
            new_variations.append(abs(new_individual - background_color))

        # Update population and variations
        population = survivors + new_individuals
        variations = variations + new_variations

        # Count individuals with variation < 10
        less_than_10 = sum(variation < 10 for variation in variations)

        # Store data for later plotting
        iterations.append(iteration + 1)
        less_than_10_count.append(less_than_10)

        # Check for stopping condition
        mean_survivor_color = sum(survivors) / len(survivors)
        mean_survivor_colors.append(mean_survivor_color)

        # Check for stopping condition
        if less_than_10 / population_size >= 0.9:
            # Plotting script
            fig_mean_survivor_color = px.line(
                x=iterations,
                y=mean_survivor_colors,
                labels={"x": "Iteration", "y": "Mean Survivor Color"},
                title="Mean Survivor Color by Iteration"
            )
            fig_mean_survivor_color.add_scatter(
                x=iterations,
                y=less_than_10_count,
                mode="lines",
                yaxis="y2",  # Associate with the right y-axis
                name="Less than 10 Count",
            )
            fig_mean_survivor_color.update_layout(
                yaxis2=dict(
                    title="Less than 10 Count",
                    overlaying='y',
                    side='right'
                )
            )
            fig_mean_survivor_color.show()

            # Plot more compact histogram
            fig_survivor_color = px.histogram(
                x=survivors,
                nbins=ceil(log(len(survivors), 2)) + 1,
                labels={"x": "Survivor Color", "y": "Number of Survivors"},
                title="Survivor Color Distribution"
            )
            fig_survivor_color.show()
            break
    return population, iterations[-1]


# Example usage
population_size = 200
background_color = 128
max_iterations = 1000
final_population, iterations = genetic_selection(population_size, background_color, max_iterations)

print(f"Final population: {final_population}")
print(f"Iterations to reach 90% with variation < 10: {iterations}")
