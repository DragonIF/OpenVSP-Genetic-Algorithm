import openvsp as vsp
import random

ITERATOR_LIMITER = int(input("how many iterations you wish to do?\n>"))
TOP_N_SCORES = int(input("Enter the number of top scores to keep:\n>"))

SECTION_LIMIT = 0.85
TIP_CHORD_LIMITS = (0.18, 0.2)
SWEEP_LOC_LIMITS = (0, 0.4)

MACH_SPEED = [0.029]


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


best_scores = []

# How to get the wing score:

for iteration in range(ITERATOR_LIMITER):
    # Generate random parameters within the specified limits
    span = random.uniform(*(0.085, 0.765))
    tip_c = random.uniform(*TIP_CHORD_LIMITS)
    sweep_loc = random.uniform(*SWEEP_LOC_LIMITS)

    # Truncate parameters to 0.01
    span, tip_c, sweep_loc = round(span, 2), round(tip_c, 2), round(sweep_loc, 2)

    # Modify the wing and run the analysis
    wing_modifier(span, tip_c, sweep_loc)

    vsp.DeleteAllResults()
    comp_geom = "VSPAEROComputeGeometry"
    vsp.SetAnalysisInputDefaults(comp_geom)
    comp_geom_results = vsp.ExecAnalysis(comp_geom)

    analysis_name = "VSPAEROSweep"
    vsp.SetIntAnalysisInput(comp_geom, "AnalysisMethod", (1, vsp.VORTEX_LATTICE))
    vsp.SetDoubleAnalysisInput(analysis_name, "MachStart", MACH_SPEED, 0)
    vsp.SetDoubleAnalysisInput(analysis_name, "AlphaEnd", [1.00], 0)
    vsp.ExecAnalysis(analysis_name)

    point_id = vsp.FindResultsID("point")
    polar_id = vsp.FindResultsID("VSPAERO_Polar")

    # Calculate the score
    cl = vsp.GetDoubleResults(polar_id, "CL", 0)
    l_d = vsp.GetDoubleResults(polar_id, "CL", 0)
    area = vsp.GetDoubleResults(point_id, "area", 0)
    scores = [(cl_value * l_d_value) / area[0] for cl_value, l_d_value in zip(cl, l_d)]
    final_score = sum(scores) / len(scores)

    # Add the current parameters and score to the list
    best_scores.append((final_score, (span, tip_c, sweep_loc)))

    # Sort the list by score and keep only the top N scores
    best_scores = sorted(best_scores, key=lambda x: x[0], reverse=True)[:TOP_N_SCORES]


winner_params = best_scores[0][-1]
wing_modifier(winner_params[0], winner_params[1], winner_params[2], True)


# Print the top N parameters and scores
for i, (score, params) in enumerate(best_scores):
    print(f"Rank {i + 1}: Parameters {params} | Score {score}")

# print(best_scores)

# Vai Corinthians