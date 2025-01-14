import random
import utils

def choose_word(words):
    return random.choice(words)

def display_word(word, guessed_letters):
    return ''.join([letter if letter in guessed_letters else '■' for letter in word])

def play_game(words, difficulty):
    lives = {'легкий': 7, 'средний': 5, 'сложный': 3}[difficulty]
    word = choose_word(words)
    guessed_letters = set()
    record = 0

    while lives > 0:
        print(display_word(word, guessed_letters))
        print(f"Количество жизней: {'♥' * lives}")

        guess = input("Назовите букву или слово целиком: ").strip().lower()

        if len(guess) == 1 and guess.isalpha():
            if guess in word:
                guessed_letters.add(guess)
            else:
                lives -= 1
                print("Неправильно. Вы теряете жизнь.")
        elif guess == word:
            print(f"Слово отгадано: {word}")
            print("Вы выиграли! Приз в студию!")
            record += 1
            break
        else:
            print("Некорректный ввод. Попробуйте еще раз.")

    if lives == 0:
        print(f"Вы проиграли. Загаданное слово было: {word}")

    return record

def main():
    words = utils.load_words('words.txt')
    if not words:
        return

    record_file = 'record.txt'
    current_record = utils.load_record(record_file)
    total_record = 0

    while True:
        difficulty = input("Выберите уровень сложности (легкий, средний, сложный): ").strip().lower()
        if difficulty not in ['легкий', 'средний', 'сложный']:
            print("Некорректный ввод. Попробуйте еще раз.")
            continue

        total_record += play_game(words, difficulty)

        if total_record > current_record:
            utils.save_record(record_file, total_record)
            current_record = total_record

        play_again = input("Хотите сыграть еще раз? (да/нет): ").strip().lower()
        if play_again != 'да':
            break

    print(f"Ваш текущий рекорд: {current_record}")

if __name__ == "__main__":
    main()