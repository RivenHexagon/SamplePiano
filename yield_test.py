def create_2pow(n):
    pows = range(n)
    for i in pows:
        yield 2**i
    print("done\n")

if __name__ == '__main__':
    mygen = create_2pow(8)
    for i in mygen:
        print(i)

''' END '''

