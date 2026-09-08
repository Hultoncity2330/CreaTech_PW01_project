def max_elt(numbers: list[int]) -> int:
    if len(numbers) == 0:
        raise Exception("List is empty, so there's nothing to compare.")
    
    max: int = numbers[0]
    for n in numbers:
        if n > max:
            max = n
    return max


def idx_max_elt(numbers: list[int]) -> int:
    if len(numbers) == 0:
            raise Exception("List is empty, so there's nothing to compare.")

    max: int = numbers[0]
    idx: int = 0
    for i in range(len(numbers)):
        if numbers[i] > max:
            max = numbers[i]
            idx = i
    return idx


def min_elt(numbers: list[int]) -> int:
    if len(numbers) == 0:
        raise Exception("List is empty, so there's nothing to compare.")
    
    min: int = numbers[0]
    for n in numbers:
        if n < min:
            min = n
    return min


def idx_min_elt(numbers: list[int]) -> int:
    if len(numbers) == 0:
            raise Exception("List is empty, so there's nothing to compare.")

    min: int = numbers[0]
    idx: int = 0
    for i in range(len(numbers)):
        if numbers[i] < min:
            min = numbers[i]
            idx = i
    return idx


def difference(numbers: list[int]) -> int:
    return max_elt(numbers) - min_elt(numbers)


def sum_list(numbers: list[int]) -> int:
    sum: int = 0
    for n in numbers:
        sum += n
    return sum


def count_above(numbers: list[int], threshold: int) -> int:
    if len(numbers) == 0:
        raise Exception("List is empty.")

    count = 0
    for n in numbers:
        if n > threshold:
            count += 1
    return count


def even_booleans(numbers: list[int]) -> list[bool]:
    if len(numbers) == 0:
        raise Exception("List is empty.")

    even_bool: list[bool] = [False] * len(numbers)
    for i in range(len(numbers)):
        if numbers[i] % 2 == 0:
            even_bool[i] = True
    return even_bool


def only_even(numbers: list[int]) -> list[int]:
    if len(numbers) == 0:
        raise Exception("List is empty.")

    even_list: list[int] = []
    for n in numbers:
        if n % 2 == 0:
            even_list.append(n)
    return even_list


def idx_only_even(numbers: list[int]) -> list[int]:
    if len(numbers) == 0:
        raise Exception("List is empty.")

    idx_even_list: list[int] = []
    for (idx, n) in enumerate(numbers):
        if n % 2 == 0:
            idx_even_list.append(idx)
    return idx_even_list


def Newton_method(n: int, epsilon: float = 1e-6) -> float:
    if n < 0:
        raise ValueError("sqrt not defined on negative values")

    guess: float = n / 2
    error: float = abs(guess * guess - n)

    max_attempts: int = 1000
    attempts: int = 0

    while error > epsilon and attempts < max_attempts:
        guess = (guess + n / guess) / 2
        error = abs(guess * guess - n)
        attempts += 1

    if attempts >= max_attempts and error > epsilon:
        raise RuntimeError("Attempts limit reached.")

    print("Total iterations :", attempts)
    return guess


def increment(n: int) -> int:
    return n + 1


def square(n: int) -> int:
    return n * n


def apply_to_list(numbers: list[int], fct) -> list[int]:
    if len(numbers) == 0:
        raise Exception("List is empty.")

    applied_list = [0] * len(numbers)
    for (i, n) in enumerate(numbers):
        applied_list[i] = fct(numbers[i])
    return applied_list


empty: list[int] = []
numbers: list[int] = [4, 6, 78, 12, 6, 32, 38, 87, 4, 12, 74, 78]

# print(count_above([4, 8, 2, 12], 5))
# print(count_above(numbers, 10))
# print(idx_only_even(numbers))
# print("The square root of 2 is approximatly", Newton_method(2))
print(apply_to_list(numbers, increment))
print(apply_to_list(numbers, square))
