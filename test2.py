import numpy as np
import iri2016

nlons = 40
nlats = 40

ALT_min = 60
ALT_max = 100
nALT = 30

ALT_step = (100 - 60) / (30 - 1)

LON = np.linspace(-180,180,nlons)
LAT = np.linspace(-90,90,nlats)
ALT = np.linspace(ALT_min, ALT_max, nALT)

GLON0, GLAT0 = np.meshgrid(LON, LAT)

GLON, GLAT, GALT = np.meshgrid(LON, LAT, ALT)
Ne = np.zeros((np.shape(GLON)))
for i in range(nlons):
    for j in range(nlats):
        temp = iri2016.IRI('2016-9-27-18T', [ALT_min, ALT_max, ALT_step], GLAT0[i, j], GLON0[i, j])
Ne[i, j, :] = temp.ne