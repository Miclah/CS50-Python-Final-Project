# TODO: 1. Quiz, retry, delete, write 
#           answers to a file
#       2. Timer, print out final score
#       3. other functionality, mnultiple answers, game history!!(zapis do suboru a potom vypis cez kniznicu)

import sys
import re
import csv
import tabulate

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
    counter = 0
    questions = read_sf("questions.csv", "simple")
    while True:
        while(len(questions) > 0):
            simple_questions = questions.pop(0)
            print(f"Question: {simple_questions['simple_questions']}")
            answer = input("Enter your answer: ").strip()
            if answer == simple_questions["answer"]:
                print("Correct!")
                counter += 1
            else:
                print("Incorrect!")
        print(f"Your final score is: {counter} points!")
        print("What would you like to do now?")
        choice = input("1. Retry, 2. New questions, 3. Add questions, 4. Quit: ").strip()
        if re.search("^(r|re|ret|retry|1)$", choice):
            questions = read_sf("simple_questions.csv")
            counter = 0
            continue
        if re.search("^(q|qu|qui|quit|2)$", choice):
            sys.exit()
        if re.search("^(n|ne|new|new q|new qu|new que|new ques|new quest|new questi|new questio|new question|new questions|3)$", choice):
            write_sf("questions.csv","w", "simple")
            continue
    
def hard_game():
    print("Hard game selected")
    
def multiple_choice_game():
    print("Multiple choice game selected")
    
def read_sf(file_name, difficulty):
    simple_questions = []
    hard_questions = []
    try:
        with open(file_name, 'r') as sfr:
            reader = csv.DictReader(sfr)
            for row in reader:
                if row["difficulty"] == "simple":
                    simple_questions.append({"simple_questions": row["simple_questions"], "answer": row["answer"]})
                else:
                    hard_questions.append({"hard_questions": row["hard_questions"], "answer": row["answer"]})
            if difficulty == "simple":
                return simple_questions
            else:
                return hard_questions
    except FileNotFoundError:
        answer = input("File not found, would you like to create it?(yes, no): ").strip().lower()
        if answer == "yes":
            diff = input("Simple or hard questions?(simple, hard): ").strip().lower()
            if diff == "simple":
                write_sf(file_name, "simple", "w")
            else:
                write_sf(file_name, "hard", "w")
        else:
            sys.exit()
    

def write_sf(file_name, difficulty, type):
    with open(file_name, type, newline="") as sfw:
        writer = csv.DictWriter(sfw, fieldnames=["question", "answer", "difficulty"])
        if sfw.tell() == 0:
            writer.writeheader()
        for question in ask_question():
            writer.writerow({"question": question["question"], "answer": question["answer"], "difficulty": question[f"{difficulty}"]})
         
    
def ask_question():
    print("\nYou will now be tasked with writing the questions, answers and difficulty. If you wish to stop type end.")
    print("Do not end without finishing the simple_questions and answer set!\n")
    questions = []
    while True:
        user_question = input("Enter a question: ").strip()
        if user_question == "end":
            break
        user_answer = input("Enter the answer: ").strip()
        user_difficulty = input("Enter the difficulty(simple, hard): ").strip()
        if user_answer == "end" or user_difficulty == "end":
            print("You cannot end without finishing the question and answer set!")
            continue
        questions.append({"simple_questions": user_question, "answer": user_answer, "difficulty": user_difficulty})
    return remove_duplicates(questions) 

def remove_duplicates(data):
    return [dict(t) for t in set(tuple(d.items()) for d in data)]

def print_table(data):
    print(tabulate.tabulate(data, headers="keys"))
    
if __name__ == "__main__":
    main()