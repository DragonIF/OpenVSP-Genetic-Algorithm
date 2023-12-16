"""
This one illustrates the process of modifying a wing, which will be used on the final algorithm.
"""

import  openvsp as vsp

vsp.ReadVSPFile("AsaMista.vsp3")
geoms = vsp.FindGeoms()

vsp.SetGeomName(geoms[0], "asinha_de_flango")
# vsp.GetParm(geoms[0], "TotalSpan", )

container = vsp.FindContainerParmIDs(geoms[0])

# for id in container:
#     print(f"{vsp.GetParmDisplayGroupName(id)}: {id}")

xsec_surf = vsp.GetXSecSurf(geoms[0], 0)
xsec = vsp.GetXSec(xsec_surf, vsp.GetNumXSec(xsec_surf) - 1)
print(vsp.GetXSecParm(xsec, "Span"))

# vsp.SetParmVal(geoms[0], "Total_Span", 20.0 )
vsp.SetParmVal(geoms[0], "Span", "XSec_2", 0.16)
vsp.SetParmVal(geoms[0], "Span", "XSec_1", 0.8)

# Once again, working with the API is a pain
sec_ids = vsp.GetXSecParmIDs(xsec)

print("All geoms in Vehicle.")
print(geoms)


# for section in range(0, 2):
#     xsec_surf = vsp.GetXSecSurf(wing, section)
#     vsp.ChangeXSecShape(xsec_surf, section, vsp.XS_FILE_AIRFOIL)
#     xsec = vsp.GetXSec(xsec_surf, section)
#     vsp.ReadFileAirfoil(xsec, "../airfoil/I_ICH10_E423_1223_75.dat")
#     vsp.Update()


vsp.WriteVSPFile("test.vsp3", vsp.SET_ALL)
vsp.ClearVSPModel()