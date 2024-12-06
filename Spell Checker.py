import tkinter as tk
from tkinter import messagebox

# Constants
MATCH = 0
CONSONANT_CONSONANT = 1
VOWEL_VOWEL = 1
VOWEL_CONSONANT = 3
GAP = 2

VOWELS = set("aeiou")

# Function to determine if a character is a vowel
def is_vowel(char):
    return char.lower() in VOWELS

# Sequence alignment algorithm
def calculate_penalty(word1, word2):
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i * GAP
    for j in range(m + 1):
        dp[0][j] = j * GAP

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = MATCH
            elif is_vowel(word1[i - 1]) and is_vowel(word2[j - 1]):
                cost = VOWEL_VOWEL
            elif not is_vowel(word1[i - 1]) and not is_vowel(word2[j - 1]):
                cost = CONSONANT_CONSONANT
            else:
                cost = VOWEL_CONSONANT

            dp[i][j] = min(
                dp[i - 1][j - 1] + cost,  # Match/mismatch
                dp[i - 1][j] + GAP,       # Insert gap in word2
                dp[i][j - 1] + GAP        # Insert gap in word1
            )

    return dp[n][m]

# Load dictionary from a text file
def load_dictionary(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

# Function to get suggestions
def get_suggestions(input_word, dictionary):
    penalties = [(word, calculate_penalty(input_word, word)) for word in dictionary]
    penalties.sort(key=lambda x: x[1])
    return [word for word, _ in penalties[:10]]

# GUI Application
class SpellCheckerApp:
    def __init__(self, root, dictionary):
        self.root = root
        self.dictionary = dictionary
        self.root.title("Spell Checker")
        
        self.label = tk.Label(root, text="Enter a word:")
        self.label.pack(pady=5)
        
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)
        
        self.button = tk.Button(root, text="Check Spelling", command=self.check_spelling)
        self.button.pack(pady=5)
        
        self.result_label = tk.Label(root, text="Suggestions:")
        self.result_label.pack(pady=5)
        
        self.result_listbox = tk.Listbox(root, width=50, height=10)
        self.result_listbox.pack(pady=5)
    
    def check_spelling(self):
        input_word = self.entry.get().strip().lower()
        if not input_word:
            messagebox.showerror("Error", "Please enter a word!")
            return
        
        suggestions = get_suggestions(input_word, self.dictionary)
        self.result_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.result_listbox.insert(tk.END, suggestion)

# Main function
if __name__ == "__main__":
    # Replace 'dictionary.txt' with the path to the provided Pride and Prejudice dictionary
    dictionary_file = "dictionary.txt"
    dictionary_words = load_dictionary(dictionary_file)
    
    root = tk.Tk()
    app = SpellCheckerApp(root, dictionary_words)
    root.mainloop()
