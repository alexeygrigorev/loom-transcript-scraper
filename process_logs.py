import re
import pandas as pd

def parse_loom_logs(log_text):
    # Regular expressions to match the Loom ID and title
    loom_id_pattern = r"https://www\.loom\.com/share/([a-f0-9]+)"
    title_pattern = r"Current page title: (.+)"

    # Find all matches in the log text
    loom_ids = re.findall(loom_id_pattern, log_text)
    titles = re.findall(title_pattern, log_text)

    # Combine the results into a dictionary
    results = {
        'Loom ID': loom_ids,
        'Title': titles
    }

    return results

# Read logs from file
try:
    with open('logs.txt', 'r', encoding='utf-8') as file:
        log_text = file.read()
except FileNotFoundError:
    print("Error: 'logs.txt' file not found.")
    exit(1)
except IOError:
    print("Error: Unable to read 'logs.txt' file.")
    exit(1)

# Parse the logs
results = parse_loom_logs(log_text)

# Create a pandas DataFrame
df = pd.DataFrame(results)

# Write results to CSV
try:
    df.to_csv('titles.csv', index=False)
    print("Results have been written to 'titles.csv'")
except IOError:
    print("Error: Unable to write to 'titles.csv' file.")
    exit(1)

# Optional: Print results to console
print(df.head())