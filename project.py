import os
import sys
import re
import csv
import tabulate
import random

def main():
    """
    The main function of the program.
    It serves as the entry point for the Quiz Game.
    """
    game_selector()
    
def game_selector():
    """
    Allows the user to select different options in the game.
    1. Start a new game
    2. Print game history
    3. Delete game history
    4. Quit
    """
    while True:
        print("Welcome to the Quiz Game!")
        print("1. Start a new game")
        print("2. Print game history")
        print("3. Delete game history")
        print("4. Quit")
        try:
            choice = int(input("Enter your choice: ").strip())
            if choice == 1:
                game_manager(input("Enter the type of game you want to play(simple quiz | hard quiz | multiple choice quiz): ").strip())
                break
            elif choice == 2:
                print_history("history.csv")
            elif choice == 3:
                delete_history("history.csv")
            elif choice == 4:
                sys.exit()
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("You did not input a number!")

def print_history(file):
    """
    Prints the game history stored in a file.

    Parameters:
    file (str): The name of the file containing the game history.

    Returns:
    None
    """
    games_history = read_game_history(file)
    print(tabulate.tabulate(games_history, headers="keys", tablefmt="fancy_grid"))

def delete_history(file_name):
    """
    Deletes the game history stored in a file.

    Parameters:
    file_name (str): The name of the file containing the game history.

    Returns:
    None
    """
    games_history = read_game_history(file_name)
    if not games_history:
        print("Game history is already empty.")
    else:
        with open(file_name, 'w', newline='') as csvfile:
            csvfile.truncate()
        print("Game history deleted.")

def read_game_history(file_name):
    """
    Reads the game history stored in a file.

    Parameters:
    file_name (str): The name of the file containing the game history.

    Returns:
    list: A list of dictionaries representing the game history.
    """
    games_history = []
    with open(file_name, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            games_history.append(row)
    return games_history


def game_manager(game_type):
    """
    Manages the game based on the selected game type.

    Parameters:
    game_type (str): The type of game to be played.

    Returns:
    None
    """
    if re.search("^(s|si|sim|simp|simpl|simple)$", game_type):
        game("simple")
    if re.search("^(h|ha|har|hard)$", game_type):
        game("hard")
    if re.search("^(m|mu|mul|mult|multp|multi|multipl|multiple)$", game_type):
        multi_choice_game()
    else:
        print("Invalid choice, please try again.")
        game_manager(input("Enter the type of game you want to play(simple quiz | hard quiz | multiple choice quiz): ").strip())
        
def game(type, games_history=None):
    """
    Runs the game based on the selected game type.

    Parameters:
    type (str): The type of game to be played.
    games_history (list, optional): The list of game histories. Defaults to None.

    Returns:
    None
    """
    counter = 0
    questions = read_sf("questions.csv", type)
    question_asked = False  
    if games_history is None:
        games_history = []
    game_history = []
    
    if len(questions) == 0:
        print("File is empty, please add questions first.")
        while True: 
            que = input("Would you like to add questions or exit?(add|exit): ").strip().lower()
            if re.search("^(a|ad|add)$", que):
                write_sf("questions.csv", "a")
                break 
            if re.search("^(e|ex|exit)$", que):
                sys.exit()
            else:
                print("Invalid choice, please try again.")
                    
    while True:        
        while(len(questions) > 0):
            simple_questions = questions.pop(0)
            print(f"Question: {simple_questions['question']}")
            answer = input("Enter your answer: ").strip()
            correct = answer == simple_questions["answer"]
            if answer == simple_questions["answer"]:
                print("Correct!")
                counter += 1
            else:
                print("Incorrect!")
            question_asked = True  
            game_history.append({"question": simple_questions["question"], "user_answer": answer, "correct_answer": simple_questions["answer"], "correct": correct})
        if game_history:
            games_history.append(game_history)
        game_history = []
        
        if question_asked:
            print(f"Your final score is: {counter} points!")
            print("What would you like to do now?")
            question_asked = False
        
        choice = input("1. Retry, 2. New questions, 3. Add questions, 4. Delete questions, 5. Print game history, 6. Quit: ").strip()
        if re.search("^(r|re|ret|retry|1)$", choice):
            game(type, games_history)
        elif re.search("^(n|ne|new|new q|new qu|new que|new ques|new questi|new questio|new question|new questions|2)$", choice):
            write_sf("questions.csv", "w")
            continue
        elif re.search("^(a|ad|add|add q|add qu|add que|add ques|add questi|add questio|add question|add questions|3)$", choice): 
            write_sf("questions.csv", "a")
            continue
        elif re.search("^(d|de|del|dele|delet|delete!delete q|delete qu|delete que|delete ques|delete quest|delete questi|delete questio|delete question|delete questions|4)$", choice):
            delete_sf("questions.csv")
            continue
        elif re.search("^(p|pr|pri|prin|print|print g|print ga|print gam|print game|print game h|print game hi|print game his|print game hist|print game histo|print game histor|print game history|5)$", choice):
            print_table(games_history)
            continue
        elif re.search("^(q|qu|qui|quit|6)$", choice):
            history(games_history)
            sys.exit()
        else:
            print("Invalid choice, please try again.")
            continue
        
def multi_choice_game():
    """
    Starts the multiple choice game.

    This function checks if the "multi_choice.csv" file exists and creates it if it doesn't.
    Then it calls the multi_game() function to run the game.

    Parameters:
    None

    Returns:
    None
    """
    if not os.path.isfile("multi_choice.csv"):
        write_mf("multi_choice.csv")

    multi_game()

def read_mf(file_name):
    """
    Reads the multiple choice questions from a file.

    This function reads the questions from the specified file and returns a list of dictionaries representing the questions.

    Parameters:
    file_name (str): The name of the file containing the multiple choice questions.

    Returns:
    list: A list of dictionaries representing the multiple choice questions.
    """
    questions = []
    with open(file_name, "r") as mf:
        reader = csv.DictReader(mf)
        for row in reader:
            questions.append(row)
    return questions


def add_multi_choice_questions():
    """
    Adds multiple choice questions to the file.

    This function prompts the user to enter multiple choice questions and their answers.
    The questions are stored in a list of dictionaries and then written to the "multi_choice.csv" file.

    Parameters:
    None

    Returns:
    None
    """
    print("You will now be prompted to add multiple choice questions.")
    print("Enter 'end' in the question field to finish adding questions.")
    print("Enter at least 3 answers and at most 6 answers.")

    questions = []
    while True:
        question = input("Enter the question: ").strip()
        if question == "end":
            break

        answers = []
        print("Enter the answers:")
        for i in range(1, 7):
            answer = input(f"{i}. ").strip()
            if answer == "end":
                if len(answers) < 3:
                    print("You cannot end without providing at least 3 answers.")
                    continue
                else:
                    break
            answers.append(answer)

        while True:
            correct_answer = input("Enter the correct answer: ").strip()
            if correct_answer in answers:
                break
            else:
                print("The correct answer must match one of the provided answers.")

        answers.remove(correct_answer)
        answers.append(correct_answer)
        formatted_answers = ",".join(answers)

        questions.append({"question": question, "answers": formatted_answers, "correct_answer": correct_answer})

    write_mf("multi_choice.csv", questions)


def write_mf(file_name, questions=[]):
    """
    Writes multiple choice questions to a file.

    This function takes a list of dictionaries representing multiple choice questions and writes them to the specified file.
    The questions are shuffled randomly before being written to the file.

    Parameters:
    file_name (str): The name of the file to write the questions to.
    questions (list, optional): The list of dictionaries representing the questions. Defaults to an empty list.

    Returns:
    None
    """
    with open(file_name, "a", newline="") as mf:
        writer = csv.DictWriter(mf, fieldnames=["question", "answers", "correct_answer"])
        if mf.tell() == 0:
            writer.writeheader()
        for question in questions:
            answers = question["answers"].split(",")
            random.shuffle(answers)
            question["answers"] = ",".join(answers)
            writer.writerow(question)


def multi_game(games_history=None):
    """
    Runs the multiple choice game.

    This function allows the user to play the multiple choice game.
    It prompts the user with questions, shuffles the answer choices, and keeps track of the user's score.
    The game history is stored in the games_history list.

    Parameters:
    games_history (list, optional): The list of game histories. Defaults to None.

    Returns:
    None
    """
    counter = 0
    questions = read_mf("multi_choice.csv")
    
    if len(questions) == 0:
        add_multi_choice_questions()
        
    question_asked = False  
    if games_history is None:
        games_history = []
    game_history = []
    
    if len(questions) == 0:
        print("File is empty, please add questions first.")
        while True: 
            que = input("Would you like to add questions or exit?(add|exit): ").strip().lower()
            if re.search("^(a|ad|add)$", que):
                write_sf("questions.csv", "a")
                break 
            if re.search("^(e|ex|exit)$", que):
                sys.exit()
            else:
                print("Invalid choice, please try again.")
                    
    while True:        
        while(len(questions) > 0):
            simple_questions = questions.pop(0)
            print(f"Question: {simple_questions['question']}")
            answers = simple_questions["answers"].split(",")
            random.shuffle(answers)
            for i, answer in enumerate(answers, 1):
                print(f"{i}. {answer}")
            user_input = input("Enter your answer or the number associated with it: ").strip()
            if user_input.isdigit():
                user_input = answers[int(user_input) - 1]
            correct = user_input == simple_questions["correct_answer"]
            if correct:
                print("Correct!")
                counter += 1
            else:
                print("Incorrect!")
            question_asked = True  
            game_history.append({"question": simple_questions["question"], "user_answer": user_input, "correct_answer": simple_questions["correct_answer"], "correct": correct})
        if game_history:
            games_history.append(game_history)
        game_history = []
        
        if question_asked:
            print(f"Your final score is: {counter} points!")
            print("What would you like to do now?")
            question_asked = False
        
        choice = input("1. Retry, 2. New questions, 3. Add questions, 4. Delete questions, 5. Print game history, 6. Quit: ").strip()
        if re.search("^(r|re|ret|retry|1)$", choice):
            multi_game(games_history)
        elif re.search("^(n|ne|new|new q|new qu|new que|new ques|new questi|new questio|new question|new questions|2)$", choice):
            write_sf("questions.csv", "w")
            continue
        elif re.search("^(a|ad|add|add q|add qu|add que|add ques|add questi|add questio|add question|add questions|3)$", choice): 
            write_sf("questions.csv", "a")
            continue
        elif re.search("^(d|de|del|dele|delet|delete!delete q|delete qu|delete que|delete ques|delete quest|delete questi|delete questio|delete question|delete questions|4)$", choice):
            delete_sf("questions.csv")
            continue
        elif re.search("^(p|pr|pri|prin|print|print g|print ga|print gam|print game|print game h|print game hi|print game his|print game hist|print game histo|print game histor|print game history|5)$", choice):
            print_table(games_history)
            continue
        elif re.search("^(q|qu|qui|quit|6)$", choice):
            history(games_history)
            sys.exit()
        else:
            print("Invalid choice, please try again.")
            continue

def history(games_history):
    """
    Writes the game history to a CSV file.

    Parameters:
    games_history (list): The list of game histories.

    Returns:
    None
    """
    with open('history.csv', 'w', newline='') as csvfile:
        fieldnames = ['question', 'user_answer', 'correct_answer', 'correct']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for game in games_history:
            for question in game:
                writer.writerow(question)

def read_sf(file_name, difficulty):
    """
    Reads the questions from a CSV file based on the specified difficulty.

    Parameters:
    file_name (str): The name of the file containing the questions.
    difficulty (str): The difficulty level of the questions.

    Returns:
    list: A list of dictionaries representing the questions.
    """
    simple_questions = []
    hard_questions = []
    try:
        with open(file_name, 'r') as sfr:
            reader = csv.DictReader(sfr)
            for row in reader:
                if row["difficulty"] == "simple":
                    simple_questions.append({"question": row["question"], "answer": row["answer"], "simple": row["difficulty"]})
                else:
                    hard_questions.append({"question": row["question"], "answer": row["answer"], "hard": row["difficulty"]})
            if difficulty == "simple":
                return simple_questions
            else:
                return hard_questions
    except FileNotFoundError:
        answer = input("File not found, would you like to create it?(yes, no): ").strip().lower()
        if answer == "yes":
            write_sf(file_name, "w")
        else:
            sys.exit()

def write_sf(file_name, type):
    """
    Writes the questions to a CSV file based on the specified type.

    Parameters:
    file_name (str): The name of the file to write the questions to.
    type (str): The type of questions to be written.

    Returns:
    None
    """
    with open(file_name, type, newline="") as sfw:
        writer = csv.DictWriter(sfw, fieldnames=["question", "answer", "difficulty"])
        if sfw.tell() == 0:
            writer.writeheader()
        data = ask_question()
        for question in format_data(data):
            writer.writerow({"question": question["question"], "answer": question["answer"], "difficulty": question["difficulty"]})
         
def delete_sf(file_name):
    """
    Deletes selected questions from a CSV file.

    Parameters:
    file_name (str): The name of the file containing the questions.

    Returns:
    None
    """
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        try:
            next(reader)  
        except StopIteration:
            print("The file is empty. No questions to delete.")
            return

        questions = list(reader)
    print("Here are the choices of questions to delete: ")
    for i, row in enumerate(questions):
        print(f"{i+1}. {row[0]}")

    line_numbers_to_delete = input("Enter the line numbers of the questions to delete, separated by commas: ")
    line_numbers_to_delete = list(map(int, line_numbers_to_delete.split(',')))

    questions = [row for i, row in enumerate(questions, start=1) if i not in line_numbers_to_delete]

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(questions)

    return

def ask_question():
    """
    Prompts the user to enter a question, answer, and difficulty level.

    Returns:
    list: A list of dictionaries representing the questions, answers, and difficulty levels.
    """
    print("\nYou will now be tasked with writing the questions, answers, and difficulty levels. If you wish to stop, type 'end'.")
    print("Do not end without finishing the question and answer set!\n")
    questions = []
    while True:
        user_question = input("Enter a question: ").strip()
        if user_question == "end":
            break
        user_answer = input("Enter the answer: ").strip()
        user_difficulty = input("Enter the difficulty (simple, hard): ").strip()
        if re.search("^(s|si|sim|simp|simpl|simple)$", user_difficulty):
            user_difficulty = "simple"
        elif re.search("^(h|ha|har|hard)$", user_difficulty):
            user_difficulty = "hard"
        else:
            print("Invalid choice, please try again.")
            continue
        if user_answer == "end" or user_difficulty == "end":
            print("You cannot end without finishing the question and answer set!")
            continue
        questions.append({"question": user_question, "answer": user_answer, "difficulty": user_difficulty})
    return remove_duplicates(questions) 

def remove_duplicates(data):
    """
    Removes duplicate questions from the list of questions.

    Parameters:
    data (list): A list of dictionaries representing the questions, answers, and difficulty levels.

    Returns:
    list: A list of dictionaries with duplicate questions removed.
    """
    return [dict(t) for t in set(tuple(d.items()) for d in data)]

def format_data(data):
    """
    Formats the questions and answers in the data.

    Parameters:
    data (list): A list of dictionaries representing the questions, answers, and difficulty levels.

    Returns:
    list: A list of dictionaries with formatted questions and answers.
    """
    for i in data:
        i["question"] = i["question"].capitalize()
        if i["question"][-1] != "?":
            i["question"] += "?"
        i["question"] = re.sub(r"[^a-zA-Z0-9?° ]", "", i["question"])
        i["answer"] = re.sub(r"[^a-zA-Z0-9° ]", "", i["answer"])
        i["answer"] = i["answer"].capitalize()
    return data

def print_table(data):
    """
    Prints the game data in a formatted table.

    This function takes a list of dictionaries representing the game data and prints it in a formatted table using the tabulate library.

    Parameters:
    data (list): A list of dictionaries representing the game data.

    Returns:
    None
    """
    flattened_data = []
    for i, game in enumerate(data):
        flattened_data.extend(game)
        if i < len(data) - 1:
            flattened_data.append({"question": f"--- End of Game {i+1} ---", "user_answer": "", "correct_answer": "", "correct": ""})
    print(tabulate.tabulate(flattened_data, headers="keys", tablefmt="fancy_grid"))
    
if __name__ == "__main__":
    main()