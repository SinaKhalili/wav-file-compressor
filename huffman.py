from collections import defaultdict
import heapq
from math import log


class HuffNode:
    """
    A huffman tree node

    Comparison dunders are frequency based
    """

    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = self.right = None

    def __gt__(self, other):
        return self.frequency > other.frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __ge__(self, other):
        return self.frequency >= other.frequency

    def __le__(self, other):
        return self.frequency <= other.frequency

    def __repr__(self):
        return """
        <{self.symbol}:{self.frequency}>
        """


def create_heap_and_counts(input_string):
    heap = []
    counts = defaultdict(int)

    for char in input_string:
        counts[char] += 1

    for key in counts:
        huff_node = HuffNode(key, counts[key])
        heapq.heappush(heap, huff_node)

    return heap, counts


def merge(heap):
    while len(heap) > 1:
        min_1 = heapq.heappop(heap)
        min_2 = heapq.heappop(heap)

        min_merge = HuffNode("MERGED", min_1.frequency + min_2.frequency)
        min_merge.left = min_2
        min_merge.right = min_1

        heapq.heappush(heap, min_merge)


def get_code_words(root):
    cw = {}

    def get_codes(root, code, code_words):
        """
        Mutates `code_words`

        Recursive code finder, based on
        """
        if root is None:
            return
        if root.symbol != "MERGED":
            code_words[root.symbol] = code

        get_codes(root.left, code + "0", code_words)
        get_codes(root.right, code + "1", code_words)

    get_codes(root, "", cw)
    return cw


def get_entropy(test_string):
    heap, counts = create_heap_and_counts(test_string)
    merge(heap)
    code_words = get_code_words(heapq.heappop(heap))
    probabilities = [
        (elem, count / len(test_string)) for (elem, count) in counts.items()
    ]

    entropy = 0
    for symbol, probability in probabilities:
        entropy += probability * log(1 / probability, 2)

    return entropy


def get_avg_code_word_len(test_string):
    heap, counts = create_heap_and_counts(test_string)
    merge(heap)
    code_words = get_code_words(heapq.heappop(heap))
    probabilities = [
        (elem, count / len(test_string)) for (elem, count) in counts.items()
    ]

    code_len = 0
    for symbol, probability in probabilities:
        code_len += probability * len(code_words[symbol])

    return code_len


def get_message(test_string):
    """
    Return the huffman encoded message as a bit string
    """
    heap, counts = create_heap_and_counts(test_string)
    merge(heap)
    code_words = get_code_words(heapq.heappop(heap))

    message = ""
    for char in test_string:
        message += code_words[char]

    return message
