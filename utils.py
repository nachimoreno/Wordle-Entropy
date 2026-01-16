import csv
import os
import random
import math

PATTERN_MATRIX_FILE = "data/pattern_matrix.bin"
cached_matrix = None

def fetch_words(
    path: str) \
    -> list:
    """
    Fetches the list of accepted words from the given path.

    :param path: Path to the CSV file containing the words.
    
    :return: List of tuples (word, frequency, the day it was 
    used as an answer, and the set of characters in the word).
    """
    words = []

    with open(path, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            words.append((row[0], row[1], row[2], set(row[0])))

    del words[0]

    return words


def isolate_words(
    words_data: list) \
    -> list:
    """
    Extracts all valid guessable words from the data.
    """
    return [w[0] for w in words_data]


def isolate_answers(
    words_data: list) \
    -> list:
    """
    Extracts only the words that are valid answers (have a date string).
    """
    return [w[0] for w in words_data if w[2] != ""]


def compute_pattern(
    guess: str, 
    answer: str) \
    -> int:
    """
    Computes the standard Wordle pattern for a given guess and answer.
    Returns an integer 0..242 representing the pattern in base 3.
    0 = Grey, 1 = Yellow, 2 = Green.
    Pattern is encoded as: p[0]*3^0 + p[1]*3^1 + ... + p[4]*3^4
    """
    # 0 = Grey, 1 = Yellow, 2 = Green
    pattern = [0] * 5
    
    # optimize counts
    answer_counts = {}
    for char in answer:
        answer_counts[char] = answer_counts.get(char, 0) + 1
        
    # First pass: Green
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 2
            answer_counts[guess[i]] -= 1
            
    # Second pass: Yellow
    for i in range(5):
        if pattern[i] == 2:
            continue
        g_char = guess[i]
        if answer_counts.get(g_char, 0) > 0:
            pattern[i] = 1
            answer_counts[g_char] -= 1
            
    # Encode to integer
    code = 0
    mult = 1
    for p in pattern:
        code += p * mult
        mult *= 3
        
    return code


def generate_pattern_matrix(
    guesses: list, 
    answers: list) \
    -> bytearray:
    """
    Generates a flattened matrix of patterns for (guess, answer) pairs.
    rows: guesses, cols: answers.
    size: len(guesses) * len(answers)
    index = guess_idx * num_answers + answer_idx
    """
    num_guesses = len(guesses)
    num_answers = len(answers)
    matrix = bytearray(num_guesses * num_answers)
    
    print(f"Generating pattern matrix ({num_guesses}x{num_answers})... This may take a moment.")
    for i, guess in enumerate(guesses):
        if i % 100 == 0:
            print(f"Processing row {i}/{num_guesses}")
        for j, answer in enumerate(answers):
            pattern = compute_pattern(guess, answer)
            matrix[i * num_answers + j] = pattern
            
    return matrix


def get_or_create_matrix(
    guesses: list, 
    answers: list) \
    -> bytearray:
    """
    Gets the pattern matrix for the given guesses and answers.
    If the matrix has already been generated, it is returned from the cache.
    Otherwise, it is generated and cached for future use.
    """
    global cached_matrix
    if cached_matrix:
        return cached_matrix
        
    expected_size = len(guesses) * len(answers)
    
    if os.path.exists(PATTERN_MATRIX_FILE):
        try:
            if os.path.getsize(PATTERN_MATRIX_FILE) == expected_size:
                with open(PATTERN_MATRIX_FILE, "rb") as f:
                    cached_matrix = bytearray(f.read())
                return cached_matrix
            else:
                print("Matrix file size mismatch. Regenerating...")
        except Exception as e:
            print(f"Error loading matrix: {e}")
            
    cached_matrix = generate_pattern_matrix(guesses, answers)
    with open(PATTERN_MATRIX_FILE, "wb") as f:
        f.write(cached_matrix)
    return cached_matrix


def calculate_remaining_answer_space(
    guess: str, 
    candidate_indices: list, 
    guessables: list, 
    answers: list,
    answer: str = None,
    pattern_int: int = None) \
    -> list[int]:
    """
    Calculates how many candidates remain after guessing 'guess' given either the 
    true answer or the observed pattern.
    
    :param guess: The word guessed.
    :param candidate_indices: List of indices into the 'answers' list (subset of potential solutions).
    :param guessables: List of all valid guess words.
    :param answers: List of all valid answer words.
    :param answer: The true answer (optional).
    :param pattern_int: The observed pattern as an integer (optional).
    :return: A list of remaining candidate indices.
    """
    matrix = get_or_create_matrix(guessables, answers)
    num_answers = len(answers)
    
    try:
        guess_idx = guessables.index(guess)
    except ValueError:
        return []

    if pattern_int is None:
        if answer is None:
            raise ValueError("Either 'answer' or 'pattern_int' must be provided.")
        try:
            answer_idx = answers.index(answer) 
        except ValueError:
            return []
        observed_pattern = matrix[guess_idx * num_answers + answer_idx]
    else:
        observed_pattern = pattern_int
    
    remaining_answer_indices = []
    row_start_idx = guess_idx * num_answers
    
    # candidate_indices are indices into 'answers'
    for idx in candidate_indices:
        if matrix[row_start_idx + idx] == observed_pattern:
            remaining_answer_indices.append(idx)
            
    return remaining_answer_indices


def string_to_pattern(
    p_str: str) \
    -> int:
    """
    Converts a 5-digit pattern string (e.g., "00210") where 0=Grey, 1=Yellow, 2=Green
    into the integer pattern used by the matrix.
    """
    code = 0
    mult = 1
    for char in p_str:
        p = int(char)
        code += p * mult
        mult *= 3
    return code


def count_to_bits(
    count: int) \
    -> int:
    """
    Converts a count of remaining answers to the number of bits of information 
    gained from the guess.
    """
    words_data = fetch_words(WORDLE_CSV)
    total_words = len(words_data)

    return -int(math.log(count / total_words, 2))


def get_initial_candidates(
    answers: list) \
    -> list:
    """
    Returns the initial list of candidate indices (0 to len(answers)-1).
    """
    return list(range(len(answers)))


def pick_answer(
    answers: list) \
    -> str:
    """
    Picks a random answer from the list of answers.
    """
    return random.choice(answers)


def top_entropy_guesses(
    remaining_answer_indices: list,
    guessables: list,
    answers: list,
    matrix: bytearray,
    n: int
) -> list[tuple[str, float]]:
    """
    Returns the top n guesses that maximize the expected number of remaining answers.

    :param remaining_answer_indices: List of indices into the 'answers' list (subset of potential solutions).
    :param guessables: List of all valid guess words.
    :param answers: List of all valid answer words.
    :param matrix: The pattern matrix for the given guesses and answers.
    :param n: The number of top guesses to return.
    :param restrict_to_candidates: Whether to restrict the guesses to the remaining candidates.
    :return: A list of tuples containing (guess, expected_remaining).
    """

    num_answers = len(answers)
    k = len(remaining_answer_indices)
    
    if k <= 1: # returns only possible answer if there is only one left
        return [(answers[remaining_answer_indices[0]], 0.0)] if k == 1 else []

    if k < 30:
        restrict_to_candidates = True
    else:
        restrict_to_candidates = False
    
    guess_to_idx = {w: i for i, w in enumerate(guessables)}
    guess_indices = [guess_to_idx[answers[a_idx]] for a_idx in remaining_answer_indices]
    results = []
    
    for guess_idx in guess_indices:
        row_start_idx = guess_idx * num_answers
        counts = [0] * 243
        for answer_idx in remaining_answer_indices:
            counts[matrix[row_start_idx + answer_idx]] += 1

        expected_remaining = sum(c*c for c in counts) / k
        results.append((guessables[guess_idx], expected_remaining))
    
    results.sort(key=lambda x: x[1])
    return results[:n]