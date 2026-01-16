from game import start_game, start_helper
from utils import fetch_words, isolate_words, isolate_answers, get_or_create_matrix, pick_answer, get_initial_candidates

WORDLE_CSV = "data/wordle.csv"

if __name__ == "__main__":
    words = fetch_words(WORDLE_CSV)
    guessables = isolate_words(words)
    answers = isolate_answers(words)
    matrix = get_or_create_matrix(guessables, answers)
    remaining_answer_indices = get_initial_candidates(answers)

    print("\nWelcome to Wordle Solver!")
    print("  1. Play Game (You guess, I check)")
    print("  2. Helper Mode (I suggest, you tell me the pattern)")
    mode = input("\nSelect mode (1 or 2): ")

    if mode == "1":
        answer = pick_answer(answers)
        start_game(answer, guessables, answers, matrix, remaining_answer_indices)
    elif mode == "2":
        start_helper(guessables, answers, matrix, remaining_answer_indices)
    else:
        print("Invalid selection. Defaulting to Play Game.")
        answer = pick_answer(answers)
        start_game(answer, guessables, answers, matrix, remaining_answer_indices)