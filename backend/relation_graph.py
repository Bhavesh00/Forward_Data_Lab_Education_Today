import math


class Professor:
    def update_to_standard_dict(self, dict):
        all = sum(dict.values())
        for k in dict.keys():
            dict[k] = dict[k] / all
            dict[k] = round(dict[k] * 100)
        return dict

    def __init__(self, name, dict_of_focus_to_weight):
        self.name = name
        self.focus_to_weight_dict = dict_of_focus_to_weight.copy()
        self.focus_to_weight_dict = self.update_to_standard_dict(self.focus_to_weight_dict)
        self.adjacent = {}

    def add_neighbor(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return list(self.adjacent.keys())

    def get_name(self):
        return self.name

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_focuses(self):
        return self.focus_to_weight_dict.keys()

    def get_focus_weight(self, focus):
        return self.focus_to_weight_dict[focus]


class Graph:
    def __init__(self):
        self.prof_name_dict = {}
        self.num_vertices = 0
        self.focus_to_prof_name_dict = {}

    def __str__(self):
        ret = ""
        for name in self.prof_name_dict.keys():
            ret += str(name)
            ret += ", whose neighbors are: { "
            node = self.get_professor_node(name)
            for neighbor in node.get_connections():
                ret += str(neighbor)
                ret += " : "
                ret += str(node.get_weight(neighbor))
                ret += "; "
            ret += "} \n"
        return ret

    def add_professor_node(self, name, dict_of_focus_to_weight):
        self.num_vertices += 1
        new_vertex = Professor(name, dict_of_focus_to_weight)
        self.prof_name_dict[name] = new_vertex
        for focus in dict_of_focus_to_weight.keys():
            if focus not in self.focus_to_prof_name_dict:
                self.focus_to_prof_name_dict[focus] = [name]
            else:
                self.focus_to_prof_name_dict[focus].append(name)
            for other_prof in self.focus_to_prof_name_dict[focus]:
                if other_prof == name:
                    continue
                edge_weight = dict_of_focus_to_weight[focus] + self.prof_name_dict[other_prof].get_focus_weight(focus)
                self.add_edge(name, other_prof, edge_weight)
        return new_vertex

    def get_professor_node(self, n):
        return self.prof_name_dict[n]

    def rank_list_of_professors(self, focus):
        # return a list of (name, int) pairs, sorted based on the int part,
        # larger value means more related to the input focus
        rank_list = []
        for prof in self.focus_to_prof_name_dict[focus]:
            rank_list.append((prof, self.get_professor_node(prof).focus_to_weight_dict[focus]))
        rank_list.sort(key=lambda x: -x[1])
        return rank_list

    def add_edge(self, frm, to, cost=0):
        if to in self.prof_name_dict[frm].get_connections():
            self.prof_name_dict[frm].adjacent[to] -= cost
            self.prof_name_dict[to].adjacent[frm] -= cost
        else:
            self.prof_name_dict[frm].add_neighbor(to, 200 - cost)
            self.prof_name_dict[to].add_neighbor(frm, 200 - cost)

    def min_distance_node(self, dist, sptSet):
        min = math.inf
        min_name = ""
        for name in self.prof_name_dict.keys():
            if dist[name] < min and sptSet[name] == False:
                min = dist[name]
                min_name = name
        return min_name

    def get_vertices(self):
        return self.prof_name_dict.keys()

    def dijkstra(self, src):
        dist_dict = {name: math.inf for name in self.prof_name_dict.keys()}
        dist_dict[src] = 0
        sptSet = {name: False for name in self.prof_name_dict.keys()}
        # which stands for "shortest path tree"

        for count in range(self.num_vertices):
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            u = self.min_distance_node(dist_dict, sptSet)
            sptSet[u] = True
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for name in self.prof_name_dict.keys():
                if name not in self.get_professor_node(u).get_connections():
                    continue
                if sptSet[name] == False and dist_dict[name] > dist_dict[u] + self.get_professor_node(u).get_weight(
                        name):
                    dist_dict[name] = dist_dict[u] + self.get_professor_node(u).get_weight(name)
        return dist_dict

    def related_professors(self, src_prof):
        # Use Dijkstra's algorithm to return a list of (name, int) pairs,
        # sorted based on the int part, with smaller value meaning more closely related
        dist_dict = self.dijkstra(src_prof)
        rank_list = []
        for prof in dist_dict:
            rank_list.append((prof, dist_dict[prof]))
        rank_list.sort(key=lambda x: x[1])
        return rank_list


if __name__ == '__main__':
    relation_graph = Graph()
    # tom = {"algo": 5, "machine learning": 10}
    # bob = {"algo": 7, "machine learning": 2, "data mining": 3}
    # alice = {"security": 10, "data mining": 3}
    # relation_graph.add_professor_node("Tom", tom)
    # relation_graph.add_professor_node("Bob", bob)
    # relation_graph.add_professor_node("Alice", alice)
    # print(relation_graph)
    # print(relation_graph.rank_list_of_professors("algo"))
    # print(relation_graph.related_professors("Tom"))

    test1 = {'concepts': 1, 'data': 1, 'data mining': 1, 'databases': 1, 'gathered data': 1, 'methods': 1, 'mining': 1,
             'techniques': 1}
    test2 = {'data mining': 2, 'databases': 1}
    test3 = {'data mining': 3}
    relation_graph.add_professor_node(('Jiawei Han', 'University of Illinois at Urbana Champaign'), test1)
    relation_graph.add_professor_node(('test name', 'test institution'), test2)
    relation_graph.add_professor_node(('test name 2', 'test institution'), test3)
    print(relation_graph.related_professors(('Jiawei Han', 'University of Illinois at Urbana Champaign')))
