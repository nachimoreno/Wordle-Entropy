import csv
import random

WORDLE_CSV = "wordle.csv"

def fetch_words(path: str) -> list:
    words = []

    with open(path, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            words.append((row[0], row[1], row[2]))

    return words


def pick_goal_word(words: list) -> str:
    while True:
        choice = random.choice(words)
        if choice[2] != "": break

    return choice[0]


def isolate_words(words: list) -> list:
    wordlist = []

    for word in words:
        wordlist.append(word[0])

    return wordlist


def evaluate_input(word: str, wordlist: list) -> str:
    passed_base_eval = True
    passed_adv_eval = False

    if len(word) != 5: passed_base_eval = False
    if len(word) > 5: print("Invalid input: Too many characters (must be 5).")
    if len(word) < 5: print("Invalid input: Too few characters (must be 5).")

    if not word.isalpha():
        passed_base_eval = False
        print("Invalid input: Only alphabetic characters are allowed.")

    if passed_base_eval:
        if word in wordlist:
            passed_adv_eval = True
        else:
            print("Invalid input: '{}' is not in the wordle set.".format(word))

    if passed_base_eval & passed_adv_eval:
        return word

    user_guess = input("\nGuess a valid word: ")
    evaluate_input(user_guess, wordlist)


def evaluate_guess(guess: str, goal_word: str) -> None:
    print(f"Evaluating {guess} against {goal_word}")

    guess = guess.lower()
    goal_word = goal_word.lower()

    guess_set = set(guess.split())

    print(f"\nGuess: '{guess_set}'")


def main():
    words = fetch_words(WORDLE_CSV)
    goal_word = pick_goal_word(words)
    words_list = isolate_words(words)

    for _ in range(6):
        user_guess = input("Guess a word: ")
        user_guess = evaluate_input(user_guess, words_list)

        if user_guess == goal_word:
            print(f"Correct! {goal_word} was the word to guess.")
            break

        evaluate_guess(user_guess, goal_word)


if __name__ == "__main__": main()