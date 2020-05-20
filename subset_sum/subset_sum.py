import datetime
import numpy
import multiprocessing


def subset_sum(l, mass):
    """
    Recursive subset sum algorithm for identifying sets of substructures that make up a given mass. Do not supply 0
    values to this function, it will think these are unique subsets and therefore yield double the number of solutions.

    :param l: A list of masses from which to identify subsets.

    :param mass: The target mass of the sum of the substructures.

    :return: Generates of lists containing the masses of valid subsets.
    """

    # we've overshot the target mass (no solution)
    if mass < 0:
        return

    # base case, yield a solution
    elif (sum(l) - mass) == 0:
        yield l
        return

    # there are no (more) masses
    elif len(l) == 0:
        return

    # can we sum up to the target value with the remaining values? - recursive call
    for subset in subset_sum(l[1:], mass):
        yield subset
    for subset in subset_sum(l[1:], mass - l[0]):
        yield [l[0]] + subset


def subset_sum_inexact(l, mass, toll=0.001):
    """
    Recursive subset sum algorithm for identifying sets of substructures that make up a given mass. We may define
    toll, which allows for non-exact solutions. Do not supply 0 values to this function, it will think these are
    unique subsets and therefore yield double the number of solutions.

    :param l: A list of masses from which to identify subsets.

    :param mass: The target mass of the sum of the substructures.

    :param toll: The allowable deviation of the sum of subsets from the target mass.

    :return: Generates of lists containing the masses of valid subsets.
    """
    
    # we've overshot the target mass (no solution)
    if mass < -toll:
        return

    # base case, yield a solution
    elif abs(sum(l) - mass) <= toll:
        yield l
        return

    # there are no (more) masses & mass is not at target
    elif len(l) == 0:
        return

    # can we sum up to the target value with the remaining values? - recursive call
    for subset in subset_sum_inexact(l[1:], mass):
        yield subset
    for subset in subset_sum_inexact(l[1:], mass - l[0]):
        yield [l[0]] + subset


def find_path(l, dp, n, mass, path=[]):
    """
    Recursive solution for backtracking through the dynamic programming boolean matrix. All possible subsets are found

    :param l: A list of masses from which to identify subsets.

    :param mass: The target mass of the sum of the substructures.

    :param dp: The dynamic programming boolean matrix.

    :param n: The size of l.

    :param path: List for keeping track of the current subset.

    :return: Generates of lists containing the masses of valid subsets.
    """

    # base case - the path has generated a correct solution
    if mass == 0:
        yield sorted(path)
        return

    # stop running when we overshoot the mass
    elif mass < 0:
        return

    # can we sum up to the target value using the remaining masses? recursive call
    elif dp[n][mass]:
        yield from find_path(l, dp, n-1, mass, path)
        path.append(l[n-1])

        yield from find_path(l, dp, n-1, mass - l[n-1], path)
        path.pop()


def subset_sum_dp(l, mass):
    """
    Dynamic programming implementation of subset sum. Note that, whilst this algorithm is pseudo-polynomial, the
    backtracking algorithm for obtaining all possible subsets has exponential complexity and so remains unsuitable
    for large input values.

    :param l: A list of masses from which to identify subsets.

    :param mass: The target mass of the sum of the substructures.

    :return: Generates of lists containing the masses of valid subsets.
    """
    n = len(l)

    # initialise dynamic programming array
    dp = numpy.ndarray([n+1, mass+1], bool)

    # subsets can always equal 0
    for i in range(n+1):
        dp[i][0] = True

    # empty subsets do not have non-zero sums
    for i in range(mass):
        dp[0][i+1] = False

    # fill in the remaining boolean matrix
    for i in range(n):
        for j in range(mass+1):
            if j >= l[i]:
                dp[i+1][j] = dp[i][j] or dp[i][j-l[i]]
            else:
                dp[i+1][j] = dp[i][j]

    # backtrack through the matrix recursively to obtain all solutions
    return find_path(l, dp, n, mass)


def subset_sum_parallel(l, mass, processes=None):
    """
    Dynamic programming implementation of subset sum. Note that, whilst this algorithm is pseudo-polynomial, the
    backtracking algorithm for obtaining all possible subsets has exponential complexity and so remains unsuitable
    for large input values.

    :param l: A list of masses from which to identify subsets.

    :param mass: The target mass of the sum of the substructures.

    :param processes: The number of processes to utilise for generating the dp table.

    :return: Generates of lists containing the masses of valid subsets.
    """
    n = len(l)

    # initialise dynamic programming array
    dp = numpy.ndarray([n+1, mass+1], bool)

    # subsets can always equal 0
    for i in range(n+1):
        dp[i][0] = True

    # empty subsets do not have non-zero sums
    for i in range(mass):
        dp[0][i+1] = False

    # fill in the remaining boolean matrix
    with multiprocessing.Pool(processes=processes) as pool:
    for i in range(n):
        for j in range(mass+1):
            if j >= l[i]:
                dp[i+1][j] = dp[i][j] or dp[i][j-l[i]]
            else:
                dp[i+1][j] = dp[i][j]

    # backtrack through the matrix recursively to obtain all solutions
    return find_path(l, dp, n, mass)


if __name__ == "__main__":
    l = [i + 1 for i in range(49)]
    s = 75

    print("M1 Integer")
    i = 0
    start = datetime.datetime.now()
    for item in subset_sum(l, s):
        i += 1  # print(item)
    print(datetime.datetime.now() - start)
    print(i)
    print("---")

    print("M1 Approximate")
    i = 0
    start = datetime.datetime.now()
    for item in subset_sum_inexact(l, s):
        i += 1  # print(item)
    print(datetime.datetime.now() - start)
    print(i)
    print("---")

    print("M2 Integer")
    i = 0
    start = datetime.datetime.now()
    for item in subset_sum_dp(l, s):
        i += 1  # print(item)
    print(datetime.datetime.now() - start)
    print(i)
    print("---")

    print("M2 Parallel")
    i = 0
    start = datetime.datetime.now()
    for item in subset_sum_parallel(l, s):
        i += 1  # print(item)
    print(datetime.datetime.now() - start)
    print(i)
    print("---")
