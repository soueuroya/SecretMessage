import requests
from bs4 import BeautifulSoup


DEFAULT_URL = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"


def print_secret_message_from_url(url: str):
    #print("Using URL: ", url)

    try:
        response = requests.get(url)
        #print("Status code:", response.status_code)
    except Exception as e:
        print("Request failed: ", e)
        return

    if response.status_code != 200:
        print("Failed to fetch document - Check URL?")
        return

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr") # looking for rows in the page, this finds all rows even fi there are multiple tables.
    #print("Rows: ", len(rows))

    if not rows:
        print("No table rows found - Check URL?")
        return

    points = []

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) != 3: # check if the row has 3 colmuns. If not, skip it.
            continue

        try: # if any of the values in the cells doesnt match the coordenates structure, skip it.
            x = int(cols[0].get_text(strip=True))
            char = cols[1].get_text(strip=True)
            y = int(cols[2].get_text(strip=True))
        except:
            continue

        points.append((x, y, char)) #if not skipped, add the values to the points list

    #print("Points: ", len(points))

    if not points: #if points list is empty, terminate
        print("No valid data parsed - Check page?")
        return
	
    #p[0] = x / p[1] = y / p[2] = char
    max_x = max(p[0] for p in points) # max coordenate X (columns) is the furtherst x position in the list
    max_y = max(p[1] for p in points) # max coordenate Y (rows) is the furthest y position in the list

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)] # create empty grid

    for x, y, char in points: # for each point, submit the character at the correct grid position
        grid[max_y - y][x] = char # max_y - y fixes the Y orientation of the grid (flips vertically)

    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    user_input = input("Paste your Google Doc URL (or press Enter to use default): ").strip()

    url = user_input
    
    if user_input:
        print_secret_message_from_url(url)
    else:
        print_secret_message_from_url(DEFAULT_URL)

    input("\nPress Enter to exit...")