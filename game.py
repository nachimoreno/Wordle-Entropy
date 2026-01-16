from utils import compute_pattern, calculate_remaining_answer_space, top_entropy_guesses

def take_input(
    guesses: list, 
    guessables: list) \
    -> str:
    """
    Takes input from the user and validates it.
    """
    user_input = input("Enter your guess: ").lower()
    
    if len(user_input) != 5:
        print("Please enter a 5-letter word.")
        return take_input(guesses, guessables)

    if set(user_input.lower()).difference("abcdefghijklmnopqrstuvwxyz"):
        print("Only alphabetic characters are allowed.")
        return take_input(guesses, guessables)

    if user_input.lower() in guesses:
        print("Word already guessed.")
        return take_input(guesses, guessables)

    if user_input.lower() not in guessables:
        print("Word not in list of valid guesses.")
        return take_input(guesses, guessables)
    
    return user_input


def start_game(
    answer: str, 
    guessables: list, 
    answers: list, 
    matrix: bytearray, 
    remaining_answer_indices: list) \
    -> None:
    """
    Starts the Wordle game.
    """
    guesses = []

    while len(guesses) < 6:
        tegs = top_entropy_guesses(remaining_answer_indices, guessables, answers, matrix, 20)
        print(f"Top 20 guesses: {tegs}\n")
        guess = take_input(guesses, guessables)
        guesses.append(guess)
        remaining_answer_indices = calculate_remaining_answer_space(guess, answer, remaining_answer_indices, guessables, answers)
        print(f"\nRemaining possible answers: {len(remaining_answer_indices)}\n")
        print(f"Remaining possible answers: {[answers[i] for i in remaining_answer_indices]}\n")
        if guess == answer:
            print(f"Congratulations! You guessed the word in {len(guesses)} guesses.")
            break
    
    if len(guesses) == 6:
        print(f"You ran out of guesses. The word was {answer}.")        