import random


class TestManager:

    def __init__(self, words):
        self.words = words

    def choosen_words(self):
        mywords = []
        for _ in range(100):
            mywords.append(random.choice(self.words))

        return " ".join(mywords)

    def calculate_cpm_wpm(self, chars, seconds):
        cpm = (60 * chars) / seconds
        wpm = cpm / 5

        return int(cpm), int(wpm)


    def calculate_speed(self, typed_words, choosen_words, chars):
        correct_cpm = chars

        for i in range(len(typed_words)):
            if typed_words[i] != choosen_words[i]:
                correct_cpm -= len(choosen_words[i])

        wpm = correct_cpm / 5

        return correct_cpm, int(wpm)
