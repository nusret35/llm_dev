import re

input_string = "1. Fig. 1. Relationships among perceived usability, perceived aesthetics, and user preference based on previous studies’ findings - This image is important because it illustrates the framework that links RM process mechanisms to firm performance during economic contractions and expansions, which includes the three key relationship tenets: communication openness, technical involvement, and customer value anticipation."

pattern = re.compile(r'^\d\.\s+(.*?)\s+-\s+(.*)$')

match = pattern.match(input_string)

if match:
    title = match.group(1).strip()
    explanation = match.group(2).strip()
    print("Title:", title)
    print("Explanation:", explanation)
else:
    print("No match found.")