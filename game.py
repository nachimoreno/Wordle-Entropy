from utils import compute_pattern

def take_input(guesses: list, guessable: list) -> str:
    user_input = input("Enter your guess: ").lower()
    
    if len(user_input) != 5:
        print("Please enter a 5-letter word.")
        return take_input(guesses, guessable)

    if set(user_input.lower()).difference("abcdefghijklmnopqrstuvwxyz"):
        print("Only alphabetic characters are allowed.")
        return take_input(guesses, guessable)

    if user_input.lower() in guesses:
        print("Word already guessed.")
        return take_input(guesses, guessable)

    if user_input.lower() not in guessable:
        print("Word not in list of valid guesses.")
        return take_input(guesses, guessable)
    
    return user_input


def start_game(answer: str, guessable: list, matrix: bytearray, candidates: list) -> None:
    guesses = []

    while len(guesses) < 6:
        guess = take_input(guesses, guessable)
        guesses.append(guess)
        pattern_returned = compute_pattern(guess, answer)

        