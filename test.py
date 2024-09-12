import numpy as np
import pandas as pd
from matplotlib import pyplot as pl
import numpy


def paint(x, y, label=None):
    pl.figure(label=label)
    pl.pie(x, labels=y, autopct='%1.1f%%')
    pl.show()


def x_y(dat, label=None):
    ind = list(i < list(dat)[0] / 3 for i in list(dat)).index(True)
    y = list(dat.index)[:ind]
    y.append('other')
    x = list(dat)[:ind]
    x.append(sum(list(dat)[ind:]))
    paint(x, y, label)


f = 'train.xlsx'
dat = pd.read_excel(f)
dat = dat.sort_values(by='Order Date')
MaxDate = dat['Order Date'].max()
# Задание 1.а
dat_1_a = dat['Sub-Category'].value_counts()
x_y(dat_1_a)
# Задание 1.б
dat_1_b = dat[dat['Order Date'] > (MaxDate - pd.DateOffset(years=2))]
dat_1_b = dat_1_b['Sub-Category'].value_counts()
x_y(dat_1_b)
# Задание 1.в
dat_1_c = dat[dat['Order Date'] > (MaxDate - pd.DateOffset(years=1))]
dat_1_c = dat_1_c['Sub-Category'].value_counts()
x_y(dat_1_c)
# Задание 2
average = dat['Sales'].mean()
s = 0
for i in list(dat['Sales']):
    s += (i - average) ** 2
s = (s / len(list(dat['Sales']))) ** (1 / 2)
dat_2 = dat[(dat['Sales'] > average - 3 * s) & (dat['Sales'] < average + 3 * s)]
dat_2['Sales'].plot(kind='box')
pl.show()
quan = dat_2['Sales'].quantile([0.25, 0.5, 0.75])
print(quan)
print(((dat['Sales'].max() - dat['Sales'].min()) / 3 + dat['Sales'].min()),
      (2 * (dat['Sales'].max() - dat['Sales'].min()) / 3 + dat['Sales'].min()))
# Задание 3
conditions = [
    (dat['Sales'] < (dat['Sales'].max() - dat['Sales'].min()) / 3 + dat['Sales'].min()),
    ((dat['Sales'] > (dat['Sales'].max() - dat['Sales'].min()) / 3 + dat['Sales'].min()) & (
                dat['Sales'] < 2 * (dat['Sales'].max() - dat['Sales'].min()) / 3 + dat['Sales'].min())),
    (dat['Sales'] > 2 * (dat['Sales'].max() - dat['Sales'].min()) / 3 + dat['Sales'].min())
]
choices = ['small', 'medium', 'big']
dat['Sale_group'] = np.select(conditions, choices)
groups = dat.groupby(['Region', 'Sale_group'])
y = []
x_buy = []
x_sale = []
for name, group in groups:
    y.append(' '.join(name))
    x_buy.append(len(group))
    x_sale.append(sum(list(group['Sales'])))
    x_y(group['Sub-Category'].value_counts(), ' '.join(name))
paint(x_buy, y)
paint(x_sale, y)
