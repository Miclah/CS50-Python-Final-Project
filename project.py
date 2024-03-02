# TODO: 1. Quiz, retry, delete, write 
#           answers to a file
#       2. Timer, print out final score
#       3. other functionality, mnultiple answers

import sys
import re
import csv

COUNTER = 0

def main():
   game_selector()
    
def game_selector():
    print("Welcome to the Quiz Game!")
    print("1. Start a new game")
    print("2. Quit")
    try:
        choice = int(input("Enter your choice: ").strip())
    except ValueError:
        print("You did not input a number!")
        pass
    if choice == 1:
        game_manager(input("Enter the type of game you want to play(simple quiz | hard quiz | multiple choice): ").strip())
    elif choice == 2:
        sys.exit()
    else:
        print("Invalid choice, please try again.")
        game_selector()
 

def game_manager(game_type):
    if re.search("^(s|si|sim|simp|simpl|simple)$", game_type):
        print("Simple quiz selected")
        simple_game()
    if re.search("^(h|ha|har|hard)$", game_type):
        print("Hard quiz selected")
        hard_game()
    if re.search("^(m|mu|mul|mult|multp|multi|multipl|multiple)$", game_type):
        print("Multiple choice quiz selected")
        multiple_choice_game()
        
def simple_game():
    global COUNTER
    questions = read_sf("simple_questions.csv")
    while(len(questions) > 0):
        question = questions.pop(0)
        print(f"Question: {question["question"]}")
        answer = input("Enter your answer: ").strip()
        if answer == question["answer"]:
            print("Correct!")
            COUNTER = COUNTER + 1
        else:
            print("Incorrect!")
    
def hard_game():
    print("Hard game selected")
def multiple_choice_game():
    print("Multiple choice game selected")
def read_sf(file_name):
    question = []
    try:
        with open(file_name, 'r') as sfr:
            reader = csv.DictReader(sfr)
            for row in reader:
                question.append({"question": row["question"], "answer": row["answer"]})
            return question
    except FileNotFoundError:
        answer = input("File not found, would you like to create it?(yes, no): ").strip().lower()
        if answer == "yes":
            write_sf(file_name)
        else:
            sys.exit()
    

def write_sf(file_name):
    with open(file_name, "w", newline="") as sfw:
        writer = csv.DictWriter(sfw, fieldnames=["question", "answer"])
        writer.writeheader()
        for question in ask_question():
            writer.writerow({"question": question["question"], "answer": question["answer"]})
         
    
def ask_question():
    print("\nYou will now be tasked with writing the questions and the answers. If you wish to stop type end.")
    print("Do not end without finishing the question and answer set!\n")
    questions_answers = []
    while True:
        user_question = input("Enter a question: ").strip()
        if user_question == "end":
            break
        user_answer = input("Enter the answer: ").strip()
        if user_answer == "end":
            print("You cannot end without finishing the question and answer set!")
            continue
        questions_answers.append({"question": user_question, "answer": user_answer})
    return remove_duplicates(questions_answers) 

def remove_duplicates(data):
    return [dict(t) for t in set(tuple(d.items()) for d in data)]
    
if __name__ == "__main__":
    main()