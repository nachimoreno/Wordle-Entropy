from utils import compute_pattern, calculate_remaining_answer_space, top_entropy_guesses, string_to_pattern

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


def take_pattern_input() -> int:
    """
    Takes a 5-digit pattern input from the user (0=Grey, 1=Yellow, 2=Green).
    Example: 00210
    """
    p_input = input("Enter the pattern (e.g., 00210 where 0=Grey, 1=Yellow, 2=Green): ")
    if len(p_input) != 5 or not all(c in "012" for c in p_input):
        print("Invalid pattern. Please enter exactly 5 digits using only 0, 1, or 2.")
        return take_pattern_input()
    return string_to_pattern(p_input)


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
        remaining_answer_indices = calculate_remaining_answer_space(
            guess, remaining_answer_indices, guessables, answers, answer=answer
        )
        print(f"\nRemaining possible answers: {len(remaining_answer_indices)}\n")
        if len(remaining_answer_indices) <= 20:
             print(f"Remaining possible answers: {[answers[i] for i in remaining_answer_indices]}\n")
        else:
             print(f"First 20 remaining answers: {[answers[i] for i in remaining_answer_indices[:20]]}...\n")

        if guess == answer:
            print(f"Congratulations! You guessed the word in {len(guesses)} guesses.")
            break
    
    if len(guesses) >= 6 and guesses[-1] != answer:
        print(f"You ran out of guesses. The word was {answer}.")


def start_helper(
    guessables: list, 
    answers: list, 
    matrix: bytearray, 
    remaining_answer_indices: list) \
    -> None:
    """
    Starts the Wordle helper mode.
    """
    guesses = []

    while len(guesses) < 6:
        print(f"Step {len(guesses) + 1}:")
        tegs = top_entropy_guesses(remaining_answer_indices, guessables, answers, matrix, 20)
        print(f"Top 20 suggested guesses: {tegs}\n")
        
        guess = input("Enter the word you guessed (or 'exit' to quit): ").lower()
        if guess == 'exit':
            break
        if guess not in guessables:
            print("Word not in list of valid guesses.")
            continue
            
        guesses.append(guess)
        pattern_int = take_pattern_input()
        
        remaining_answer_indices = calculate_remaining_answer_space(
            guess, remaining_answer_indices, guessables, answers, pattern_int=pattern_int
        )

        if len(remaining_answer_indices) == 1:
            print(f"The word is {answers[remaining_answer_indices[0]]}")
            break
        
        print(f"\nRemaining possible answers: {len(remaining_answer_indices)}\n")
        if len(remaining_answer_indices) <= 20:
             print(f"Remaining possible answers: {[answers[i] for i in remaining_answer_indices]}\n")
        else:
             print(f"First 20 remaining answers: {[answers[i] for i in remaining_answer_indices[:20]]}...\n")

        if pattern_int == 242: # 2*3^0 + 2*3^1 + 2*3^2 + 2*3^3 + 2*3^4 = 2(1+3+9+27+81) = 2(121) = 242
            print(f"Congratulations! You win!")
            break
    
    if len(guesses) >= 6 and pattern_int != 242:
        print("Game over.")