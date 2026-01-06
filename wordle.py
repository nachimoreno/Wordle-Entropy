import csv
import random
import math
import statistics
import json

WORDLE_CSV = "wordle.csv"

def fetch_words(path: str) \
        -> list:
    words = []

    with open(path, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            words.append((row[0], row[1], row[2]))

    del words[0]

    return words


def isolate_words(words: list) \
        -> list:

    wordlist = []

    for word in words:
        wordlist.append(word[0])

    return wordlist


def pick_goal_word(words: list) \
        -> str:
    while True:
        choice = random.choice(words)
        if choice[2] != "": break

    return choice[0]


def take_input(wordlist: list,
               guesses: list,) \
        -> str:

    while True:

        word = input("Guess a word: ").strip().lower()

        if word in guesses:
            print("Invalid input: Already entered.")
            continue

        if len(word) > 5:
            print("Invalid input: Too many characters (must be 5).")
            continue
        if len(word) < 5:
            print("Invalid input: Too few characters (must be 5).")
            continue

        if not word.isalpha():
            print("Invalid input: Only alphabetic characters are allowed.")
            continue

        if word not in wordlist:
            print(f"Invalid input: '{word}' is not in the wordle set.")
            continue

        guesses.append(word)
        return word


def evaluate_guess(guess: str,
                   goal_word: str) \
        -> tuple[set[str], list[str]]:

    if guess is None or goal_word is None:
        raise ValueError("Invalid input: guess cannot be None.")

    guess = guess.lower()
    goal_word = goal_word.lower()

    intersection = set(guess) & set(goal_word)

    if len(intersection) == 0:
        print("No matching letters found.")
        return intersection, ['_','_','_','_','_']

    matches = ['_','_','_','_','_']

    for pos in range(5):
        if guess[pos] == goal_word[pos]:
            matches[pos] = guess[pos]

    return intersection, matches


def update_game_state(known_letters: set[str],
                      matches: list[str],
                      guess:str,
                      goal_word:str) \
    -> None:

    intersection, found_matches = evaluate_guess(guess, goal_word)

    for pos in range(len(matches)):
        if found_matches[pos] == '_': continue
        matches[pos] = found_matches[pos]

    known_letters.update(intersection)


def print_info(known_letters: set[str],
                matches: list[str]) \
    -> None:

    matchstring = ''.join(matches)

    print(f"\nKnown positions: {matchstring}")
    print(f"Known letters: {known_letters}\n")


def game():
    words = fetch_words(WORDLE_CSV)
    words_list = isolate_words(words)
    goal_word = pick_goal_word(words)

    won = False
    known_letters = set()
    matches = ['_','_','_','_','_']
    guesses = []

    for _ in range(6):
        guess = take_input(words_list, guesses)

        if guess == goal_word:
            print(f"\nCorrect! {goal_word.title()} was the word to guess. Well done!")
            won = True
            break

        update_game_state(known_letters, matches, guess, goal_word)
        print_info(known_letters, matches)

    if not won:
        print(f"\nYou ran out of guesses. The word was '{goal_word}'!")


def p_to_bits(p: float) -> float:
    bits = -math.log2(p)
    return bits


def total_possible_matches(words,
                           known_letters: set[str],
                           matches: list[str]) \
    -> int:

    possible_matches = []

    if matches == ['_','_','_','_','_']: char_match_available = False # To be set to false, but true for debugging
    else: char_match_available = True

    num_char_matches_possible = 0

    if char_match_available:

        for match in matches:

            if not match == '_':
                num_char_matches_possible += 1

    for word in words:
        if word == words[0]: continue

        if known_letters.issubset(word[0]):

            if char_match_available:
                num_char_matches_found = 0

                for pos in range(len(word[0])):

                    if word[0][pos] == matches[pos]:
                        num_char_matches_found += 1

                if num_char_matches_found == num_char_matches_possible:
                    possible_matches.append(word)
                    continue

            possible_matches.append(word)

    return len(possible_matches)


def compute_opener_scores():
    opener_scores = {}
    words = fetch_words(WORDLE_CSV)
    answer_words = [word for word in words if word[2] != '']

    ca = 0
    for answer in answer_words:
        ca += 1
        cw = 0
        for word in words:
            cw += 1
            print(f"{ca}/{len(answer_words)}: {answer[0]} |{cw}/{len(words)}: {word[0]}")

            intersection, matches = evaluate_guess(word[0], answer[0])
            tpm = total_possible_matches(words, intersection, matches)
            p = tpm / len(words)
            bits = p_to_bits(p)

            if not word[0] in opener_scores:
                opener_scores[word[0]] = [bits]
            else:
                opener_scores[word[0]].append(bits)

    for word in opener_scores:
        mean = statistics.mean(opener_scores[word])
        opener_scores[word] = mean

    sorted_opener_scores = sorted(opener_scores.items(), key=lambda dct: dct[1], reverse=True)

    with open("opener_scores.json", "w", encoding="utf-8") as f:
        json.dump(sorted_opener_scores, f, indent=4)


def analysis():
    compute_opener_scores()


if __name__ == "__main__": analysis()