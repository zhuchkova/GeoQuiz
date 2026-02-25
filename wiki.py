from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia
import time

def get_wikipedia_summary(title):
    """
    Returns (first_paragraph, url) or (None, None) if unavailable.
    """
    try:
        page = wikipedia.page(title, auto_suggest=False)
        summary = page.summary.split("\n")[0]
        return summary, page.url

    except wikipedia.DisambiguationError:
        print(f"(Wikipedia ambiguous page for '{title}')")
        return None, None

    except wikipedia.PageError:
        print(f"(Wikipedia page not found for '{title}')")
        return None, None

    except Exception as e:
        print(f"(Wikipedia error for '{title}': {e})")
        return None, None


def get_country_city_data(qid, data="population", lang="en"):
    """Returns the given metric (capital, population, area) for the country with the given QID"""

    # Add a delay to avoid rate limiting issue
    time.sleep(0.5)  # Wait 0.5 seconds before next request

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    if data == "capital":
        metric = "capitalLabel"
        query_where = f"wd:{qid} wdt:P36 ?capital ."
        select_vars = "?capitalLabel"
    elif data == "population":
        metric = data
        query_where = f"wd:{qid} wdt:P1082 ?population ."
        select_vars = "?population"
    elif data == "area":
        metric = data
        query_where = f"wd:{qid} wdt:P2046 ?area ."
        select_vars = "?area"
    else:
        return None

    our_query = f"""
    SELECT {select_vars} WHERE {{
      {query_where}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{lang}". }}
    }}
    LIMIT 1
    """

    sparql.setQuery(our_query)

    # Handel the expection for rate limit errors
    try:
        res = sparql.query().convert()
    except Exception as e:
        # If we get a rate limit error or any other error, return None
        print(f"Warning: Could not fetch data from Wikidata (rate limit or error). {e}")
        return None


    bindings = res.get("results", {}).get("bindings", [])
    if not bindings:
        return None

    row = bindings[0]
    return row.get(metric, {}).get("value")

def map_countries_to_qids(country_names, lang="en"):
    """Returns a dictionary mapping country names to their QIDs"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    def lang_lit(s):
        # escape for SPARQL string literal
        s = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{s}"@{lang}'

    values = " ".join(f"({lang_lit(name)})" for name in country_names)

    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?inputLabel ?country WHERE {{
      VALUES (?inputLabel) {{ {values} }}
      ?country rdfs:label ?inputLabel .
      ?country wdt:P31 wd:Q3624078 .  # sovereign state
    }}
    """

    sparql.setQuery(query)
    rows = sparql.query().convert()["results"]["bindings"]

    countries_with_quids = {name: None for name in country_names}
    for r in rows:
        name = r["inputLabel"]["value"]  # e.g., "France"
        qid = r["country"]["value"].rsplit("/", 1)[-1]
        countries_with_quids[name] = qid

    return countries_with_quids

def map_cities_to_qids(cities, lang="en"):
    """Returns a dictionary mapping city names to their QIDs"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    cities_with_qids = {}

    for city in cities:
        query = f"""
        SELECT ?city ?population WHERE {{
          ?city rdfs:label "{city}"@{lang} .
          ?city wdt:P31/wdt:P279* wd:Q486972 .  # human settlement
          OPTIONAL {{ ?city wdt:P1082 ?population . }}
        }}
        ORDER BY DESC(?population)
        LIMIT 1
        """

        sparql.setQuery(query)
        rows = sparql.query().convert()["results"]["bindings"]

        if not rows:
            cities_with_qids[city] = None
            continue

        qid = rows[0]["city"]["value"].rsplit("/", 1)[-1]
        cities_with_qids[city] = qid

    return cities_with_qids


def main():
    print(get_wikipedia_summary("Berlin"))
    print(get_country_city_data("Q142", "capital"))
    print(get_country_city_data("Q142", "population"))
    print(get_country_city_data("Q142", "area"))
    print(map_countries_to_qids(["France", "Germany", "Spain"]))
    print(map_cities_to_qids(["Paris", "Berlin", "Moscow"]))

if __name__ == "__main__":
    main()

