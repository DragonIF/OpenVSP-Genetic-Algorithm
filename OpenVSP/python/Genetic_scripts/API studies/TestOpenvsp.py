# import charm.input_automation as charm
# import utilities.units as uu
import openvsp as vsp
import numpy as np

import os
import math

# Changed to "True" because I ran it twice and the second time it threw an error b/c it couldn't write the file.  Just a
# preference for this testing.
overwrite_files = True

wing = vsp.AddGeom("WING", "")
vsp.SetGeomName(wing, "ASA_DO_FEFE")

# vsp.InsertXSec(wing, 1, vsp.XS_UNDEFINED)

# for section in range(0, 2):
#     xsec_surf = vsp.GetXSecSurf(wing, section)
#     vsp.ChangeXSecShape(xsec_surf, section, vsp.XS_FILE_AIRFOIL)
#     xsec = vsp.GetXSec(xsec_surf, section)
#     vsp.ReadFileAirfoil(xsec, "../airfoil/I_ICH10_E423_1223_75.dat")
#     vsp.Update()

vsp.Update()

file_name = "apitest1.vsp3"

vsp.WriteVSPFile(file_name)

vsp_prop_name = "Prop"

