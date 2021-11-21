import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # builds the frontier and adds explored nodes to a list
    explored_list = explore(source, target)

    # returns None if people are not connected
    if explored_list is None:
        return None

    # recreates the shortest path from the explored nodes list
    solution = reconstruct_path(explored_list)

    return solution


# builds a queue frontier and uses it to create a list of explored nodes
def explore(start, target):
    # print("Exploring...")

    f = QueueFrontier()

    f.add(Node(start, None, None))

    explored_nodes = []

    # this loop gets the next node in the frontier, adds all unexplored neighbors to the frontier,
    # and then removes the current node from the frontier
    while True:
        try:
            # pop off the node you're going to explore
            current_node = f.remove()

            """
            # check if the node you're currently exploring is the target, if so, add to list and break
            if current_node.state == target:
                explored_nodes.append(current_node)
                break
            """
            # get neighbors for that node and iterate through them
            for x in neighbors_for_person(current_node.state):
                # add here a test to see if neighbor is target, to optimize search
                if x[1] == target:
                    explored_nodes.append(Node(x[1], current_node, x[0]))
                    # print(f"Explored {len(explored_nodes)} nodes.")
                    return explored_nodes
                # if the node is not in the frontier and is not in the explored list, add it to the frontier
                # IMPORTANT each node needs to have a state (person), parent (previous node), action (movie)
                if not f.contains_state(x[1]) and not (any(x[1] == node.state for node in explored_nodes)):
                    f.add(Node(x[1], current_node, x[0]))
            
            # when done with adding neighbors, add node to explored list
            explored_nodes.append(current_node)
        
        # this should run only when it has went through all possible layers of neighbors but didn't find target
        except:
            # print(f"Explored {len(explored_nodes)} nodes.")
            return None
    
    # print(f"Explored {len(explored_nodes)} nodes.")
    return explored_nodes

# go through the nodes in reverse to find the path solution
def reconstruct_path(node_list):
    # this reverses the list
    node_list.reverse()

    # initialize empty list for storing the reconstructed path
    reconstructed_path = []
    
    # start from the first node in the reversed list
    current_node = node_list[0]

    # loop through node list and stop when you reach a node with no parent
    while current_node.parent is not None:
        # when reconstructing path, each step is a (movie_id, person_id) tuple
        reconstructed_path.append((current_node.action, current_node.state))
        # then move on to the next
        current_node = current_node.parent

    reconstructed_path.reverse()
    
    return reconstructed_path


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
