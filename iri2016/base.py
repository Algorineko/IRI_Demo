import subprocess
from dateutil.parser import parse
from datetime import datetime
from pathlib import Path
import xarray
import io
import shutil
import numpy as np
import typing

from .build import build

R = Path(__file__).resolve().parent
datadir = R / "data"
src_path = R.parent
exe_path = src_path / "build"
EXE = shutil.which("iri2016_driver", path=str(exe_path))
if not EXE:
    build("meson", src_path, exe_path)
EXE = shutil.which("iri2016_driver", path=str(exe_path))
if not EXE:
    raise ImportError("IRI2016 executable not available.")

SIMOUT = ["ne", "Tn", "Ti", "Te", "nO+", "nH+", "nHe+", "nO2+", "nNO+", "nCI", "nN+"]

__all__ = ["IRI"]


def IRI(time: datetime, altkmrange: typing.Sequence[float], glat: float, glon: float) -> xarray.Dataset:

    if isinstance(time, str):
        time = parse(time)

    assert len(altkmrange) == 3, "altitude (km) min, max, step"
    assert isinstance(glat, float) and isinstance(glon, float), "glat, glon is scalar"

    cmd = [
        str(EXE),
        str(time.year),
        str(time.month),
        str(time.day),
        str(time.hour),
        str(time.minute),
        str(time.second),
        str(glat),
        str(glon),
        str(altkmrange[0]),
        str(altkmrange[1]),
        str(altkmrange[2]),
        str(datadir),
    ]

    ret = subprocess.check_output(cmd, universal_newlines=True, cwd=str(exe_path))  # str for Windows
    # %% get altitude profile data
    Nalt = int((altkmrange[1] - altkmrange[0]) // altkmrange[2]) + 1

    arr = np.genfromtxt(io.StringIO(ret), max_rows=Nalt)
    arr = np.atleast_2d(arr)
    assert arr.ndim == 2 and arr.shape[1] == 12, "bad text data output format"

    dsf = {k: (("alt_km"), v) for (k, v) in zip(SIMOUT, arr[:, 1:].T)}
    altkm = arr[:, 0]
    # %% get parameter data
    arr = np.genfromtxt(io.StringIO(ret), skip_header=Nalt)
    assert arr.ndim == 1 and arr.size == 100, "bad text data output format"
    # %% assemble output
    iono = xarray.Dataset(
        dsf, coords={"time": [time], "alt_km": altkm, "glat": glat, "glon": glon}, attrs={"f107": arr[40], "ap": arr[51]}
    )

    for i, p in enumerate(["NmF2", "hmF2", "NmF1", "hmF1", "NmE", "hmE"]):
        iono[p] = (("time"), [arr[i]])

    iono["TEC"] = (("time"), [arr[36]])
    iono["EqVertIonDrift"] = (("time"), [arr[43]])

    return iono
