import datetime
import requests
from bs4 import BeautifulSoup

cards = {}
dashes = '------' + '\n'


def parse_html(html):
    with requests.get(html, allow_redirects=True) as site:
        soup = BeautifulSoup(site.text, "html.parser")
        tables = soup.find_all('table')
        for all_cards in tables:
            # check all headers for full card list
            first_header = all_cards.find_next('th')
            second_header = first_header.find_next('th')
            if first_header.text == "Color" and second_header.text == "Card":
                for card in first_header.find_all_next('tr'):
                    # color
                    first_data_value = card.find_next('td').text
                    # card
                    second_data_value = card.find_next('td').next_sibling.next_sibling.text
                    if first_data_value in cards.keys():
                        cards[first_data_value].append(second_data_value)
                    else:
                        cards[first_data_value] = [second_data_value]


def write_sorted_by_type(file_name):
    with open(file_name, 'w') as f:
        f.write('MTGO Vintage Cube - Type Sorted' + '\n')
        f.write('Generated on: ' + datetime.datetime.now().strftime('%B %d %Y') + '\n')
        keys = list(sorted(cards.keys()))
        last_key = keys[-1]
        first_key = keys[0]
        for key in keys:
            if key != first_key:
                f.write('\n' + dashes + key + '\n' + dashes)
            else:
                f.write(dashes + key + '\n' + dashes)
            sorted_cards = list(sorted(map(lambda x: x + '\n', cards[key])))
            if key == last_key:
                sorted_cards[len(sorted_cards)-1] = sorted_cards[len(sorted_cards)-1].rstrip('\n')
            f.writelines(sorted_cards)


def write_full_alphabetical(file_name):
    with open(file_name, 'w') as f:
        all_cards = []
        f.write('MTGO Vintage Cube' + '\n')
        f.write('Generated on: ' + datetime.datetime.now().strftime('%B %d %Y') + '\n')
        f.write(dashes)
        for key in cards:
            for card in cards[key]:
                all_cards.append(card + '\n')
        all_cards.sort()
        all_cards[len(all_cards)-1] = all_cards[len(all_cards)-1].rstrip('\n')
        f.writelines(all_cards)


parse_html('https://www.mtgo.com/vintage-cube-cardlist')
write_full_alphabetical('no_type_sorting.txt')
write_sorted_by_type('type_sorted.txt')
