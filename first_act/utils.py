import pandas as pd

# 1
def load_and_calc_data(filepath):
    df = pd.read_csv(filepath)
    df = diff_calc(df)
    df = z_score_calc(df)
    return df

# 2
def diff_calc(df):
    df['diff_yesterday'] = df['today'] - df['yesterday']
    df['diff_same_day_last_week'] = df['today'] - df['same_day_last_week']
    df['diff_avg_last_week'] = df['today'] - df['avg_last_week']
    df['diff_avg_last_month'] = df['today'] - df['avg_last_month']
    return df

# 3
def z_score_calc(df):
    df['z_score_yesterday'] = (df['diff_yesterday'] - df['diff_yesterday'].mean()) / df['diff_yesterday'].std()
    df['z_score_same_day_last_week'] = (df['diff_same_day_last_week'] - df['diff_same_day_last_week'].mean()) / df['diff_same_day_last_week'].std()
    df['z_score_avg_last_week'] = (df['diff_avg_last_week'] - df['diff_avg_last_week'].mean()) / df['diff_avg_last_week'].std()
    df['z_score_avg_last_month'] = (df['diff_avg_last_month'] - df['diff_avg_last_month'].mean()) / df['diff_avg_last_month'].std()
    return df

# 4
def detect_anomalies(df, threshold=2):
    anomalies = df[(df['z_score_yesterday'].abs() > threshold) |
                   (df['z_score_same_day_last_week'].abs() > threshold) |
                   (df['z_score_avg_last_week'].abs() > threshold) |
                   (df['z_score_avg_last_month'].abs() > threshold)]
    return anomalies

# 5
def plot_anomalies(df, anomalies, title):
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(14, 7))
    plt.plot(df['time'], df['today'], label='Today', marker='o')
    plt.plot(df['time'], df['yesterday'], label='Yesterday', linestyle='--')
    plt.plot(df['time'], df['same_day_last_week'], label='Same Day Last Week', linestyle='--')
    plt.plot(df['time'], df['avg_last_week'], label='Average Last Week', linestyle='--')
    plt.plot(df['time'], df['avg_last_month'], label='Average Last Month', linestyle='--')
    plt.scatter(anomalies['time'], anomalies['today'], color='red', label='Anomalies', zorder=5)
    plt.title(title)
    plt.xlabel('Hour')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

# 6
def plot_query_anomalies(df, anomalies, title):
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(14, 7))
    plt.plot(df['time'], df['today'], label='Today', marker='o')
    plt.plot(df['time'], df['avg_last_month'], label='Average Last Month', linestyle='--')
    plt.scatter(anomalies['time'], anomalies['today'], color='red', label='Anomalies', zorder=5)
    plt.title(title)
    plt.xlabel('Hour')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()