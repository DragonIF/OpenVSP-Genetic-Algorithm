import openvsp as vsp

vsp.ReadVSPFile("AsaMista.vsp3")
wing_geom = vsp.FindGeoms()[0]

containers = vsp.FindContainers()
wing_container = ''

for container in containers:
    container_name = vsp.GetContainerName(container)
    if container_name == "WingGeom":
        print(f"Container name = {container_name}")
        wing_container = container
        break

wing_param_ids = vsp.FindContainerParmIDs(wing_container)
for id in wing_param_ids:
    print(vsp.GetParmName(id))
