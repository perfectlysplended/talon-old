#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from rapidfuzz import process
from rapidfuzz.distance import Opcodes, Opcode, Levenshtein_cpp, Levenshtein_py


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class Levenshtein:
    @staticmethod
    def distance(*args, **kwargs):
        dist1 = Levenshtein_cpp.distance(*args, **kwargs)
        dist2 = Levenshtein_py.distance(*args, **kwargs)
        assert dist1 == dist2
        return dist1

    @staticmethod
    def similarity(*args, **kwargs):
        dist1 = Levenshtein_cpp.similarity(*args, **kwargs)
        dist2 = Levenshtein_py.similarity(*args, **kwargs)
        assert dist1 == dist2
        return dist1

    @staticmethod
    def normalized_distance(*args, **kwargs):
        dist1 = Levenshtein_cpp.normalized_distance(*args, **kwargs)
        dist2 = Levenshtein_py.normalized_distance(*args, **kwargs)
        assert isclose(dist1, dist2)
        return dist1

    @staticmethod
    def normalized_similarity(*args, **kwargs):
        dist1 = Levenshtein_cpp.normalized_similarity(*args, **kwargs)
        dist2 = Levenshtein_py.normalized_similarity(*args, **kwargs)
        assert isclose(dist1, dist2)
        return dist1


def test_empty_string():
    """
    when both strings are empty this is a perfect match
    """
    assert Levenshtein.distance("", "") == 0
    assert Levenshtein.distance("", "", weights=(1, 1, 0)) == 0
    assert Levenshtein.distance("", "", weights=(1, 1, 2)) == 0
    assert Levenshtein.distance("", "", weights=(1, 1, 5)) == 0
    assert Levenshtein.distance("", "", weights=(3, 7, 5)) == 0


def test_cross_type_matching():
    """
    strings should always be interpreted in the same way
    """
    assert Levenshtein.distance("aaaa", "aaaa") == 0
    assert Levenshtein.distance("aaaa", ["a", "a", "a", "a"]) == 0
    # todo add support in pure python
    assert Levenshtein_cpp.distance("aaaa", [ord("a"), ord("a"), "a", "a"]) == 0
    assert Levenshtein_cpp.distance([0, -1], [0, -2]) == 1


def test_word_error_rate():
    """
    it should be possible to use levenshtein to implement a word error rate
    """
    assert Levenshtein.distance(["aaaaa", "bbbb"], ["aaaaa", "bbbb"]) == 0
    assert Levenshtein.distance(["aaaaa", "bbbb"], ["aaaaa", "cccc"]) == 1


def test_simple_unicode_tests():
    """
    some very simple tests using unicode with scorers
    to catch relatively obvious implementation errors
    """
    s1 = "ÁÄ"
    s2 = "ABCD"
    assert Levenshtein.distance(s1, s2) == 4  # 2 sub + 2 ins
    assert Levenshtein.distance(s1, s2, weights=(1, 1, 0)) == 2  # 2 sub + 2 ins
    assert (
        Levenshtein.distance(s1, s2, weights=(1, 1, 2)) == 6
    )  # 2 del + 4 ins / 2 sub + 2 ins
    assert Levenshtein.distance(s1, s2, weights=(1, 1, 5)) == 6  # 2 del + 4 ins
    assert Levenshtein.distance(s1, s2, weights=(1, 7, 5)) == 12  # 2 sub + 2 ins
    assert Levenshtein.distance(s2, s1, weights=(1, 7, 5)) == 24  # 2 sub + 2 del

    assert Levenshtein.distance(s1, s1) == 0
    assert Levenshtein.distance(s1, s1, weights=(1, 1, 0)) == 0
    assert Levenshtein.distance(s1, s1, weights=(1, 1, 2)) == 0
    assert Levenshtein.distance(s1, s1, weights=(1, 1, 5)) == 0
    assert Levenshtein.distance(s1, s1, weights=(3, 7, 5)) == 0


def test_Editops():
    """
    basic test for Levenshtein_cpp.editops
    """
    assert Levenshtein_cpp.editops("0", "").as_list() == [("delete", 0, 0)]
    assert Levenshtein_cpp.editops("", "0").as_list() == [("insert", 0, 0)]

    assert Levenshtein_cpp.editops("00", "0").as_list() == [("delete", 1, 1)]
    assert Levenshtein_cpp.editops("0", "00").as_list() == [("insert", 1, 1)]

    assert Levenshtein_cpp.editops("qabxcd", "abycdf").as_list() == [
        ("delete", 0, 0),
        ("replace", 3, 2),
        ("insert", 6, 5),
    ]
    assert Levenshtein_cpp.editops("Lorem ipsum.", "XYZLorem ABC iPsum").as_list() == [
        ("insert", 0, 0),
        ("insert", 0, 1),
        ("insert", 0, 2),
        ("insert", 6, 9),
        ("insert", 6, 10),
        ("insert", 6, 11),
        ("insert", 6, 12),
        ("replace", 7, 14),
        ("delete", 11, 18),
    ]

    ops = Levenshtein_cpp.editops("aaabaaa", "abbaaabba")
    assert ops.src_len == 7
    assert ops.dest_len == 9


def test_Opcodes():
    """
    basic test for Levenshtein_cpp.opcodes
    """
    assert Levenshtein_cpp.opcodes("", "abc") == Opcodes(
        [Opcode(tag="insert", src_start=0, src_end=0, dest_start=0, dest_end=3)], 0, 3
    )


def test_mbleven():
    """
    test for regressions to previous bugs in the cached Levenshtein implementation
    """
    assert 2 == Levenshtein.distance("0", "101", score_cutoff=1)
    assert 2 == Levenshtein.distance("0", "101", score_cutoff=2)
    assert 2 == Levenshtein.distance("0", "101", score_cutoff=3)

    match = process.extractOne(
        "0", ["101"], scorer=Levenshtein_cpp.distance, processor=None, score_cutoff=1
    )
    assert match is None
    match = process.extractOne(
        "0", ["101"], scorer=Levenshtein_py.distance, processor=None, score_cutoff=1
    )
    assert match is None
    match = process.extractOne(
        "0", ["101"], scorer=Levenshtein_cpp.distance, processor=None, score_cutoff=2
    )
    assert match == ("101", 2, 0)
    match = process.extractOne(
        "0", ["101"], scorer=Levenshtein_py.distance, processor=None, score_cutoff=2
    )
    assert match == ("101", 2, 0)
    match = process.extractOne(
        "0", ["101"], scorer=Levenshtein_cpp.distance, processor=None, score_cutoff=3
    )
    assert match == ("101", 2, 0)
    match = process.extractOne(
        "0", ["101"], scorer=Levenshtein_py.distance, processor=None, score_cutoff=3
    )
    assert match == ("101", 2, 0)


if __name__ == "__main__":
    unittest.main()
