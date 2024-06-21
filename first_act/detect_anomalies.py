import pandas as pd
from utils import load_and_calc_data, detect_anomalies, plot_anomalies

# 7
checkout1 = load_and_calc_data('first_act/checkout_1.csv')
checkout2 = load_and_calc_data('first_act/checkout_2.csv')

# 8
anomalies1 = detect_anomalies(checkout1)
anomalies2 = detect_anomalies(checkout2)

# 9
print("Anomalies in checkout_1.csv")
print(anomalies1)
print("\nAnomalies in checkout_2.csv")
print(anomalies2)

# 10
plot_anomalies(checkout1, anomalies1, 'Anomalies in checkout_1.csv')
plot_anomalies(checkout2, anomalies2, 'Anomalies in checkout_2.csv')
