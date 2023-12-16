import openvsp as vsp

# Creating a wing from scratch
wing = vsp.AddGeom("WING", "")
vsp.SetGeomName(wing, "AsaDoFe")
vsp.SetParmVal(wing, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)


# Section to illustrate some parameterizing functions.
vsp.SetDriverGroup(wing, 1, vsp.SPAN_WSECT_DRIVER, vsp.TAPER_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER)
vsp.SetParmVal(wing, "SectTess_U", "XSec_1", 20)
vsp.SetParmVal(wing, "Span", "XSec_1", 63.63)
vsp.SetParmVal(wing, "Taper", "XSec_1", 0.45)
vsp.SetParmVal(wing, "Root_Chord", "XSec_1", 16.672)
vsp.SetParmVal(wing, "Sweep", "XSec_1", 45.0)
vsp.SetParmVal(wing, "Sweep_Location", "XSec_1", 0.25)
vsp.Update()


# Airfoil Section
NUM_OF_SECTIONS: int = 2  # Input for the amount of section your wing has.

for section in range(0, NUM_OF_SECTIONS):
    xsec_surf = vsp.GetXSecSurf(wing, section)
    vsp.ChangeXSecShape(xsec_surf, section, vsp.XS_FILE_AIRFOIL)
    xsec = vsp.GetXSec(xsec_surf, section)
    vsp.ReadFileAirfoil(xsec, "../airfoil/I_ICH10_E423_1223_75.dat")

# Extremely important! save your changes before computational or high hierarchical processes.
vsp.Update()

# Wing File Saving
vsp.WriteVSPFile("fefezin.vsp3", vsp.SET_ALL)
vsp.ClearVSPModel()
vsp.ReadVSPFile("AsaMista.vsp3")  # Opening a more featured wing file

# Needless to say you need to create a simulation mesh body before trying to simulate this
# If you get file read errors, this may be the cause... >:0
comp_geom = "VSPAEROComputeGeometry"
vsp.SetAnalysisInputDefaults(comp_geom)
vsp.SetIntAnalysisInput(comp_geom, "AnalysisMethod", (1, vsp.VORTEX_LATTICE))

# Executing Analysis
comp_geom_results = vsp.ExecAnalysis(comp_geom)

# Now I'll list every simulation mode available
for analysis in vsp.ListAnalysis():
    print(analysis)

analysis_name = "VSPAEROSweep"  # From the printed list, choose a suitable mode.
# help(vsp.SetIntAnalysisInput)  # The API has poor documentation :(
mach_speed = [0.029]  # Monkey unit mach is used on the software, so you need to convert
# your units or use a ready to go one

vsp.PrintAnalysisInputs(analysis_name)  # This will list the current state of your simulation parameters
# it also list all parameter possibilities to copy and paste on the following functions
vsp.SetDoubleAnalysisInput(analysis_name, "MachStart", mach_speed, 0)  # The analysis parameters are easy to work with
vsp.SetDoubleAnalysisInput(analysis_name, "AlphaEnd", [1.00], 0)

# analysis_method = vsp.GetIntAnalysisInput(analysis_name, "AnalysisMethod")
# analysis_method = [vsp.VSPAERO_ANALYSIS_METHOD.VORTEX_LATTICE]
# print(analysis_method)
input()

# Executing test and exporting to a csv
test = vsp.ExecAnalysis(analysis_name)
vsp.WriteResultsCSVFile(test, "FefeRes.csv")

# The API has nice functions to work with the analysis data, so it's worth checking it out

