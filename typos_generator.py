import random
import yaml


def generate_typos_mistakes(sentence):
    variants = []
    words = sentence.split()

    for _ in range(3):
        new_sentence = []
        for word in words:
            if random.random() < 0.3:
                new_word = introduce_typo(word)
                new_sentence.append(new_word)
            else:
                new_sentence.append(word)

        variants.append(' '.join(new_sentence))
    return variants


def introduce_typo(word):
    if len(word) <= 2:
        return word
    else:
        typo_operations = [
            lambda w: w[:-1],  # delete last char
            lambda w: w[1:],  # deleting  first char
            lambda w: w[::-1],  # reversing word
            lambda w: w + w[-1],  # doubling last char
            lambda w: w[:2] + w[-1] + w[2:],  # swap middle char with last char
            lambda w: ''.join(random.sample(w, len(w)))  # randomly shuffle chars
        ]

        typo_function = random.choice(typo_operations)
        return typo_function(word)


def create_examples_with_mistakes(file_name, intent_name):
    file_path = f'data/nlu/{file_name}.yml'

    with open(file_path, 'r') as file:
        yaml_content = file.read()

    data = yaml.safe_load(yaml_content)

    examples = None
    for item in data.get('nlu', []):
        if item.get('intent') == intent_name:
            examples = item.get('examples', '').strip().split('\n')[1:]

    generated_variations = []
    for example in examples:
        variations = generate_typos_mistakes(example)
        generated_variations.extend(variations)

    for variation in generated_variations:
        print(variation)


# PARAMETERS: file_name, intent_name
create_examples_with_mistakes("opening_hours_nlu", "check_open_now")
