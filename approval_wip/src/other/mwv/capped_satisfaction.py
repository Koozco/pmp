#
#
#
#


def calculateNCSAforOneVoter(committee_size, number_of_representatives, q=1.0):
    numerator = number_of_representatives - (committee_size - number_of_representatives)
    if q == 1.0:
        denominator = (1.0 * committee_size)
    else:
        denominator = committee_size ** q
    return numerator / denominator


def foo(committee_size, number_of_representatives, q):

    y = committee_size
    x = number_of_representatives

    a = calculateNCSAforOneVoter(y, x, q=q)
    origScore = 2 * a

    # remove one candidate from the committee that is approved only by the second voter
    b = calculateNCSAforOneVoter(y-1, x, q=q)
    c = calculateNCSAforOneVoter(y-1, x-1, q=q)
    newScore = b + c

    print(f"committee size: {y}, representatives: {x}, {x}: origScore: {origScore}")
    print(f"committee size: {y-1}, representatives: {x}, {x-1}: origScore: {newScore}")
    print()

    pass


def main():
    q = 0.2
    q = 1

    foo(committee_size=10, number_of_representatives=9, q=q)
    foo(committee_size=10, number_of_representatives=6, q=q)
    foo(committee_size=10, number_of_representatives=5, q=q)
    foo(committee_size=10, number_of_representatives=2, q=q)

    pass




if __name__ == '__main__':
    main()
