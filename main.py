# This will not run on online IDE
import requests
from bs4 import BeautifulSoup
import webbrowser
import concurrent.futures

ANIMAL_NAME = 'Animal Name'
COLLATERAL_ADEJECTIVE = 'Collateral Adjective'
RESULTS_FILENAME = 'animal_results.html'
HTML_HEAD_PART = '<html><meta charset='"Windows-1252"'><head><title>Title</title></head>'
HTML_BODY_TABLE = '<body><h2>Wikipedia animal scraping</h2><table>'
HTML_ENDING = '</table></body></html>'
HTML_TR_TD = '<tr><td>'
HTML_TD_TR = '</td></tr>'
HTML_TD_TD = '</td><td>'


def process_scrape(url):
    try:

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')

        # Looking for the second table with the classes 'wikitable' and 'sortable'
        table = soup.find_all("table", {"class": "wikitable sortable"})[-1]

        animals = []

        # Collecting data
        for row in table.tbody.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')

            if columns:
                animal = {ANIMAL_NAME: columns[0].text.strip(), COLLATERAL_ADEJECTIVE: columns[5].text.strip()}
                animals.append(animal)

        save_results(animals)

        return animals

    except BaseException as e:  # work on python 3.x
        print('Exception - ' + str(e))


def save_results(animals):
    html_template = HTML_HEAD_PART
    html_template += HTML_BODY_TABLE

    for animal in animals:
        html_template += f'{HTML_TR_TD}{ANIMAL_NAME} - {animal[ANIMAL_NAME]}{HTML_TD_TD}{COLLATERAL_ADEJECTIVE} - {HTML_TD_TD}{animal[COLLATERAL_ADEJECTIVE]}{HTML_TD_TR}'

    html_template += HTML_ENDING

    f = open(RESULTS_FILENAME, 'w')
    # writing the code into the file
    f.write(html_template)

    # close the file
    f.close()


def load_results():
    webbrowser.open(RESULTS_FILENAME)



###########################################################

def run_scrape_returns_value(url):

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(process_scrape, url)
        return_value = future.result()
        print(return_value)


###########################################################
# Normal OK flow
###########################################################
main_url = 'https://en.wikipedia.org/wiki/List_of_animal_names'
run_scrape_returns_value(main_url)


###########################################################
# 1) test bad url
###########################################################
#bad_url = 'https://en.wikipedia.org/wiki/List_of_animal_names111'
#run_scrape_returns_value(bad_url)


###########################################################
# 2) test no internet connection, manually disable network adapter
###########################################################
#main_url = 'https://en.wikipedia.org/wiki/List_of_animal_names'
#run_scrape_returns_value(main_url)






