from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Penalty constants
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

# Load the dictionary and log the number of words
dictionary_words = load_dictionary("dictionary.txt")
print(f"Loaded {len(dictionary_words)} words from the dictionary.")

# API to get suggestions
@app.route('/suggest', methods=['POST'])
def suggest():
    try:
        # Debugging: Check if request contains JSON
        if not request.is_json:
            print("Request is not JSON")
            return jsonify({"error": "Invalid request format"}), 400

        input_word = request.json.get("word", "").strip().lower()
        print(f"Received word: {input_word}")  # Log the input word

        if not input_word:
            return jsonify({"error": "No word provided"}), 400

        # Check if the dictionary is loaded
        if not dictionary_words:
            print("Error: Dictionary is empty!")
            return jsonify({"error": "Dictionary not loaded."}), 500

        # Calculate penalties and generate suggestions
        penalties = [(word, calculate_penalty(input_word, word)) for word in dictionary_words]
        penalties.sort(key=lambda x: x[1])
        suggestions = [word for word, _ in penalties[:10]]

        print(f"Suggestions: {suggestions}")  # Log suggestions
        return jsonify({"suggestions": suggestions})
    except Exception as e:
        print(f"Error occurred: {e}")  # Log any unexpected errors
        return jsonify({"error": "An internal server error occurred."}), 500

# Main route to serve the webpage
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
