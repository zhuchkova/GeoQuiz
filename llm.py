import os

from dotenv import load_dotenv
from openai import OpenAI
from colors import C


def init_openai():
    load_dotenv()

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    return client


def show_funfact(question):
    client = init_openai()
    response = client.responses.create(
        model="gpt-5-nano",
        instructions="You are a quiz app assistant, you provide fun fact about question. No follow up suggestion/question.",
        input=question,
    )

    print(response.output_text)

def analyze_knowledge(prompt):
    client = init_openai()
    response = client.responses.create(
        model="gpt-5-nano",
        instructions="You are a quiz app assistant, you analyze user knowledge. No follow up suggestion/question.",
        input=prompt,
    )

    print(f"{C.YELLOW}{response.output_text}{C.RESET}")


def example_funfact():
    show_funfact("Which city is bigger in size Berlin or Delhi?")
    print("==")
    show_funfact("Which city is bigger in population Berlin or Delhi?")

def main():
    prompt = """The player doesn't not know that Paris is the capital of France. Which advice can you give to the player?
                Be honest but friendly and funny.
              """
    analyze_knowledge(prompt)


if __name__ == "__main__":
    # example_funfact()
    main()
