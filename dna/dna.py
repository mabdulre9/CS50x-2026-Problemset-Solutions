import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit()

    # TODO: Read database file into a variable
    with open(sys.argv[1]) as file:
        database = list(csv.DictReader(file))

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    STRs = list(database[0].keys())
    STRs.remove("name")

    STR_dict = dict.fromkeys(STRs, 0)

    for i in range(len(STRs)):
        STR_dict[STRs[i]] = str(longest_match(sequence,STRs[i]))

    # TODO: Check database for matching profiles

    for i in range(len(database)):
        match = True
        for j in range(len(STRs)):
            if database[i][STRs[j]] != STR_dict[STRs[j]]:
                match = False
                break
        if match == True:
            print(database[i]["name"])
            break
    else:
        print("No match")








    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
