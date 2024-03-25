# lol

import numpy_financial as npf
from datetime import datetime

def calculate_yield(settlement, maturity, rate, pr, redemption, frequency, basis=0):
    # Convert settlement and maturity dates to datetime objects
    settlement_date = datetime.strptime(settlement, "%m/%d/%Y")
    maturity_date = datetime.strptime(maturity, "%m/%d/%Y")
    
    # Calculate time to maturity in years
    time_to_maturity = (maturity_date - settlement_date).days / 365.0
    
    # Convert annual coupon rate to periodic rate
    periodic_rate = rate / frequency
    
    # Calculate yield using numpy_financial's rate function
    yield_value = npf.rate(nper=time_to_maturity*frequency,
                           pmt=periodic_rate*redemption,
                           pv=-pr,
                           fv=redemption,
                           when='end',
                           guess=0.1,
                           tol=1e-6,
                           maxiter=1000)
    
    # Convert yield to percentage
    yield_percentage = yield_value * 100
    
    return yield_percentage

# Example usage:
settlement = "1/1/2024"
maturity = "1/1/2030"
rate = 0.05
pr = 95
redemption = 100
frequency = 2
basis = 0

yield_percentage = calculate_yield(settlement, maturity, rate, pr, redemption, frequency, basis)
print("Yield percentage:", yield_percentage)



import pandas as pd

# Sample DataFrame with bond information
data = {
    'Settlement': ["1/1/2024", "2/1/2024"],
    'Maturity': ["1/1/2030", "2/1/2030"],
    'Rate': [0.05, 0.06],
    'Pr': [95, 97],
    'Redemption': [100, 100],
    'Frequency': [2, 2],
    'Basis': [0, 0]
}

df = pd.DataFrame(data)

# Function to calculate yield and apply it to DataFrame
def calculate_yield_row(row):
    return calculate_yield(row['Settlement'], row['Maturity'], row['Rate'], row['Pr'], row['Redemption'], row['Frequency'], row['Basis'])

df['Yield'] = df.apply(calculate_yield_row, axis=1)

print(df)
