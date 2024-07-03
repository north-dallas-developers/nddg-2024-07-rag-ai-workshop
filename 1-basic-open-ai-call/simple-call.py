import os
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()


while True:
    input_string = input()

    response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=input_string
    )

    # print(response)
    print(response.choices[0].text)

    print("")
    print("Give it another prompt!")
