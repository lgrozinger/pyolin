import numpy
import csv
import pathlib

gate_prefixes = {"af" : "1201",
                 "standard" : "1717"}

def csv_paths(name, xs=None):
    ucf_dir = pathlib.Path(__file__).resolve().parent.parent / "ucf"
    prefix = gate_prefixes[name]
    if xs is None:
        return ucf_dir.glob(prefix + "_*.csv")
    else:
        return map(lambda x: csv_path(name, x), xs)

def csv_path(name, x):
    ucf_dir = pathlib.Path(__file__).resolve().parent.parent / "ucf"
    prefix = gate_prefixes[name]
    return list(ucf_dir.glob(prefix + "_" + str(x) + "_*.csv"))[0]

def median(path, column="B1-A :: GFP-A"):
    with path.open() as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        cols = next(reader)
        col_index = cols.index(column)
        channel_data = list(map(lambda r: float(r[col_index]), reader))
        channel_data = numpy.array(channel_data)
        return numpy.median(channel_data)
