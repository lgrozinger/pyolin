import pandas
import os
from tkinter import *
from tkinter import filedialog


root = Tk()
root.withdraw()
yourdir = filedialog.askdirectory(title = "Select Measurement folder")
usedir=yourdir

file_list[0]

file_list=os.listdir(usedir):
pandas.read_csv(usedir+"/"+file_list[0],index=false)

df_list=[]
for file in file_list:
    df=pandas.read_csv(usedir+"/"+file,header=None,names=["iptg","median_yfp"])
    df["filename"]=file
    df_list.append(df)

df1=pandas.read_csv(usedir+"/"+file_list[0],header=None,index_col=0)
df1.insert[]
df_list = [pandas.read_csv(usedir+"/"+file,header=None,index_col=0) for file in file_list]

["new"]=file
df_list
df_list[0]['new'] = "test"
big_df = pandas.concat(df_list)

big_df["strain"]=big_df.filename.str.extract(r"op_(.*?)_")
big_df["backbone"]=big_df.filename.str.extract(r"_.*?_(.*?)_")
big_df["plasmid"]=big_df.filename.str.extract(r"_.*?_.*?_(.*)?\.")
big_df
