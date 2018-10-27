import requests
from bs4 import BeautifulSoup


class PlayerInfos():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    urls = [
        "https://www.transfermarkt.ch/david-von-ballmoos/profil/spieler/203124",
        "https://www.transfermarkt.ch/marco-wolfli/profil/spieler/4860",
        "https://www.transfermarkt.ch/mohamed-camara/profil/spieler/426723",
        "https://www.transfermarkt.ch/steve-von-bergen/profil/spieler/4793",
        "https://www.transfermarkt.ch/leonardo-bertone/profil/spieler/194975",
        "https://www.transfermarkt.ch/miralem-sulejmani/profil/spieler/36080",
        "https://www.transfermarkt.ch/djibril-sow/profil/spieler/212723",
        "https://www.transfermarkt.ch/nicolas-moumi-ngamaleu/profil/spieler/266768",
        "https://www.transfermarkt.ch/christian-fassnacht/profil/spieler/250490",
        "https://www.transfermarkt.ch/roger-assale/profil/spieler/263183",
        "https://www.transfermarkt.ch/jean-pierre-nsame/profil/spieler/225055",
        "https://www.transfermarkt.ch/thorsten-schick/profil/spieler/55574",
        "https://www.transfermarkt.ch/michel-aebischer/profil/spieler/237658",
        "https://www.transfermarkt.ch/ulisses-garcia/profil/spieler/192616",
        "https://www.transfermarkt.ch/gregory-wuthrich/profil/spieler/203125",
        "https://www.transfermarkt.ch/loris-benito/profil/spieler/119085",
        "https://www.transfermarkt.ch/jan-kronig/profil/spieler/346881",
        "https://www.transfermarkt.ch/david-von-ballmoos/profil/spieler/203124",
        "https://www.transfermarkt.ch/pedro-teixeira/profil/spieler/433189",
        "https://www.transfermarkt.ch/jordan-lotomba/profil/spieler/313094",
        "https://www.transfermarkt.ch/sandro-lauper/profil/spieler/254965",
        "https://www.transfermarkt.ch/sekou-sanogo/profil/spieler/173656",
        "https://www.transfermarkt.ch/leo-seydoux/profil/spieler/313097",
        "https://www.transfermarkt.ch/dario-marzino/profil/spieler/254968",
        "https://www.transfermarkt.ch/kevin-mbabu/profil/spieler/183321",
        "https://www.transfermarkt.ch/guillaume-hoarau/profil/spieler/23934",
    ]

    @classmethod
    def get_player_infos(cls):
        players = []
        for url in cls.urls:
            player_info = cls.__get_player_info(url)
            players.append(player_info)
        return players

    @classmethod
    def __get_player_info(cls, url):
        page_tree = requests.get(url, headers=cls.headers)
        page_soup = BeautifulSoup(page_tree.content, 'html.parser')
        player_data_table = page_soup.find("div", {"class": "spielerdaten"}).find("table", {"class": "auflistung"}).find_all("td")

        player_name = page_soup.find_all("h1", {"itemprop": "name"})[0].text
        player_jersy_number = page_soup.find_all("span", {"class": "dataRN"})[0].text[1:]
        player_image_url = page_soup.find_all("div", {"class": "dataBild"})[0].find("img")["src"]
        player_birthday = player_data_table[0].text.strip()
        player_birthplace = player_data_table[1].text.replace("\n", "").replace("\xa0", "").strip()
        player_age = player_data_table[2].text
        player_height = player_data_table[3].text.replace("\xa0", "")
        player_nationality = player_data_table[4].text.replace("\n", "").replace("\xa0", "").replace("\t", "")
        player_position = player_data_table[5].text.replace("\r", "").replace("\n", "").replace("\t", "")
        player_foot = player_data_table[6].text
        player_in_team_since = player_data_table[9].text.replace("\r", "").replace("\n", "").replace("\t", "")
        player_contract_until = player_data_table[10].text

        player_infos = {
            'name': player_name,
            'jerseyNumber': player_jersy_number,
            'imageUrl': player_image_url,
            'birthday': player_birthday,
            'birthplace': player_birthplace,
            'age': player_age,
            'height': player_height,
            'nationality': player_nationality,
            'position': player_position,
            'foot': player_foot,
            'inTeamSince': player_in_team_since,
            'contractUntil': player_contract_until
        }

        return player_infos
