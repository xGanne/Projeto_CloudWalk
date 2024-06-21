import pandas as pd

# 1
def detect_anomalies(transactions, threshold=2):
    transactions['time'] = pd.to_datetime(transactions['time'])
    stats = transactions.groupby(transactions['time'].dt.floor('min')).agg(
        total_transactions=('count', 'sum'),
        failed=('failed', 'sum'),
        reversed=('reversed', 'sum'),
        denied=('denied', 'sum')
    )

    stats['z_score_failed'] = (stats['failed'] - stats['failed'].mean()) / stats['failed'].std()
    stats['z_score_reversed'] = (stats['reversed'] - stats['reversed'].mean()) / stats['reversed'].std()
    stats['z_score_denied'] = (stats['denied'] - stats['denied'].mean()) / stats['denied'].std()

    anomalies = stats[(stats['z_score_failed'].abs() > threshold) |
                      (stats['z_score_reversed'].abs() > threshold) |
                      (stats['z_score_denied'].abs() > threshold)]

    return anomalies
