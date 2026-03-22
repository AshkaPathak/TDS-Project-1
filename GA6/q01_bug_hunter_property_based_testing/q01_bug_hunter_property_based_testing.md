# GA6 — Q1: The Bug Hunter (Property-Based Testing)

## Problem Summary
The task was to write a Hypothesis-based property test that distinguishes a buggy implementation of `sort_metrics(nums)` from the correct reference implementation. The function is expected to return a sorted copy of the input list in non-decreasing order while preserving all values. However, the provided implementation contains a hidden bug that is not caught by standard unit tests.

The buggy function is:
    def sort_metrics(nums):
      arr = nums[:]
      for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
          if arr[i] > arr[j] or (arr[i] == arr[j] and i % 2 == 0 and j == i + 1):
            arr[i], arr[j] = arr[j], arr[i]
      return arr

Basic unit tests such as:
    def test_basic_sorting_examples():
      assert sort_metrics([3, 1, 2]) == [1, 2, 3]
      assert sort_metrics([]) == []
      assert sort_metrics([5]) == [5]
do not expose the issue.

## Key Insight
The bug occurs when two adjacent elements are equal and located at positions where the first index is even. In such cases, the function unnecessarily swaps them:
(arr[i] == arr[j] and i % 2 == 0 and j == i + 1)
This introduces a stability violation. A correct sorting algorithm must preserve the relative order of equal elements. Python’s built-in sorted() function is stable, so it serves as the correct reference.

The challenge is that with plain integers, swapping equal values is invisible because identical numbers remain indistinguishable. Therefore, a stronger testing strategy is required.

## Strategy to Detect the Bug
To expose the bug, we:
1. Use custom objects instead of plain integers.
2. Compare objects based only on their numeric value (key).
3. Assign each object a unique identifier (tag) to track original order.
4. Force at least one pair of equal adjacent elements at indices 0 and 1.
5. Compare the output of the buggy function with Python’s stable sorted().

## Final Test Code
from hypothesis import given, strategies as st

class Metric:
    def __init__(self, key, tag):
        self.key = key
        self.tag = tag

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __eq__(self, other):
        return isinstance(other, Metric) and self.key == other.key

    def __repr__(self):
        return f"Metric({self.key}, {self.tag})"


@given(st.lists(st.integers(), min_size=2, max_size=10))
def test_sort_metrics_stability(nums):
    nums[1] = nums[0]
    metrics = [Metric(x, i) for i, x in enumerate(nums)]

    got = sort_metrics(metrics)
    expected = sorted(metrics)

    assert [m.tag for m in got] == [m.tag for m in expected]

## Step-by-Step Explanation
A custom class Metric is created where comparison depends only on key. Each object carries a tag representing its original position. Hypothesis generates random integer lists. The first two elements are forced to be equal to guarantee triggering the bug. The list is converted into Metric objects. The buggy function output is compared with Python’s stable sorted() output. Instead of comparing values, the test compares the order of tags. If the order differs, stability is violated and the test fails.

## Why This Works
The buggy implementation swaps equal adjacent elements at specific indices, breaking stability. The reference implementation preserves order. By tracking identity using tags, we make this difference observable. The test is strong because it targets the exact failure condition instead of relying on random chance.

## Conclusion
The issue in the function is not incorrect sorting of values but incorrect handling of equal elements. A naive property based on numeric sorting would fail to detect this. By designing a property that checks stability using custom objects, we reliably expose the bug. This demonstrates the power of property-based testing in uncovering subtle edge-case failures that traditional unit tests miss.

## Final Answer Submitted
from hypothesis import given, strategies as st

class Metric:
    def __init__(self, key, tag):
        self.key = key
        self.tag = tag

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __eq__(self, other):
        return isinstance(other, Metric) and self.key == other.key

    def __repr__(self):
        return f"Metric({self.key}, {self.tag})"


@given(st.lists(st.integers(), min_size=2, max_size=10))
def test_sort_metrics_stability(nums):
    nums[1] = nums[0]
    metrics = [Metric(x, i) for i, x in enumerate(nums)]

    got = sort_metrics(metrics)
    expected = sorted(metrics)

    assert [m.tag for m in got] == [m.tag for m in expected]
