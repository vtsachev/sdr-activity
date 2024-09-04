import csv
from collections import defaultdict
from datetime import datetime

def analyze_data(file_path):
    daily_metrics = defaultdict(lambda: {"new_contacts": 0, "emails_sent": 0, "responses_received": 0})
    sequences = defaultdict(lambda: {"sent": 0, "replies": 0})
    stages = defaultdict(int)
    total_emails = 0
    total_responses = 0

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sent_at = row['Sent At (PST)']
            try:
                date = datetime.strptime(sent_at, '%B %d, %Y %H:%M').date()
            except ValueError:
                print(f"Error parsing date: {sent_at}")
                continue
            
            print(f"Processing row: Date = {date}, To Email = {row['To Email']}, From Email = {row['From Email']}")
            
            # Daily metrics
            daily_metrics[date]['emails_sent'] += 1
            if row['From Email'] == 'ryan@trunk.io':
                total_emails += 1
                if not row['Sequence']:  # Assuming new contacts don't have a sequence
                    daily_metrics[date]['new_contacts'] += 1
            if row['Replied'] == 'true':
                daily_metrics[date]['responses_received'] += 1
                total_responses += 1

            # Sequence performance
            if row['Sequence']:
                sequences[row['Sequence']]['sent'] += 1
                if row['Replied'] == 'true':
                    sequences[row['Sequence']]['replies'] += 1

            # Contact stages
            stages[row['Contact Stage']] += 1

    print("\nDaily Metrics:")
    for date, metrics in daily_metrics.items():
        print(f"{date}: {metrics}")

    return {
        'daily_metrics': dict(daily_metrics),
        'sequences': dict(sequences),
        'stages': dict(stages),
        'total_emails': total_emails,
        'total_responses': total_responses,
        'reply_rate': (total_responses / total_emails) * 100 if total_emails > 0 else 0
    }

# Usage
results = analyze_data('week of 8.26.24.apollo-messages-export.csv')
print("\nFinal Results:")
print(results)
