import openvsp as vsp
import random
from datetime import datetime
from time import perf_counter


SECTION_LIMIT = 0.85
SPAN_LIMIT = (0.085, 0.765)
TIP_CHORD_LIMITS = (0.18, 0.2)
SWEEP_LOC_LIMITS = (0, 0.4)
MACH_SPEED = [0.029]


def initialize_population(n):
    if n%2 != 0:
        n += 1
        print("adding another extra element because the population size is odd")

    population = []
    for _ in range(n):
        # Generation random elements
        population.append(
            {
                'span': round(random.uniform(SPAN_LIMIT[0], SPAN_LIMIT[1]), 2),
                'tip_chord': round(random.uniform(TIP_CHORD_LIMITS[0], TIP_CHORD_LIMITS[1]), 2),
                'sweep_loc': round(random.uniform(SWEEP_LOC_LIMITS[0], SWEEP_LOC_LIMITS[1]), 2)
            }
        )
    return population

population = initialize_population(int(input("how many elements should be started for evolution?\n>")))

ITERATOR_LIMITER = int(input("how many iterations you wish to do?\n>"))
TOP_N_SCORES = int(input("Enter the number of top scoring wings to keep:\n>"))
CURRENT_DATETIME = datetime.now().strftime("%d%m%Y_%H_%M_%S")

log = open(f"{CURRENT_DATETIME}.txt", "w")


def show_population(population):
    for i, element in enumerate(population):
        print(f"element {i} = span: {element['span']},"
              f" tip_chord: {element['tip_chord']}, sweep_loc: {element['sweep_loc']}")


def mutate(element):
    # Introduce slight variations to the parameters
    mutated_element = {
        'span': element['span'] + (element['span'] * random.uniform(-0.05, 0.05)),
        'tip_chord': element['tip_chord'] + (element['tip_chord'] * random.uniform(-0.05, 0.05)),
        'sweep_loc': element['sweep_loc'] + (element['sweep_loc'] * random.uniform(-0.05, 0.05))
    }

    # Ensure parameters are within the specified ranges
    mutated_element['span'] = max(min(mutated_element['span'], SPAN_LIMIT[1]), SPAN_LIMIT[0])
    mutated_element['tip_chord'] = max(min(mutated_element['tip_chord'], TIP_CHORD_LIMITS[1]), TIP_CHORD_LIMITS[0])
    mutated_element['sweep_loc'] = max(min(mutated_element['sweep_loc'], SWEEP_LOC_LIMITS[1]), SWEEP_LOC_LIMITS[0])

    return mutated_element


def wing_modifier(span, tip_c, sweep_loc, save=False):
    # Loading wing
    vsp.ClearVSPModel()
    vsp.ReadVSPFile("AsaMista.vsp3")
    wing_geom = vsp.FindGeoms()[0]

    vsp.SetParmVal(wing_geom, "Span", "XSec_1", span)
    vsp.SetParmVal(wing_geom, "Span", "XSec_2", 0.85-span)
    vsp.SetParmVal(wing_geom, "Tip_Chord", "XSec_2", tip_c)
    vsp.SetParmVal(wing_geom, "Sweep_Location", "XSec_2", sweep_loc)
    vsp.Update()

    if save:
        # When you've got a winner, it saves the winner .vsp3 model
        vsp.WriteVSPFile("test_wing.vsp3", vsp.SET_ALL)


def get_score(element):

    # Modify the wing and run the analysis
    wing_modifier(element["span"], element["tip_chord"], element["sweep_loc"])

    vsp.DeleteAllResults()
    comp_geom = "VSPAEROComputeGeometry"
    vsp.SetAnalysisInputDefaults(comp_geom)
    comp_geom_results = vsp.ExecAnalysis(comp_geom)

    analysis_name = "VSPAEROSweep"
    vsp.SetIntAnalysisInput(comp_geom, "AnalysisMethod", (1, vsp.VORTEX_LATTICE))
    vsp.SetDoubleAnalysisInput(analysis_name, "MachStart", MACH_SPEED, 0)
    vsp.SetDoubleAnalysisInput(analysis_name, "AlphaEnd", [1.00], 0)

    # EExecuting the Analysis while logging the analysis time
    start_time = perf_counter()
    vsp.ExecAnalysis(analysis_name)
    end_time = perf_counter()
    log.write(f"Simulation time {end_time - start_time}")

    point_id = vsp.FindResultsID("point")
    polar_id = vsp.FindResultsID("VSPAERO_Polar")

    # Calculate the score
    cl = vsp.GetDoubleResults(polar_id, "CL", 0)
    l_d = vsp.GetDoubleResults(polar_id, "CL", 0)
    area = vsp.GetDoubleResults(point_id, "area", 0)
    scores = [(cl_value * l_d_value) / area[0] for cl_value, l_d_value in zip(cl, l_d)]
    final_score = sum(scores) / len(scores)

    return final_score


best_scores = []

# How to get the wing score:


for iteration in range(ITERATOR_LIMITER):
    # Compute scores for the population
    scores = [(get_score(element), element) for element in population]

    # Sort scores by score
    scores.sort(key=lambda x: x[0], reverse=True)
    # print(scores)

    # Select the top-performing elements
    selected_elements = [elem for _, elem in scores[:(len(population)//2)]]
    # print(selected_elements)

    # Extract and store scores for the selected elements
    selected_scores = [score for score, _ in scores[:(len(population)//2)]]
    # print(selected_scores)

    best_scores = list(zip(selected_scores, selected_elements))
    # print(best_scores)
    # input()
    if iteration == ITERATOR_LIMITER-1:
        # skipping the natural loop end to avoid the list constructors below
        # which will be slow when there are a lot of elements
        continue

    # Apply mutation to create new elements
    new_elements = [mutate(element) for element in selected_elements]

    # Replace worst-scoring elements
    population = selected_elements + new_elements

if len(best_scores) <= TOP_N_SCORES:
    while len(best_scores) != TOP_N_SCORES:
        best_scores.append((0.000, {
                'span': 0.000,
                'tip_chord': 0.000,
                'sweep_loc': 0.000
            }))
else:
    best_scores = best_scores[:TOP_N_SCORES]

# Extract parameters for the winner
winner_params = [param for param in best_scores[0][1].values()]
wing_modifier(winner_params[0], winner_params[1], winner_params[2], True)

file = open("results.txt", "w")
# Print the top N parameters and scores
for i, (score, params) in enumerate(best_scores):
    print(f"\nWing n{i+1}:\nscore: {score:.6e}\nspan: {params['span']:.4f}; tip_chord: {params['tip_chord']:.4f}; "
          f"sweep_loc {params['sweep_loc']:.4f}\n")
    file.write(f"Rank {i + 1}:\n\nScore: {score}\nParameters: {params}\n\n\n")
file.close()
log.close()


# print(best_scores)

# Vai Corinthians