import random

# Original examples for the Opening Hours intent
original_examples = [
    "what time does the restaurant open?",
    "when does the restaurant start serving?",
    "tell me opening hours?"
]


# Function to generate variations with typos and mistakes
def generate_typos_mistakes(sentence):
    variants = []
    # Split the sentence into words
    words = sentence.split()

    for _ in range(3):  # Generate 3 variations for each sentence
        new_sentence = []
        for word in words:
            # Introduce typos or mistakes randomly
            if random.random() < 0.3:  # Introduce a mistake with 30% probability
                # Simulate a simple typo/mistake (for demonstration purposes)
                # You can add more sophisticated typo generation logic here
                new_word = introduce_typo(word)
                new_sentence.append(new_word)
            else:
                new_sentence.append(word)

        # Join the words back to form a sentence
        variants.append(' '.join(new_sentence))

    return variants


# Function to introduce a simple typo (for demonstration purposes)
# def introduce_typo(word):
#     if len(word) <= 2:
#         return word  # Don't modify very short words
#     else:
#         # Introduce a simple typo by swapping two characters randomly
#         idx1, idx2 = random.sample(range(len(word)), 2)
#         word_list = list(word)
#         word_list[idx1], word_list[idx2] = word_list[idx2], word_list[idx1]
#         return ''.join(word_list)

def introduce_typo(word):
    if len(word) <= 2:
        return word  # Don't modify very short words
    else:
        # Define a list of possible typo operations
        typo_operations = [
            lambda w: w[:-1],  # Deleting the last character
            lambda w: w[1:],  # Deleting the first character
            lambda w: w[::-1],  # Reversing the word
            lambda w: w + w[-1],  # Doubling the last character
            lambda w: w[:2] + w[-1] + w[2:],  # Swapping middle character with the last character
            lambda w: ''.join(random.sample(w, len(w)))  # Randomly shuffling characters
            # Add more sophisticated typo operations as needed
        ]

        # Randomly select and apply a typo operation to the word
        typo_function = random.choice(typo_operations)
        return typo_function(word)


# Generate variations for the Opening Hours intent examples
generated_variations = []
for example in original_examples:
    variations = generate_typos_mistakes(example)
    generated_variations.extend(variations)

# Print the generated variations
for idx, variation in enumerate(generated_variations):
    print(f"{idx + 1}. {variation}")
