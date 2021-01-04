import csv
import json
import itertools
import requests
import numpy as np
import sympy as sym
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from scipy import stats
from bs4 import BeautifulSoup


path = '/content/drive/MyDrive/assets/historical data'
symbols = ['VT', 'BND', 'GLD']

df = pd.read_csv(path + '/portfolio3.csv', header=None)

df = df[[3, 4]].values
plt.scatter(df[4], df[3], c=df[2], cmap='plasma')
plt.colorbar()
plt.show()