import datetime
import re
import os
import json

# Define the custom start date for Week 1
start_date = datetime.date(2025, 7, 30)
today = datetime.date.today()

# Calculate the number of days since the start date
days_since_start = (today - start_date).days

# Determine the current week number based on the custom start date
current_week = days_since_start // 7 + 1

# Stop checking after Week 16
if current_week > 16:
    print("🎉 Your Python learning journey is complete! You've reached the end of Week 16.")
else:
    # Read the README.md file
    with open("README.md", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract week entries from the markdown table
    week_entries = []
    for line in lines:
        match = re.match(r"\|\s*Week\s*(\d+)\s*\|\s*\[(.*?)\]\((.*?)\)", line)
        if match:
            week_number = int(match.group(1))
            topic = match.group(2)
            link = match.group(3)
            week_entries.append((week_number, topic, link))

    # Find the topic for the current week
    selected_week = None
    for week_number, topic, link in week_entries:
        if week_number == current_week:
            selected_week = (week_number, topic, link)
            break

    # Load progress.json
    progress_file = "progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            progress = json.load(f)
    else:
        progress = {}

    # Determine notebook filename
    notebook_filename = f"Python_Learning_Week{current_week}.ipynb"
    notebook_updated = False
    if os.path.exists(notebook_filename):
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(notebook_filename)).date()
        if (today - modified_time).days <= 7:
            notebook_updated = True
            progress[f"Week {current_week}"] = "complete"
    else:
        notebook_updated = False

    # Save updated progress
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)

    # Print the result
    if selected_week:
        print(f"📘 Week {selected_week[0]}: {selected_week[1]}")
        print(f"🔗 Link: {selected_week[2]}")
        status = progress.get(f"Week {current_week}", "incomplete")
        if notebook_updated:
            print(f"✅ Status: {status} (automatically marked based on recent notebook update)")
        else:
            print(f"✅ Status: {status} (notebook file not found or not updated recently)")
    else:
        print(f"No topic found for custom week {current_week}.")
        print("Please check if the README.md file includes this week.")
