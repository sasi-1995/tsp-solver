class Vertex:
    def __init__(self, identifier):
        self.identifier = identifier
        self.neighbours = dict()

    def __hash__(self):
        return hash(self.identifier)

    def connect(self, neighbour, cost):
        self.neighbours[neighbour] = cost

    def __str__(self):
        return str(self.identifier)

    def __repr__(self):
        return repr(self.identifier)


class Graph:
    def __init__(self):
        self.vertices = dict()
        self.initial_vertex = None
        self.path = []
        self.answer = float("inf")

    def _get_or_create_vertex(self, identifier):
        if identifier not in self.vertices:
            self.vertices[identifier] = Vertex(identifier)
        return self.vertices[identifier]

    def connect(self, v1, v2, cost):
        vertex1 = self._get_or_create_vertex(v1)
        vertex2 = self._get_or_create_vertex(v2)
        vertex1.connect(vertex2, cost)
        vertex2.connect(vertex1, cost)

    def __str__(self):
        return "\n".join(["{} -> {}".format(vertex, self.vertices[vertex].neighbours) for vertex in self.vertices])

    def solve(self, starting_vertex, visited=None, path=None, cost_to_reach_source=0):
        if path is None:
            path = []
        if self.initial_vertex is None:
            self.initial_vertex = self.vertices[starting_vertex]
        if starting_vertex not in self.vertices:
            print("Invalid Starting Point has to be one of: {}".format(self.vertices))

        if visited is None:
            visited = set()
        if len(visited) == len(self.vertices) - 1:
            cost = cost_to_reach_source + self.vertices[starting_vertex].neighbours.get(self.initial_vertex,
                                                                                        float("inf"))
            if cost < self.answer:
                self.path = list(path)
                self.path.append(starting_vertex)
                self.path.append(self.initial_vertex.identifier)
                self.answer = cost

        visited.add(self.vertices[starting_vertex])
        path.append(starting_vertex)
        for neighbour in self.vertices[starting_vertex].neighbours:
            if neighbour not in visited:
                cost_to_reach_neighbour = cost_to_reach_source + self.vertices[starting_vertex].neighbours[neighbour]
                self.solve(neighbour.identifier, visited, path, cost_to_reach_neighbour)
        path.remove(starting_vertex)
        visited.remove(self.vertices[starting_vertex])


class Problem:
    def __init__(self):
        self.cost_mapping = []
        self.start = ''


class ProblemParser:
    def __init__(self, problem_file):
        self.problem_file = problem_file

    def parse(self):
        problem_instance = Problem()
        with open(self.problem_file, 'r') as infile:
            starting_vertex = infile.readline().strip("\n")
            problem_instance.start = starting_vertex
            line = infile.readline().strip("\n")
            while line != '':
                vertex1, vertex2, cost = line.split(" ")
                problem_instance.cost_mapping.append([vertex1, vertex2, int(cost)])
                line = infile.readline().strip("\n")

        return problem_instance


class Solution:
    def main(self, problem):
        graph = Graph()
        for entry in problem.cost_mapping:
            graph.connect(*entry)
        print("*" * 50)
        print("Graph is:")
        print(graph)
        print("*" * 50)
        print("Starting Vertex is: {}".format(problem.start))
        graph.solve(problem.start)
        print("Minimum Cost is: {}".format(graph.answer))
        print("The best path is: {}".format(graph.path))


def setup():
    problem_parser = ProblemParser('problem.txt')
    problem = problem_parser.parse()
    solution = Solution()
    solution.main(problem)


if __name__ == "__main__":
    setup()
