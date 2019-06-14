import numpy
import csv
import pathlib
import re
from math import log10 as log

import pyolin.utils as utils
from pyolin.csvdata import CSVMedians

gate_prefixes = {"af" : "1201",
                 "standard" : "1717",
                 "input" : "1818",
                 "pTac" : "1818"}

with open("../gates.csv") as f:
    for name in CSVMedians(f).names:
        gate_prefixes[name] = name

def csv_paths(name, xs=None):
    data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
    prefix = gate_prefixes[name]
    if xs is None:
        paths = data_dir.glob(prefix + "_*.csv")
        return [(x_from_path(p), p) for p in paths]
    else:
        return list(map(lambda x: (x, csv_path(name, x)), xs))

def csv_path(name, x):
    data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
    prefix = gate_prefixes[name]
    return (x, list(data_dir.glob(prefix + "_" + str(x) + "_*.csv"))[0])

def x_from_path(path):
    filename = path.name
    regex_match = re.match(r"(.*_)(\d+)(.*\.csv)", filename)
    return int(regex_match.group(2))

def input_rpu():
    data = csv_paths("input")
    channel = [csv_channel(p, channel=channel) for _, p in data]
    channel = numpy.concatenate(channel)

def median_af(channel="B1-A"):
    data = csv_paths("af")
    channel = [csv_channel(p, channel=channel) for _, p in data]
    channel = numpy.concatenate(channel)
    return numpy.median(channel)

def median_standard(channel="B1-A"):
    data = csv_paths("standard")
    channel = [csv_channel(p, channel=channel) for _, p in data]
    channel = numpy.concatenate(channel)
    return numpy.median(channel)

def csv_channel(path, channel="B1-A"):
    with path.open() as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        cols = next(reader)
        col_index = cols.index(channel)
        channel_data = list(map(lambda r: float(r[col_index]), reader))
        return numpy.array(channel_data)

def median(path, channel="B1-A"):
        channel_data = csv_channel(path, channel=channel)
        return numpy.median(channel_data)

def rpu_median(path, channel="B1-A"):
        channel_data = csv_channel(path, channel=channel)
        af = median_af()
        st = median_standard()
        au = numpy.median(channel_data)

        return utils.au_to_rpu(au, af, st)

def au_histogram(path,
              channel="B1-A",
              num_bins=100,
              bin_min=None,
              bin_max=None):

        channel_data = csv_channel(path, channel=channel)
        if bin_min is None:
            bin_min = min(channel_data)
        if bin_max is None:
            bin_max = max(channel_data)

        bins = numpy.logspace(log(bin_min), log(bin_max), num=num_bins)
        return numpy.histogram(channel_data, bins=bins, density=True)

def rpu_histogram(path,
              channel="B1-A",
              num_bins=100,
              bin_min=None,
              bin_max=None):

        channel_data = csv_channel(path, channel=channel)
        af = median_af()
        st = median_standard()
        au = numpy.median(channel_data)
        constant = utils.c(au, af, st)
        channel_data = channel_data * constant

        if bin_min is None:
            bin_min = min(channel_data)
        if bin_max is None:
            bin_max = max(channel_data)

        bins = numpy.logspace(log(bin_min), log(bin_max), num=num_bins)
        return numpy.histogram(channel_data, bins=bins, density=True)
