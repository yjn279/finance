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


for per in itertools.product(range(101), repeat=3):

    if sum(per) != 100:
        continue

    portfolio = PortFolio(symbols, per, path)
    returns = sum(portfolio.returns())
    risks = portfolio.risks()
    var = portfolio.var(risks)

    with open(path + '/portfolio3.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(per + (returns, var))

    print(per)