import sys
from bs4 import BeautifulSoup
import pandas as pd

def scrape_individual_speechwire(year, event, conference, level, level_input):
    print(f"Speechwire Individual Results will be scraped! Year: {year}; Event: {event}; Conference: {conference}; Level: {level}; Level_input: {level_input}")

def scrape_team_speechwire(year, event, conference, level, level_input):
    print(f"Speechwire Team Results will be scraped! Year: {year}; Event: {event}; Conference: {conference}; Level: {level}; Level_input: {level_input}")

# def get_speechwire_url(year, event, conference, level, level_input):
#     """
#     Creates the URL for speechwire

#     Args:
#         event: String that has the name of the event
#         conference: 1-6 for 1A-6A
#         district_number: "" if not district
#         region_number: "" if not region
#         state_number: "0" if not state; "1" otherwise
#         year: 2023, 2024, or 2025

#     Returns: 
#         String: The full url for the speechwire page
#     """

#     def event_code(e):
#         match e:
#             case "Journalism team results": 
#                 return -3
#             case "Speech team results": 
#                 return -2
#             case "Overall school sweepstakes": 
#                 return -1
#             case "Accounting": 
#                 return 1
#             case "Computer Applications": 
#                 return 2
#             case "Current Issues and Events": 
#                 return 3
#             case "Literary Criticism": 
#                 return 4
#             case "Ready Writing": 
#                 return 5
#             case "Social Studies": 
#                 return 6
#             case "Spelling": 
#                 return 7
#             case "Calculator Applications": 
#                 return 8
#             case "Computer Science": 
#                 return 9
#             case "Mathematics": 
#                 return 10
#             case "Number Sense": 
#                 return 11
#             case "Science": 
#                 return 12
#             case "Copy Editing": 
#                 return 13
#             case "Editorial": 
#                 return 14
#             case "Feature Writing": 
#                 return 15
#             case "Headline Writing": 
#                 return 16
#             case "News Writing": 
#                 return 17
#             case "Informative Speaking": 
#                 return 18
#             case "Persuasive Speaking": 
#                 return 19
#             case "Lincoln Douglas Debate": 
#                 return 20
#             case "Poetry Interpretation": 
#                 return 21
#             case "Prose Interpretation": 
#                 return 22
#             case _: 
#                 raise ValueError(f"Unknown event name: {event}")
            
#     def year_code(y):
#         match y:
#             case 2025: 
#                 return 17
#             case 2024:
#                 return 16
#             case 2023:
#                 return 15
#             case _: 
#                 raise ValueError(f"Unsupported year: {y}")

#     base = "https://postings.speechwire.com/r-uil-academics.php?Submit=View+postings"
#     e_code = event_code(event)
#     y_code = year_code(year)

#     district_number = level_input if level == "district" else ""
#     region_number = level_input if level == "region" else ""
#     state_number = level_input if level == "state" else ""
#     return base + "&groupingid=" + str(e_code) + "&seasonid=" + str(y_code) + "&conference=" + str(conference) + "&district=" + str(district_number) + "&region=" + str(region_number) + "&state=" + str(state_number)

# # URL and headers
# try:
#     year = sys.argv[1]
#     event = sys.argv[2]
#     conference = sys.argv[3]
#     level = sys.argv[4]
#     level_input = sys.argv[5]
    
# except IndexError:
#     print("IndexError: no parameters given in the command line for the type of competition")
#     raise

# url = get_speechwire_url(year, event, conference, level, level_input)
# print("Scraping from URL: " + url)

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# # Fetch the page
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "lxml")

# # Find all tables
# tables = soup.find_all("table")

# # Creating Individual Table
# individual_table_data = []
# individual_table = tables[5]
# individual_table_rows = individual_table.find_all("tr")
# individual_table_headers = [header.get_text(strip=True) for header in individual_table_rows[0].find_all('td')]

# for row in individual_table_rows[1:]:  # Skip the header row
#     columns = row.find_all('td')
#     individual_table_data.append([col.get_text(strip=True) for col in columns])

# # Creating Team Table
# team_table_data = []
# team_table = tables[6]
# team_table_rows = team_table.find_all("tr")
# team_table_headers = [header.get_text(strip=True) for header in team_table_rows[0].find_all('td')]

# for row in team_table_rows[1:]:  # Skip the header row
#     columns = row.find_all('td')

#     # Split the 'School' column (columns[1]) by <br> tag
#     school_column = columns[1]

#     # Parse the inner HTML of the school cell
#     school_soup = BeautifulSoup(school_column.decode_contents(), 'html.parser')

#     # Split into parts using .stripped_strings to handle both the text and <br> nicely
#     school_parts = list(school_soup.stripped_strings)

#     # Ensure exactly 5 parts: 1 school + 4 students
#     school_parts = school_parts[:5] + [''] * (5 - len(school_parts))

#     # Combine with other columns
#     row_data = [columns[0].get_text(strip=True)] + school_parts + [col.get_text(strip=True) for col in columns[2:]]

#     # Add to list
#     team_table_data.append(row_data)

# # Creates new team table headers to include members of the team
# new_team_table_headers = []
# for header in team_table_headers:
#     new_team_table_headers.append(header)
#     if header == "School":
#         new_team_table_headers.extend(["Entry 1", "Entry 2", "Entry 3", "Entry 4"])

# # Create Data Frames for both tables
# df_individual_table = pd.DataFrame(individual_table_data, columns=individual_table_headers)
# df_team_table = pd.DataFrame(team_table_data, columns=new_team_table_headers)

# # Save tables as CSV Files
# df_individual_table.to_csv("data/individual_results.csv", index=False)
# print("CSV saved: data/individual_results.csv")

# df_team_table.to_csv("data/team_results.csv", index=False)
# print("CSV saved: data/team_results.csv")


# print("Individual Table:")
# print(df_individual_table)
# print("\nTeam Table:")
# print(df_team_table)