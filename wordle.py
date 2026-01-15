from game import start_game
from utils import fetch_words, isolate_words, isolate_answers, get_or_create_matrix, pick_answer, get_initial_candidates

WORDLE_CSV = "wordle.csv"
PATTERN_MATRIX_FILE = "pattern_matrix.bin"
cached_matrix = None

if __name__ == "__main__":
    words = fetch_words(WORDLE_CSV)
    guessable = isolate_words(words)
    answers = isolate_answers(words)
    matrix = get_or_create_matrix(guessable, answers)
    candidates = get_initial_candidates(answers)
    answer = pick_answer(answers)

    start_game(answer, guessable, matrix, candidates)