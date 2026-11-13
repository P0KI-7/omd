import math


class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        self._vocabulary = {}
        self.lowercase = lowercase
        self.ngram_size = ngram_size

    def add_word(self, word):
        if word in self._vocabulary:
            return self._vocabulary[word]
        else:
            self._vocabulary[word] = len(self._vocabulary)
            return self._vocabulary[word]

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        if self.ngram_size == 1:
            return text.split()
        elif self.ngram_size == 2:
            text_split = text.split()
            return [(text_split[i-1] + ' ' + text_split[i]) for i in range(1, len(text_split))]

    def fit(self, corpus):
        set_corpus = set(token for text in corpus for token in self.tokenize(text))

        if len(set_corpus) > 0:
            self._vocabulary = {}
            for text in corpus:
                for token in self.tokenize(text):
                    self.add_word(token)
        else:
            raise ValueError('corpus пустой!')

    def transform(self, corpus):
        if not self._vocabulary:
            raise RuntimeError('CountVectorizer не обучен')

        ans = []

        for text in corpus:
            if text.strip() == '':
                ans.append([])
                continue

            tek_ans = [0] * len(self._vocabulary)
            for word in self.tokenize(text):
                if word in self._vocabulary:
                    tek_ans[self._vocabulary[word]] += 1
            ans.append(tek_ans)

        return ans

    def get_feature_names(self):
        return [token for token in self._vocabulary.keys()]

    def fit_transform(self, corpus):
        self.fit(corpus)
        return self.transform(corpus)

    @property
    def vocabulary(self):
        return self._vocabulary.copy()

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}

    @vocabulary.setter
    def vocabulary(self, value):
        self._vocabulary = value



    def to_dict(self):
        state = {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self.vocabulary,
        }
        return state

    @classmethod
    def from_dict(cls, state):

        temp = cls(lowercase=state['lowercase'], ngram_size=state['ngram_size'])
        temp.vocabulary = state['vocabulary']

        return temp



class BinaryVectorizer(CountVectorizer):


    def transform(self, corpus):
        if not self._vocabulary:
            raise RuntimeError('CountVectorizer не обучен')

        ans = []

        for text in corpus:
            if text.strip() == '':
                ans.append([])
                continue

            tek_ans = [0] * len(self._vocabulary)
            set_text = self.tokenize(text)

            if len(set_text) < len(self._vocabulary):
                for word in set_text:
                    if word in self._vocabulary:
                        tek_ans[self._vocabulary[word]] = 1
            else:
                for key in self._vocabulary.keys():
                    if key in set_text:
                        tek_ans[self._vocabulary[key]] = 1
            ans.append(tek_ans)

        return ans

class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase=True, ngram_size=1, use_idf=True):
        super().__init__(lowercase=lowercase, ngram_size=ngram_size)
        self.use_idf = use_idf
        self._idf = []

    @property
    def idf(self):
        return list(self._idf)

    def fit(self, corpus):
        new_vocabulary = {}
        vocab_for_idf = {} # словарь частот
        documents_count = len(corpus)

        for text in corpus:
            tokens = self.tokenize(text)

            for token in tokens:
                if token not in new_vocabulary: # можно через add_word
                    new_vocabulary[token] = len(new_vocabulary)

            for token in set(tokens):
                vocab_for_idf[token] = (
                    vocab_for_idf.get(token, 0) + 1
                )

        if not new_vocabulary:
            raise ValueError('corpus не содержит токенов')

        self._vocabulary = new_vocabulary

        if self.use_idf:
            self._idf = [
                math.log(
                    (documents_count + 1) /
                    (vocab_for_idf.get(word, 0) + 1)
                ) + 1
                for word in self.get_feature_names()
            ]
        else:
            self._idf = []

        return self

    def transform(self, corpus):
        if not self._vocabulary:
            raise RuntimeError('TfidfVectorizer не обучен')

        size = len(self._vocabulary)

        if self.use_idf and len(self._idf) != size:
            raise RuntimeError('TfidfVectorizer не обучен')

        result = []

        for text in corpus:
            tokens = self.tokenize(text)
            counts = [0] * size
            known_words_count = 0 # общее число известных слов

            for token in tokens:
                index = self._vocabulary.get(token)
                if index is not None:
                    counts[index] += 1
                    known_words_count += 1

            row = [0.0] * size

            if known_words_count > 0:
                for index, count in enumerate(counts):
                    if count == 0:
                        continue

                    tf = count / known_words_count

                    if self.use_idf:
                        row[index] = tf * self._idf[index]
                    else:
                        row[index] = tf

            result.append(row)

        return result

    @classmethod
    def from_config(cls, config=None):
        config = config or {}

        return cls(
            lowercase=config.get('lowercase', True),
            ngram_size=config.get('ngram_size', 1),
            use_idf=config.get('use_idf', True),

        )

class KeywordExtractor:
    def __init__(self, vectorizer, top_n=3):
        self.vectorizer = vectorizer
        self.top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError('top_n должен быть целым числом > 0')

        self._top_n = value

    def fit(self, corpus):
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus):
        matrix = self.vectorizer.transform(corpus)
        feature_names = self.vectorizer.get_feature_names()

        result = []

        for row in matrix:
            pairs = [
                (word, weight)
                for word, weight in zip(feature_names, row)
                if weight > 0
            ]

            pairs.sort(key=lambda item: (-item[1], item[0]))
            result.append(pairs[:self.top_n])

        return result

# Обучающие сообщения
TRAIN_CORPUS = [
    'Марс сигнал сигнал',
    'Марс пыль',
    'Марс сигнал антенна',
]
# Сообщения для проверки
CHECK_CORPUS = [
    'СИГНАЛ шум сигнал',
    'антенна пыль',
    'марс марс марс',
    'комета', '',
]


def demo():
    print('=' * 70,'\n')
    print('1. Веса TF-IDF')

    tfidf = TfidfVectorizer.from_config({})

    count_matrix = CountVectorizer().fit_transform(TRAIN_CORPUS)
    tfidf_matrix = tfidf.fit_transform(TRAIN_CORPUS)

    print('слова:', tfidf.get_feature_names())
    print('idf:', tfidf.idf)
    print('матрица частот:', count_matrix)
    print('матрица TF-IDF:', tfidf_matrix)

    idf_copy = tfidf.idf
    idf_copy.clear()

    print('idf после очистки:', tfidf.idf)

    print('\n','=' * 70,'\n')
    print('2. Настройки и новый fit()')

    tf = TfidfVectorizer.from_config({
        'lowercase': False,
        'use_idf': False,
    })

    tf_matrix = tf.fit_transform([
        'Марс марс',
        'МАРС сигнал',
    ])

    print('cлова:', tf.get_feature_names())
    print('idf:', tf.idf)
    print('матрица TF:', tf_matrix)

    tfidf.fit(['Венера облака'])

    print('после fit на ["Венера облака"]:')
    print('слова:', tfidf.get_feature_names())
    print('idf:', tfidf.idf)
    print(
        'матрица для ["Марс Венера облака"]:',
        tfidf.transform(["Марс Венера облака"])
    )

    print('\n','=' * 70,'\n')
    print('3. Ключевые слова')

    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(TRAIN_CORPUS)

    print('top_n=2:')
    print(extractor.extract(CHECK_CORPUS))

    extractor.top_n = 1

    print('top_n=1:')
    print(extractor.extract(CHECK_CORPUS))

    try:
        extractor.top_n = 0
    except ValueError as error:
        print('ValueError при top_n=0:', error)


if __name__ == '__main__':
    demo()