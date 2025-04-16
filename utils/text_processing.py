import re

def extract_weekly_content(syllabus_text):
    # Regex to match "Week X" sections and content that follows
    week_pattern = r"(Week \d+)(.*?)(?=Week \d+|$)"
    weeks = re.findall(week_pattern, syllabus_text, flags=re.DOTALL)

    weekly_data = {}

    # Check if weekly content was populated properly
    if not weeks:
        print("No weekly content extracted. Please check the syllabus text.")
    else:
        print(f"Weekly content extracted: {weeks}")  # For debugging purposes
    
    for week_header, week_content in weeks:
        # Extract specific details like assignments, midterm, and readings
        assignments = re.findall(r"\*\*Assignment [\d]+\*\*:([^\n]+)", week_content)
        midterm = re.search(r"\*\*Midterm Exam\*\*: (Scheduled for Week \d+ \(\w+ \d+\))", week_content)
        readings = re.findall(r"Readings: ([^*]+)", week_content)

        # Store each piece of extracted data in a dictionary
        week_info = {
            "assignments": assignments,
            "midterm": midterm.group(1) if midterm else None,
            "readings": readings
        }

        weekly_data[week_header] = week_info

    return weekly_data
