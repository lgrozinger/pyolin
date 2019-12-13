import pandas


class GateData:
    def __init__(self, pandas_dataframe):
        self.df = pandas_dataframe

    def __getitem__(self, key):
        if isinstance(key, slice):
            strain, backbone, cargo = key
            data = self.df[self.df.strain == strain]
            data = data[data.backbone == backbone]
            data = data[data.cargo == cargo]


def get_plasmids(df):
    return df.plasmid.drop_duplicates()[df.plasmid != 'Empty']


def get_strains(df):
    return df.strain.drop_duplicates()[df.strain != 'Empty']


def get_backbones(df):
    return df.backbone.drop_duplicates()[df.backbone != 'Empty']
