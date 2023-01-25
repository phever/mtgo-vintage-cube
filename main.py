import datetime
import os
import requests
from bs4 import BeautifulSoup

cards = {}


def parse_html(html):
    with requests.get(html, allow_redirects=True) as site:
        soup = BeautifulSoup(site.text, "html.parser")
        tables = soup.find_all('table')
        for all_cards in tables:
            # check all headers for full card list
            first_header = all_cards.findNext('th')
            if first_header.text == "Card Name":
                for card in first_header.findAllNext('tr'):
                    new_card = card.findNext('td').text
                    new_card_type = card.findNext('td').next_sibling.next_sibling.text
                    if new_card_type in cards.keys():
                        cards[new_card_type].append(new_card)
                    else:
                        cards[new_card_type] = [new_card]


def write_sorted_by_type(file_name):
    dashes = '------' + os.linesep
    with open(file_name, 'w') as f:
        f.write('MTGO Vintage Cube - Type Sorted' + os.linesep)
        f.write('Generated on: ' + datetime.datetime.now().strftime('%B %d %Y') + os.linesep)
        keys = list(cards.keys())
        last_key = keys[-1]
        first_key = keys[0]
        for key in cards:
            if key != first_key:
                f.write(os.linesep + dashes + key + os.linesep + dashes)
            else:
                f.write(dashes + key + os.linesep + dashes)
            sorted_cards = list(sorted(map(lambda x: x + os.linesep, cards[key])))
            if key == last_key:
                sorted_cards[len(sorted_cards)-1] = sorted_cards[len(sorted_cards)-1].rstrip(os.linesep)
            f.writelines(sorted_cards)


def write_full_alphabetical(file_name):
    with open(file_name, 'w') as f:
        all_cards = []
        f.write('MTGO Vintage Cube' + os.linesep)
        f.write('Generated on: ' + datetime.datetime.now().strftime('%B %d %Y') + os.linesep)
        f.write('------' + os.linesep)
        for key in cards:
            for card in cards[key]:
                all_cards.append(card + os.linesep)
        all_cards.sort()
        all_cards[len(all_cards)-1] = all_cards[len(all_cards)-1].rstrip(os.linesep)
        f.writelines(all_cards)


parse_html('https://www.mtgo.com/vintage-cube-cardlist')
write_full_alphabetical('no_type_sorting.txt')
write_sorted_by_type('type_sorted.txt')
