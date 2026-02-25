from list_of_cities import major_cities_short
from list_of_countries import allowed_countries_short
from wiki import map_cities_to_qids, map_countries_to_qids
import json

def main():
    """Get dictionaries of mapped countries and cities to their Q ids"""

    #####Cities##########
    # cities_dict = map_cities_to_qids(major_cities_short)
    # print(cities_dict)
    # with open("cities.json", "w", encoding="utf-8") as f:
    #     json.dump(cities_dict, f, ensure_ascii=False, indent=2)

    #####Countries##########
    countries_dict = map_countries_to_qids(allowed_countries_short)
    print(countries_dict)
    with open("countries.json", "w", encoding="utf-8") as f:
        json.dump(countries_dict, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()