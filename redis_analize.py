import redis
import sys
import pandas

client = redis.Redis(host='redis', port=6379)

keys = client.keys('*')

df = pandas.DataFrame({
    'keys': [item.decode() for item in keys]

})

df['domain'] = df['keys'].apply(lambda x: x.split(':')[0])
df['size'] = df['keys'].apply(lambda x: sys.getsizeof(client.get(x)))
df['size'] = df['size'] / 1024 / 1024

df_by_domain = df.groupby('domain').aggregate({'size': 'sum', 'domain': 'count'})
df_by_domain.index.name = 'd'
df_by_domain = df_by_domain.rename(columns={'d': 'domain', 'domain': 'count'})

df_by_domain = df_by_domain.sort_values('size', ascending=False)

print(df_by_domain)