from termcolor import colored
from ai_query_logic import make_query

print("")
print(colored("Ask a question of your AI, peasant, and be quick about it!", "red"))
print("")

while True:
    input_string = input()
    make_query(input_string)

    print("")
    print("Ask another question before I decide to terminate you!")