import pandas as pd
import matplotlib.pyplot as plt

#load the Data
file_path = r"data\US-2016-primary.csv"
df = pd.read_csv(file_path, sep=';')

#Filter and Plot
candidate_1 = 'Donald Trump'
df_candidate_1 = df[df['candidate'] == candidate_1]

plt.figure(figsize=(10, 6))
df_candidate_1['fraction_votes'].plot(
    kind='hist', 
    bins=20, 
    edgecolor='black', 
    alpha=0.7, 
    title=f'Distribution of Vote Fraction for {candidate_1}',
    xlabel='Fraction of Votes (0.0 to 1.0)',
    ylabel='Number of Counties')
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.savefig('donald_trump_vote_fraction_histogram.png')
plt.show()
print("done")