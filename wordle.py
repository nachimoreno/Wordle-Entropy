from game import start_game
from utils import fetch_words, isolate_words, isolate_answers, get_or_create_matrix, pick_answer, get_initial_candidates

WORDLE_CSV = "data/wordle.csv"

if __name__ == "__main__":
    words = fetch_words(WORDLE_CSV)
    guessables = isolate_words(words)
    answers = isolate_answers(words)
    matrix = get_or_create_matrix(guessables, answers)
    remaining_answer_indices = get_initial_candidates(answers)
    answer = pick_answer(answers)

    start_game(answer, guessables, answers, matrix, remaining_answer_indices)