import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nba_region_and_teams(url):

    # Set display options for wider columns
    pd.set_option('display.max_colwidth', None)  # Show full column width without truncation

    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    
    # Find all division titles (teams are likely nested under these)
    divisions = soup.find_all(class_="NavTeamList_ntlDivision__lJFro")
    
    main_dict = {}
    team_names = []
    region_names = [] 
    profile_links = []
    logos = []
    
    # Iterate through each division and extract team names
    for div in divisions:
        # Get the teams under this division
        region = div.div.string
        teams = div.find_all("a", class_ = "Anchor_anchor__cSc3P NavTeamList_ntlTeam__9K_aX")  # Assuming teams are links under the division title

        for team in teams:

            # Team Name
            team_names.append(team['data-text'])  # Extract team name and clean it

            # Region
            region_names.append(region)
            
            # Logo Source
            div = team.find('div')
            img = div.find('img') if div else None
            if img:
                full_url = img.get('src')
                logos.append(full_url)

            # Profile Link
            team_anchor = soup.find('a', text=team['data-text'])
            if team_anchor:
                team_div = team_anchor.find_parent('div', class_='TeamFigure_tfContent__Vxiyh')
                
                # Now find the "Profile" link within this div
                profile_link = team_div.find('a', text="Profile")['href']
                profile_links.append('https://www.nba.com' + profile_link)

            # Coach info
            

        main_dict['Team Name'] = team_names
        main_dict['Region'] = region_names
        main_dict['Logo Source'] = logos
        main_dict['Profile Link'] = profile_links

    return main_dict

def create_df(main_dictionary):

    df = pd.DataFrame(main_dictionary)

    return df



# URL of the NBA teams page
url = "https://www.nba.com/teams"
main_dict = scrape_nba_region_and_teams(url)
data = create_df(main_dict)
print(data)

