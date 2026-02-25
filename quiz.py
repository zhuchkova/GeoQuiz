from wiki import get_wikipedia_summary, get_country_city_data
from display_with_border import *
import json
import random
import time
import difflib # for close matches

# ----------------------------
# Load data
# ----------------------------

with open("countries.json", "r", encoding="utf-8") as f:
    countries = json.load(f)

with open("cities.json", "r", encoding="utf-8") as f:
    cities = json.load(f)

# remove missing qids (None/empty) and New York giving problems
countries = {k: v for k, v in countries.items() if v}
cities = {k: v for k, v in cities.items() if v and k != "New York"}

# ----------------------------
# Helper functions
# ----------------------------

def get_random_geo(dictionary):
    """Returns a random key from the given dictionary"""
    return random.choice(list(dictionary.keys()))

def print_answer(answer, correct=True):
    """Prints the answer to the question and whether it was correct or not"""
#    print()
    if correct:
        fprint("CONGRATS!!! You are correct!", C.GREEN)
        fprint(f"The answer is '{answer}'", C.BLUE)
    else:
        fprint("Unfortunately, you are wrong...", C.RED)
        fprint(f"The correct answer is '{answer}'", C.GREEN)


def print_answer_details(metric, biggest_name, smallest_name, biggest_metric, smallest_metric, unit=None):
    """Prints details including the ratio between the two values"""
    unit_text = f" {unit}" if unit else ""
    fprint(f"\nThe {metric} of {biggest_name} is {biggest_metric}{unit_text}", C.BLUE)
    fprint(f"The {metric} of {smallest_name} is {smallest_metric}{unit_text}", C.BLUE)

    # avoid division by zero (just in case)
    if smallest_metric:
        ratio = biggest_metric / smallest_metric
        fprint(f"\nThat is {ratio:.2f} times more than {smallest_name}", C.BLUE)

def safe_int(value):
    """Convert value to int safely. Return None if missing/bad."""
    if value is None:
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Convert value to float safely. Return None if missing/bad."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def ask_ab(question_text):
    """Ask until player enters A or B (case-insensitive). Returns 'A' or 'B'."""
    while True:
        ans = cinput(question_text, C.CYAN).lower() #.strip().lower()
        if ans in ("a", "b"):
            return ans.upper()
        error("\nPlease answer with A or B.\n")

def get_additional_info_wiki(entity_1, entity_2):
    """Print summaries about the given entities from Wikipedia"""
    mult_factor = 100
    fprint("\nThere is some information for you from Wikipedia:", C.YELLOW)
    fprint(f"{'*' * mult_factor}", C.YELLOW)

    fprint(f"** {entity_1} **", C.MAGENTA)
    summary1, url1 = get_wikipedia_summary(entity_1)
    if summary1:
        fprint(summary1, C.MAGENTA)
        if url1:
            fprint(f"Read more: {url1}", C.MAGENTA)
    else:
        fprint("No summary available.", C.MAGENTA)

    fprint(f"\n{'*' * mult_factor}", C.YELLOW)

    fprint(f"** {entity_2} **", C.BLUE)
    summary2, url2 = get_wikipedia_summary(entity_2)
    if summary2:
        fprint(summary2, C.BLUE)
        if url2:
            fprint(f"Read more: {url2}", C.BLUE)
    else:
        fprint("No summary available.", C.BLUE)

    time.sleep(0.5)  # pause because sometimes there're too many requests

def is_close_match(user_input, correct_answer, threshold=0.8):
    """
    Returns True if user_input is close enough to correct_answer.
    """
    similarity = difflib.SequenceMatcher(
        None,
        user_input.lower(),
        correct_answer.lower()
    ).ratio()
    return similarity >= threshold


# ----------------------------
# Questions
# ----------------------------

def city_capital_question():
    """
    Capital question (user types capital).
    Returns (correct, points, question_text).
    Added typo detection
    """
    random_country = get_random_geo(countries)
    capital = get_country_city_data(countries[random_country], "capital")

    question_text = f"Which city is the capital of {random_country}? "

    if not capital:
        question_text = f"(Skipped) Could not find capital for {random_country}."
        cprint(question_text, C.CYAN)
        return False, 0, question_text

    user_capital = cinput(question_text).strip()

    # Exact match
    if user_capital.lower() == capital.lower():
        correct = True
        typo_note = None

    # Close match (typo)
    elif is_close_match(user_capital, capital):
        correct = True
        typo_note = f"Minor typo detected - assuming you meant '{capital}'."

    else:
        correct = False
        typo_note = None

    points = 1 if correct else 0

    frame_top()
    print_answer(capital, correct=correct)

    if typo_note:
        fprint(typo_note, C.YELLOW)

    get_additional_info_wiki(random_country, capital)
    frame_bottom()

    return correct, points, question_text


def compare_question(dictionary, metric, metric_label, unit=None, cast_func=safe_int, kind="city"):
    """
    Generic A/B question for population/area.
    - dictionary: cities or countries mapping name -> QID
    - metric: 'population' or 'area'
    - cast_func: safe_int or safe_float
    Returns (correct, points, question_text).

    If metric is missing for chosen items, it retries a few times.
    """
    tries = 0
    max_tries = 5

    while tries < max_tries:
        tries += 1

        name_1 = get_random_geo(dictionary)
        name_2 = get_random_geo(dictionary)
        while name_2 == name_1:
            name_2 = get_random_geo(dictionary)

        value_1 = cast_func(get_country_city_data(dictionary[name_1], metric))
        value_2 = cast_func(get_country_city_data(dictionary[name_2], metric))

        # retry if missing data
        if value_1 is None or value_2 is None:
            continue

        # determine correct option
        if value_1 > value_2:
            correct_option = "A"
            biggest_name, smallest_name = name_1, name_2
            biggest_metric, smallest_metric = value_1, value_2
        else:
            correct_option = "B"
            biggest_name, smallest_name = name_2, name_1
            biggest_metric, smallest_metric = value_2, value_1

        question_text = (
            f"Which {kind} has higher {metric_label}?\n"
            f"A) {name_1}\n"
            f"B) {name_2}\n"
            f"Your answer (A/B): "
        )

        user_choice = ask_ab(question_text)
        correct = (user_choice == correct_option)
        points = 1 if correct else 0

        frame_top()
        print_answer(biggest_name, correct=correct)
        print_answer_details(metric_label, biggest_name, smallest_name, biggest_metric, smallest_metric, unit=unit)
        get_additional_info_wiki(name_1, name_2)
        frame_bottom()
        return correct, points, question_text

    # if we failed to find data after retries
    question_text = f"(Skipped) Could not find two {kind}s with {metric_label} data."
    cprint(question_text, C.CYAN)
    return False, 0, question_text


def city_population_question():
    return compare_question(
        dictionary=cities,
        metric="population",
        metric_label="population",
        unit=None,
        cast_func=safe_int,
        kind="city"
    )

def city_area_question():
    return compare_question(
        dictionary=cities,
        metric="area",
        metric_label="area",
        unit="km²",
        cast_func=safe_float,
        kind="city"
    )

def country_population_question():
    return compare_question(
        dictionary=countries,
        metric="population",
        metric_label="population",
        unit=None,
        cast_func=safe_int,
        kind="country"
    )

def country_area_question():
    return compare_question(
        dictionary=countries,
        metric="area",
        metric_label="area",
        unit="km²",
        cast_func=safe_float,
        kind="country"
    )

# ----------------------------
# Main
# ----------------------------

def main():
    results = []

    results.append(city_capital_question())
    results.append(country_population_question())
    results.append(country_area_question())
    results.append(city_population_question())
    results.append(city_area_question())
    print(results)


if __name__ == "__main__":
    main()
