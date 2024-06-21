import pandas as pd
import sqlite3
from utils import load_and_calc_data, plot_query_anomalies

# 11
checkout1 = load_and_calc_data('first_act/checkout_1.csv')
checkout2 = load_and_calc_data('first_act/checkout_2.csv')

# 12
conn = sqlite3.connect('sales_data.db')
checkout1.to_sql('checkout1', conn, if_exists='replace', index=False)
checkout2.to_sql('checkout2', conn, if_exists='replace', index=False)
conn.commit()

# 13
query1 = '''
SELECT time, today, z_score_yesterday, z_score_same_day_last_week, z_score_avg_last_week, z_score_avg_last_month
FROM checkout1
WHERE ABS(z_score_avg_last_month) > 2
'''

query2 = '''
SELECT time, today, z_score_yesterday, z_score_same_day_last_week, z_score_avg_last_week, z_score_avg_last_month
FROM checkout2
WHERE ABS(z_score_avg_last_month) > 2
'''

# 14
anomalies1 = pd.read_sql_query(query1, conn)
anomalies2 = pd.read_sql_query(query2, conn)

# 15
conn.close()

# 16
plot_query_anomalies(checkout1, anomalies1, 'Sales Comparison: Today vs. Average Last Month with Anomalies (checkout_1)')
plot_query_anomalies(checkout2, anomalies2, 'Sales Comparison: Today vs. Average Last Month with Anomalies (checkout_2)')

# 17
print("Anomalies in checkout_1.csv")
print(anomalies1)
print("\nAnomalies in checkout_2.csv")
print(anomalies2)
