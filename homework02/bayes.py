import math
from collections import Counter, defaultdict


class NaiveBayesClassifier:

    def __init__(self, alpha=0.05):
        """задаем параметры"""
        self.alpha = alpha
        self.class_counts = Counter()
        self.feature_counts = defaultdict(lambda: defaultdict(int))
        self.class_total_words = defaultdict(int)
        self.vocab = set()
        self.classes = set()

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        for text, label in zip(X, y):
            words = (text or "").split()
            self.class_counts[label] += 1
            self.classes.add(label)
            for word in words:
                self.feature_counts[label][word] += 1
                self.class_total_words[label] += 1
                self.vocab.add(word)
        # Общее количество уникальных слов
        self.d = len(self.vocab)

    def _calculate_log_prob(self, word, label):
        """Вероятность слова для класса со сглаживанием Лапласа"""
        n_word = self.feature_counts[label].get(word, 0)
        total = self.class_total_words[label]
        return math.log((n_word + self.alpha) / (total + self.alpha * self.d))

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predictions = []
        total_classes = sum(self.class_counts.values())
        for text in X:
            words = text.split() if text else []
            max_log_prob = -float("inf")
            best_class = None

            for label in self.classes:
                # Логарифм априорной вероятности класса
                log_prob = math.log(self.class_counts[label] / total_classes)

                for word in words:
                    log_prob += self._calculate_log_prob(word, label)

                if log_prob > max_log_prob:
                    max_log_prob = log_prob
                    best_class = label

            predictions.append(best_class or max(self.classes, key=lambda x: self.class_counts[x]))
        return predictions

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        y_pred = self.predict(X_test)
        correct = sum(pred == true for pred, true in zip(y_pred, y_test))
        return correct / len(y_test)
