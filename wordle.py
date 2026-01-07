import csv
import random
import math
import os
import json

WORDLE_CSV = "wordle.csv"
OPENER_SCORES = "opener_scores.json"

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


def pattern(guess: str,
            answer: str) \
        -> tuple:

    guess = guess.lower()
    answer = answer.lower()

    remaining_answer = {}
    for char in answer:
        if char in remaining_answer.keys():
            remaining_answer[char] += 1
        else:
            remaining_answer[char] = 1

    p = [0,0,0,0,0]

    for i in range(len(answer)):
        if guess[i] == answer[i]:
            p[i] = 2
            remaining_answer[answer[i]] -= 1

    for i in range(len(p)):
        if p[i] == 2: continue

        if remaining_answer.get(guess[i], 0) > 0:
            p[i] = 1
            remaining_answer[guess[i]] -= 1

    return p[0], p[1], p[2], p[3], p[4]


def update_game_state(known_letters: set[str],
                      matches: str,
                      guess:str,
                      answer:str) \
    -> None:

    p = pattern(guess, answer)



def print_info(known_letters: set[str],
                matches: str) \
    -> None:

    print(f"\nKnown positions: {matches}")
    print(f"Known letters: {known_letters}\n")


def game():
    words = fetch_words(WORDLE_CSV)
    words_list = isolate_words(words)
    goal_word = pick_goal_word(words)

    won = False
    known_letters = set()
    matches = '_____'
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


def compute_entropy():
    if os.path.exists(OPENER_SCORES):
        print("Loading opener scores from disk...")
        with open(OPENER_SCORES, "r", encoding="utf-8") as f:
            opener_scores = json.load(f)

        # convert list of [word, score] back to dict if needed
        opener_scores = dict(opener_scores)
        return opener_scores

    print("Computing opener scores...")

    words = fetch_words(WORDLE_CSV)
    answers = [word[0] for word in words if word[2] != ""]
    opener_scores = {}
    N = len(answers)

    for idx, word in enumerate(words, 1):
        if idx % 1000 == 0: print(f"testing word: {word[0]}")
        opener = word[0]
        buckets = {}

        for answer in answers:
            p = pattern(opener, answer)
            buckets[p] = buckets.get(p, 0) + 1

        logN = math.log2(N)
        post_entropy = 0.0
        invN = 1.0 / N

        for c in buckets.values():
            post_entropy += (c * invN) * math.log2(c)

        info_gain_bits = logN - post_entropy
        opener_scores[opener] = info_gain_bits

    sorted_opener_scores = sorted(opener_scores.items(), key=lambda kv: kv[1], reverse=True)

    with open("opener_scores.json", "w", encoding="utf-8") as f:
        json.dump(sorted_opener_scores, f, indent=4)

    return sorted_opener_scores


def analysis():
    print(compute_entropy())


if __name__ == "__main__":
    analysis()