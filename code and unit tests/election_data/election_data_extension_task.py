import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r"data\US-2016-primary.csv"
df = pd.read_csv(file_path, sep=';')

candidate_A = 'Hillary Clinton'
candidate_B = 'Bernie Sanders'

# Filter, group by state, and calculate the mean vote fraction
df_comparison = df[df['candidate'].isin([candidate_A, candidate_B])]
comparison_data = df_comparison.groupby(['state_abbreviation', 'candidate'])[
    'fraction_votes'].mean().unstack()

# Plot the comparison
plt.figure(figsize=(15, 7))
comparison_data.plot(kind='bar', ax=plt.gca(), alpha=0.8)
plt.title(f'Average Vote Fraction by State: {candidate_A} vs. {candidate_B}', fontsize=16)
plt.xlabel('State Abbreviation', fontsize=12)
plt.ylabel('Average Fraction of Votes', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Candidate')
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.savefig('clinton_sanders_vote_comparison_bar_chart.png')
