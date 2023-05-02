import sys
from cs50 import SQL



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookclub.db")


# Query for all books suggested
book_list = db.execute("SELECT * FROM suggestions")

# Create list of all books suggested
books = []
for row in book_list:
    books.append(row["suggestion_1"])
    books.append(row["suggestion_2"])

# Query for all votes
votes = db.execute("SELECT * FROM votes")


def main():
    """ Hold a 'runoff' election to see which book is the winner """

    # Initialize global variables
    global candidate_count
    global candidates
    global voter_count
    global preferences

    # Number of candidates. The number of books is always twice the readers
    candidate_count = len(books)

    # Initialize list of candidate dictionaries
    candidates = []

    # Populate the list with candidate dictionaries
    for i in range(candidate_count):
        candidate = {
            "name": books[i],
            "votes": 0,
            "eliminated": False
        }
        candidates.append(candidate)

    # Number of voters
    voter_count = len(db.execute("SELECT * FROM users"))

    # Create a 2-D list comprehension to index into to find the voter's preference for each candidate
    # preferences[i][j] is jth preference for voter i
    # There are only a max of "3" preferences per voter
    preferences = []
    for i in range(voter_count):
        preferences.append([])
        for j in range(3):
            preferences[i].append(j)

    # Make list comprehension for all voters' votes.
    vote_list = []
    votes = db.execute("SELECT * FROM votes")
    for i in range(voter_count):
        vote_list.append([])
        vote_list[i].append(votes[i]["first"])
        vote_list[i].append(votes[i]["second"])
        vote_list[i].append(votes[i]["third"])

    # Keep querying for votes.  Index into vote_list to fill out preferences
    for i in range(voter_count):

        # Query for each rank
        for j in range(3):
            name = vote_list[i][j]

            # Record vote
            vote(i, j, name)

    # Keep holding runoff until winner exists
    while True:

        # Calculate votes given remaining candidates
        tabulate()

        # Check if election has been won
        won = print_winner()
        if won != False:
            return won

        # Eliminate last place candidates
        min = find_min()
        tie = is_tie(min)

        # If tie, all tied books win
        if tie == True:
            return "It's a tie, select winners at random!"

        # Eliminate anyone with the minimum number of votes
        eliminate(min)

        # Reset vote counts back to zero
        for i in range(candidate_count):
            candidates[i]["votes"] = 0


def vote(voter, rank, name):
    """ Record preference if vote is valid """

    for i in range(candidate_count):

        if name == candidates[i]["name"]:
            preferences[voter][rank] = i
            return

    return


def tabulate():
    """ Tabulate votes for non-eliminated candidates """

    for i in range(voter_count):

        for j in range(candidate_count):

            if candidates[preferences[i][j]]["eliminated"] == False:

                candidates[preferences[i][j]]["votes"] += 1
                break

    return


def print_winner():
    """ Print the winner of the election, if there is one """

    for i in range(candidate_count):

        if candidates[i]["votes"] > voter_count/2:
            return candidates[i]["name"]

    return False


def find_min():
    """ Return the minimum number of votes any candidate has """

    # Start with min being the max and increment it down to the least amount of votes
    min = voter_count
    for i in range(candidate_count):

        if candidates[i]["eliminated"] == False and candidates[i]["votes"] < min:

            min = candidates[i]["votes"]

    return min


def is_tie(min):
    """ Return true if election is tied between all candidates, false otherwise """

    for i in range(candidate_count):

        if candidates[i]["eliminated"] == False and candidates[i]["votes"] != min:
            return False

    return True


def eliminate(min):
    """ Eliminate candidate or candidates in last place """

    for i in range(candidate_count):

        if candidates[i]["votes"] == min:

            candidates[i]["eliminated"] = True

    return


if __name__ == "__main__":
    main()