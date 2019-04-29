import csv
import matplotlib.pyplot as plt

class CSVMedians:

    def __init__(self, stream, xaxis="RPU", yaxis="RPU"):
        self._stream = stream
        self._x = xaxis
        self._y = yaxis

    def plotgate(self, gatename):
        figure, axes = plt.subplots()
        axes.set_xlabel(xaxis)
        axes.set_ylabel(yaxis)
        axes.set_title(gatename)
        return plt.show(plt.plot(self.xs, self[gatename]))

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError("Provide gate name as a string.")
        else:
            match = [row[1:] for row in self.reader if row[0] == key]
            if len(match) == 0:
                raise KeyError("No such gate {} in CSV file.".format(key))
            elif len(match) > 1:
                raise Exception("CSV file contains duplicate duplicate row names.")
            else:
                return [float(y) for y in  match[0]]

    def __contains__(self, item):
        match = [row[1:] for row in self.reader if row[0] == item]
        return len(match) > 0

    @property
    def reader(self):
        self._stream.seek(0)
        return csv.reader(self._stream, delimiter=',', quotechar='"')

    @property
    def filename(self):
        return self._filename

    @property
    def names(self):
        return [row[0] for row in self.reader][1:]

    @property
    def xs(self):
        return self["xs"]
