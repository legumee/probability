WORDLE_LEN = 5


# returns a list of the answers (from the Wordle source file of all answers) that haven't been
# used yet (up to March 6th)
def get_answers_left():
    wordle_history = open('PastWordles.txt')
    answer_data = open('wordle-nyt-answers-alphabetical.txt')

    wordle_history = wordle_history.read()
    wordle_history = wordle_history.splitlines()

    # puts all past wordles into a list
    past_answers = []
    for wordle in wordle_history:
        wordle = wordle.split(' ')
        past_answers.append(wordle[-1].lower())

    # puts all wordles not found in past into a list
    answers_left = []
    for answer in answer_data:
        answer = answer.strip()
        if answer not in past_answers:
            answers_left.append(answer)

    return answers_left


# given a list of words, returns a dictionary of the probabilities for each letter to appear in a
# given word from the word list
def get_p_letter(words):  # probability that each letter occurs in a 5-letter word
    priors = {}
    total_letters = 0

    # count how many times each letter appears in all words
    for answer in words:
        for ch in answer:
            if ch not in priors:
                priors[ch] = 0
            priors[ch] += 1
            total_letters += 1

    # makes all counts into probabilities by dividing by total (normalization)
    for prob_letter in priors:
        priors[prob_letter] = priors[prob_letter] / total_letters

    return priors


# given a position (e.g. first letter -> position = 0), returns a dictionary of the likelihood of
# each letter appearing in that position based on given list of words
def get_p_letter_given_position(position, words):  # probability that a letter will be in a certain position
    likelihood = {}
    sum = 0

    # using rejection sampling to count how many times each letter appears in position
    for word in words:
        if word[position] not in likelihood:
            likelihood[word[position]] = 0
        sum += 1
        likelihood[word[position]] += 1

    # makes all counts into probabilities by dividing by total (normalization)
    for prior in likelihood:
        likelihood[prior] = likelihood[prior] / sum
    return likelihood


# returns the 5 letters with the highest probabilities of appearing in a given wordle
def get_5_highest(p_letter):
    sorted_freq = sorted(p_letter, key=lambda letter: p_letter[letter], reverse=True)
    return sorted_freq[:WORDLE_LEN]


# PART 1:
# from word list, finds the words that maximize the probability that each letter appears
# in the true wordle answer
def maximize_letters(p_letter, words):
    five_highest_letters = (get_5_highest(p_letter))

    optimal_words = []
    for word in words:
        word = word.strip()
        num_contains = 0
        for i in range(WORDLE_LEN):  # counts how many of the 5 most frequent letters appear in word
            if five_highest_letters[i] in word:
                num_contains += 1
        if num_contains == WORDLE_LEN:  # if word has all of the 5 most common letters, append to optimal_words
            optimal_words.append(word)

    return optimal_words


# PART 2:
# from list of words, find the singular word that maximizes the probability that each letter
# appears in the right order in the true wordle answer, using Bayesian logic
def maximize_order_given_letters(words, p_letter, answers_left):
    p_letter_given_position = []

    # for each letter position, finds a dictionary of the probability of each letter given position
    for i in range(5):
        p_letter_given_position.append(get_p_letter_given_position(i, answers_left))

    max_p = 0
    max_guess = ''
    for word in words:
        p_guess = 1  # cumulative probability
        for i in range(5):
            if word[i] in p_letter_given_position[i]:
                p_guess *= ((p_letter_given_position[i][word[i]] * 0.2) / p_letter[word[i]])  # Bayes used here
            else:  # if letter doesn't have a frequency in that position, multiply by extremely small number
                p_guess *= 0.0000000000001
        if p_guess > max_p:  # update most optimal word if p_guess exceeds previous max
            max_p = p_guess
            max_guess = word
    return max_guess


def get_best_wordle():
    wordle_history = open('PastWordles.txt')

    wordle_history = wordle_history.read()
    wordle_history = wordle_history.splitlines()

    # puts all past wordles into a list
    past_answers = []
    for wordle in wordle_history:
        wordle = wordle.split(' ')
        past_answers.append(wordle[-1].lower())

    allowed_guesses = open('wordle-nyt-allowed-guesses.txt')

    p_letter = get_p_letter(past_answers)

    words = maximize_letters(p_letter, allowed_guesses)
    print("Words that optimize letters:")
    print(words)

    max_guess = maximize_order_given_letters(words, p_letter, past_answers)
    print("Optimal first word: " + max_guess)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_best_wordle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
