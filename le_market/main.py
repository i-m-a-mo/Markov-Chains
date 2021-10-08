
import pandas as pd
import numpy as np

from SupermarketClasses import Supermarket, Customer

probs = pd.read_csv('probs.csv', index_col=0)
time_ppl = pd.read_csv('time_ppl.csv', index_col='timestamp')
spawn = pd.read_csv('spawn.csv', index_col=0)

#print(spawn)

#c1 = Customer('Bob', spawn['location'], probs)

edeka = Supermarket(spawn['location'], time_ppl, probs)
#edeka = Supermarket(spawn['location'], time_ppl, probs)

#edeka.customers
#edeka.go_shopping(100)
#edeka.customers_recording
