import os
import sys
from pathlib import Path

pkg_path = os.path.abspath(str(Path(__file__).parent.parent))
sys.path.insert(0, pkg_path)

import json
import numpy
import wquantiles
from io import StringIO
import datetime
from gate import Gate
from dataframe import GateData
import pandas
import argparse


class UCF:
    def __init__(self, **kwargs):
        if "file" in kwargs:
            io = StringIO(kwargs["file"].read())
            self.data = json.load(io)
        else:
            self.data = []

    def __str__(self):
        if not list(self.getcollections("header")):
            self.data.append(self.header)

        if not list(self.getcollections("measurement_std")):
            self.data.append(self.measurementstd)

        if not list(self.getcollections("logic_constraints")):
            self.data.append(self.logicconstraints)

        return json.dumps(self.data)

    def getcollections(self, collectionname):
        return (c for c in self.data
                if "collection" in c
                and c["collection"] == collectionname)

    def getgates(self):
        return self.getcollections("gates")

    def getgate(self, gatename):
        for gate in self.getgates():
            if gate["name"] == gatename:
                return gate

        raise KeyError(f"No such gate {gatename} in UCF")

    def addheader(self, **kwargs):
        header = {"collection": "header",
                  "date": datetime.datetime.today().strftime("%d-%m-%Y")}

        version = kwargs.get("version", "1")
        organism = kwargs.get("organism", "")
        genome = kwargs.get("genome", "")
        media = kwargs.get("media", "")
        temperature = kwargs.get("temperature", "37")
        growth = kwargs.get("growth", "")

        header["version"] = version
        header["organism"] = organism
        header["genome"] = genome
        header["media"] = media
        header["temperature"] = temperature
        header["growth"] = growth

        self.data.append(header)

    def addmeasurementstd(self, **kwargs):
        kwargs["collection"] = "measurement_std"
        self.data.append(kwargs)

    def addlogicconstraints(self, **kwargs):
        kwargs["collection"] = "logic_constraints"
        self.data.append(kwargs)

    def addgate(self, gate):
        gates = {"collection": "gates", "gate_type": "NOR", "system": "TetR"}
        gates["group_name"] = gate.repressor
        gates["gate_name"] = gate.name
        self.data.append(gates)

        gate_parts = {"collection": "gate_parts", "gate_name": gate.name}
        gate_parts["promoter"] = f"p{gate.repressor}"
        gate_parts["transcription_units"] = [[gate.rbs, gate.repressor]]
        self.data.append(gate_parts)

        response_functions = {"collection": "response_functions"}
        response_functions["gate_name"] = gate.name
        response_functions["variables"] = "x"
        response_functions["equations"] = "ymin+(ymax-ymin)/(1.0+(x/K)^n)"
        response_functions["parameters"] = [{"name": k, "value": v} for k, v in gate.params.items()]
        self.data.append(response_functions)

        rbs = {"collection": "parts", "type": "rbs", "name": gate.rbs}
        rbs["dnasequence"] = "ACTG"
        self.data.append(rbs)

        cds = {"collection": "parts", "type": "cds", "name": gate.repressor}
        cds["dnasequence"] = "ACTG"
        self.data.append(cds)

    @property
    def header(self):
        try:
            return next(self.getcollections("header"))
        except StopIteration:
            exampleucf = Path(__file__).parent.parent / "ucf" / "Eco1C1G1T1.UCF.json"
            with open(exampleucf) as eg:
                return next(UCF(file=eg).getcollections("header"))

    @property
    def measurementstd(self):
        try:
            return next(self.getcollections("measurement_std"))
        except StopIteration:
            exampleucf = Path(__file__).parent.parent / "ucf" / "Eco1C1G1T1.UCF.json"
            with open(exampleucf) as eg:
                return next(UCF(file=eg).getcollections("measurement_std"))

    @property
    def logicconstraints(self):
        try:
            return next(self.getcollections("logic_constraints"))
        except StopIteration:
            numgates = len(list(self.getgates()))
            return {"collection": "logic_constraints",
                    "available_gates": [
                        {"type": "NOR",
                         "max_instances": str(numgates)},
                        {"type": "NOT",
                         "max_instances": str(numgates)}]}


description = """
Generate a minimal UCF file, compatible with Cello, for a collection of gates.

Some metadata may be missing or incorrect, for example, sequence
data. The use of the generated UCF file is therefore restricted to the
design stage, and cannot be used for the build stage. This may be
updated in the future.  """


parser = argparse.ArgumentParser(description=description,
                                 prog="UCF file generate")
parser.add_argument("filepath", type=str, metavar="FILEPATH",
                    help="a CSV file, such as generated by FlowScatt, containing the gate data")
parser.add_argument("-o", "--outpath", type=str, nargs='?', metavar="FILEPATH",
                    help="the file path to write the UCF to. If omitted output is written to stdout",
                    default="")


if __name__ == '__main__':
    args = parser.parse_args()
    FILEPATH = args.filepath
    OUTPATH = args.outpath
    dataframe = pandas.read_csv(FILEPATH)
    dataframe = dataframe.rename(columns={'rrpu': 'decomp_flor'})
    dataframe = dataframe.rename(columns={'newstandard': 'rrpu'})
    data = GateData(dataframe)

    u = UCF()
    for gate in data:
        u.addgate(gate)

    if OUTPATH:
        with open(OUTPATH, "w") as outfile:
            outfile.write(str(u))
    else:
        print(u)
