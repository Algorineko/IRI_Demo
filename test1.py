import iri2016
import numpy as np

s = iri2016.IRI("2020-12-31T00", (100, 1000, 10), 80, 120)
x = s['ne'].to_numpy()

print(x[0])