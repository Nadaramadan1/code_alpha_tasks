import random
import time
from difflib import get_close_matches
from collections import defaultdict

# Word lists for categories
categories = {
    'animals': ['cat', 'dog', 'elephant', 'lion', 'tiger', 'bear'],
    'fruits': ['apple', 'banana', 'cherry', 'grape', 'mango', 'orange'],
    'countries': ['egypt', 'france', 'germany', 'india', 'japan', 'mexico']
}

# Global variables
max_incorrect_guesses = 6
leaderboard = defaultdict(list)
ascii_art = [
    """
     -----
     |   |
         |
         |
         |
         |
    """,
    """
     -----
     |   |
     O   |
         |
         |
         |
    """,
    """
     -----
     |   |
     O   |
     |   |
         |
         |
    """,
    """
     -----
     |   |
     O   |
    /|   |
         |
         |
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
         |
         |
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    /    |
         |
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    """
]


def display_ascii_art(incorrect_guesses):
    print(ascii_art[incorrect_guesses])


def show_definition(word):
    try:
        from PyDictionary import PyDictionary
        dictionary = PyDictionary()
        definition = dictionary.meaning(word)
        if definition:
            for key, value in definition.items():
                print(f"{key}: {', '.join(value)}")
    except ImportError:
        print("Definition lookup feature requires PyDictionary module.")
        print(f"Definition unavailable for '{word}'.")


def play_game(word, multiplayer=False):
    hidden_word = ['_'] * len(word)
    incorrect_guesses = 0
    hints_used = 0
    start_time = time.time()
    print("Word:", " ".join(hidden_word))

    while incorrect_guesses < max_incorrect_guesses and '_' in hidden_word:
        guess = input("Guess a letter (or type 'hint' for a hint): ").lower()

        if guess == 'hint' and not multiplayer:
            if hints_used < len(word) - hidden_word.count('_'):
                hints_used += 1
                for i, char in enumerate(word):
                    if hidden_word[i] == '_':
                        hidden_word[i] = char
                        break
                print("Hint used. Word:", " ".join(hidden_word))
            else:
                print("No hints remaining.")
            continue

        if not guess.isalpha() or len(guess) != 1:
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in word:
            print(f"Good guess! '{guess}' is in the word.")
            for i, char in enumerate(word):
                if char == guess:
                    hidden_word[i] = char
        else:
            incorrect_guesses += 1
            print(f"Incorrect guess. You have {max_incorrect_guesses - incorrect_guesses} guesses left.")
            display_ascii_art(incorrect_guesses)

        print("Word:", " ".join(hidden_word))

    elapsed_time = time.time() - start_time
    if '_' not in hidden_word:
        print(f"Congratulations, you won! The word was: {word}")
        print(f"You finished in {elapsed_time:.2f} seconds with {hints_used} hints used.")
        return True
    else:
        print(f"Sorry, you lost. The word was: {word}")
        show_definition(word)
        return False


def leaderboard_display():
    print("\nLeaderboard:")
    for category, scores in leaderboard.items():
        print(f"{category.capitalize()}:")
        for score in scores:
            print(f"  {score[0]} - {score[1]} points")


def start_game():
    print("Welcome to Hangman!")
    mode = input("Choose mode (single/multiplayer): ").lower()
    while mode not in ['single', 'multiplayer']:
        print("Invalid choice. Please choose single or multiplayer.")
        mode = input("Choose mode (single/multiplayer): ").lower()

    multiplayer = mode == 'multiplayer'

    if multiplayer:
        word = input("Enter a word for the opponent to guess: ").lower()
        while not word.isalpha():
            print("Invalid word. Please enter a valid word.")
            word = input("Enter a word for the opponent to guess: ").lower()
        category = 'multiplayer'
    else:
        category = input("Choose category (animals/fruits/countries): ").lower()
        while category not in categories:
            print("Invalid choice. Please choose animals, fruits, or countries.")
            category = input("Choose category (animals/fruits/countries): ").lower()
        word = random.choice(categories[category])

    player = input("Enter your name: ")
    print(f"\nGood luck, {player}!")
    result = play_game(word, multiplayer)
    if result:
        leaderboard[category].append((player, len(word) * 10))


if __name__ == "__main__":
    while True:
        start_game()
        leaderboard_display()
        if input("\nDo you want to play again? (yes/no): ").lower() != 'yes':
            break