import math
import nltk  # used to find edit-distance for user input with all the possible matches in the database
import mysql.connector
import operator


def print_int_list(some_list):
    ret = "("
    for i in some_list:
        ret += str(i)
        ret += ","
    ret = ret[:-1]
    ret += ")"
    return ret


def print_str_list(some_list):
    ret = "("
    for i in some_list:
        ret += "'"
        ret += i
        ret += "',"
    ret = ret[:-1]
    ret += ")"
    return ret


class Professor:

    def __init__(self, name, dict_of_focus_to_weight):
        self.name = name
        self.focus_to_weight_dict = self.update_to_standard_dict(dict_of_focus_to_weight.copy())
        self.adjacent = {}  # neighbor node  ->  edge weight

        # so the sum of all the weights of key-words for a professor is 100

    @staticmethod  # And we only consider the top ten weighted keywords
    def update_to_standard_dict(diction):
        if len(diction) <= 10:
            opt_dict = diction.copy()
        else:
            opt_dict = dict(sorted(diction.items(), key=operator.itemgetter(1), reverse=True)[:10])
        total = sum(opt_dict.values())
        for k in opt_dict.keys():
            opt_dict[k] = opt_dict[k] / total
            opt_dict[k] = round(opt_dict[k] * 100)
        return opt_dict

    def get_connections(self):
        return list(self.adjacent.keys())

    def get_name(self):
        return self.name

    # returns the weight of the edge between this professor and a neighbor
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_focuses(self):
        return self.focus_to_weight_dict.keys()

    def get_focus_weight(self, focus):
        return self.focus_to_weight_dict[focus]


class Graph:
    def __init__(self, fos_cursor, npmi_cursor):
        self.prof_name_dict = {}  # professor name string  ->  professor node
        self.num_vertices = 0
        self.focus_to_prof_names_dict = {}  # research focus string  ->  list of professor name strings
        self.fos_cursor = fos_cursor  # dataset about professors recorded
        self.npmi_cursor = npmi_cursor  # dataset about similarity between two words
        self.construct_graph()

    # print the information of the relation graph in a straight-forward way
    def __str__(self):
        ret = ""
        for name in self.prof_name_dict.keys():
            ret += name
            ret += ", whose neighbors are: { "
            node = self.get_professor_node(name)
            for neighbor in node.get_connections():
                ret += neighbor
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
            if focus not in self.focus_to_prof_names_dict:
                self.focus_to_prof_names_dict[focus] = [name]
            else:
                self.focus_to_prof_names_dict[focus].append(name)
        for other_prof in self.prof_name_dict.keys():
            if other_prof == name:
                continue
            edge_weight = self.calc_distance(new_vertex, self.get_professor_node(other_prof))
            self.add_edge(name, other_prof, edge_weight)
        return new_vertex

    def construct_graph(self):
        self.fos_cursor.execute("SELECT name FROM Professor")
        list_of_professors = list(self.fos_cursor.fetchall())
        for name in list_of_professors:
            self.fos_cursor.execute("SELECT keyword, occurrence FROM Keywords WHERE name = '%s'" % name[0])
            rows = list(self.fos_cursor.fetchall())
            dict_of_focus_to_weight = {}
            for r in rows:
                dict_of_focus_to_weight[r[0]] = r[1]
            self.add_professor_node(name[0], dict_of_focus_to_weight)

    # returns all the professor names of this graph
    def get_vertices(self):
        return self.prof_name_dict.keys()

    def get_professor_node(self, n):
        return self.prof_name_dict[n]

    def add_edge(self, frm, to, cost):
        self.prof_name_dict[frm].adjacent[to] = cost
        self.prof_name_dict[to].adjacent[frm] = cost

    # return the distance between two professor nodes based on their key words
    def calc_distance(self, prof_node1, prof_node2):
        value = 200
        focus1 = prof_node1.get_focuses()
        focus2 = prof_node2.get_focuses()
        focus1_list = print_str_list(focus1)
        focus2_list = print_str_list(focus2)
        self.npmi_cursor.execute("SELECT * FROM fos WHERE FoS_name in " + focus1_list)
        id1 = self.npmi_cursor.fetchall()
        self.npmi_cursor.execute("SELECT * FROM fos WHERE FoS_name in " + focus2_list)
        id2 = self.npmi_cursor.fetchall()
        id1 = {a[0]: a[1] for a in id1}
        id2 = {a[0]: a[1] for a in id2}
        id1_list = print_int_list(id1.keys())
        id2_list = print_int_list(id2.keys())
        self.npmi_cursor.execute("SELECT id1, id2, npmi FROM fos_npmi_springer " +
                                 "WHERE (id1 in " + id1_list + " AND id2 in " + id2_list + " )")
        sim_pairs = self.npmi_cursor.fetchall()
        sim_dict = {}
        for p in sim_pairs:
            sim_dict[(p[0], p[1])] = p[2]
        for a in id1.keys():
            max_factor = 0
            for b in id2.keys():
                if (a, b) in sim_dict:
                    s_score = sim_dict[(a, b)]
                elif (b, a) in sim_dict:
                    s_score = sim_dict[(b, a)]
                elif a == b:
                    s_score = 1
                else:
                    s_score = 0
                if s_score > max_factor:
                    max_factor = s_score
            if id1[a] not in prof_node1.get_focuses():
                continue
            value -= max_factor * prof_node1.get_focus_weight(id1[a])
        for b in id2.keys():
            max_factor = 0
            for a in id1.keys():
                if (b, a) in sim_dict:
                    s_score = sim_dict[(b, a)]
                elif (a, b) in sim_dict:
                    s_score = sim_dict[(a, b)]
                elif a == b:
                    s_score = 1
                else:
                    s_score = 0
                if s_score > max_factor:
                    max_factor = s_score
            if id2[b] not in prof_node2.get_focuses():
                continue
            value -= max_factor * prof_node2.get_focus_weight(id2[b])
        return round(value, 3)

    def populate_for_focus(self, focus):
        id_focus_dict = {}
        focus_id_dict = {}
        id_factor_dict = {}
        prof_factor_dict = {}
        self.npmi_cursor.execute("SELECT id FROM fos WHERE FoS_name='" + focus + "'")
        id = self.npmi_cursor.fetchone()
        if id is None:
            return {}
        id = id[0]
        self.npmi_cursor.execute("SELECT id1, id2, npmi FROM fos_npmi_springer " +
                                 "WHERE (id1 = " + str(id) + " OR id2 = " + str(id) + " )" +
                                 "AND npmi > 0.2")
        triple = self.npmi_cursor.fetchall()
        id_factor_dict[id] = 1
        for t in triple:
            if t[0] == id:
                id_factor_dict[t[1]] = t[2]
            else:
                id_factor_dict[t[0]] = t[2]
        ids = id_factor_dict.keys()
        ids = print_int_list(ids)
        self.npmi_cursor.execute("SELECT * FROM fos WHERE id in " + ids)
        pairs = self.npmi_cursor.fetchall()
        for p in pairs:
            id_focus_dict[p[0]] = p[1]
            focus_id_dict[p[1]] = p[0]
        focuses = focus_id_dict.keys()
        focuses = print_str_list(focuses)
        self.fos_cursor.execute("SELECT name, keyword FROM Keywords WHERE keyword in " + focuses)
        pairs = self.fos_cursor.fetchall()
        for p in pairs:
            node = self.get_professor_node(p[0])
            if p[1] not in node.get_focuses():
                continue
            if p[1] not in focus_id_dict:
                continue
            factor = id_factor_dict[focus_id_dict[p[1]]]
            if p[0] in prof_factor_dict:
                tmp = prof_factor_dict[p[0]]
                prof_factor_dict[p[0]] = max(factor * node.get_focus_weight(p[1]), tmp)
            else:
                prof_factor_dict[p[0]] = factor * node.get_focus_weight(p[1])
        return prof_factor_dict

    @staticmethod
    def merge_dicts(dict1, dict2):
        for k in dict2.keys():
            if k in dict1:
                dict1[k] += dict2[k]
            else:
                dict1[k] = dict2[k]
        return dict1

    # return a list of (name, int) pairs, sorted based on the int part,
    # larger value means more related to the input focus
    def rank_list_of_professors(self, focuses):
        rank_map = {}
        for focus in focuses:
            focus_map = self.populate_for_focus(focus)
            rank_map = self.merge_dicts(rank_map, focus_map)
        rank_list = list(zip(rank_map.keys(), rank_map.values()))
        rank_list.sort(key=lambda x: -x[1])
        return rank_list

    # a helper function for the Dijkstra's Algorithm, could be improved by using heap sort
    def min_distance_node(self, dist, sptset):
        math_min = math.inf
        min_name = ""
        for name in self.prof_name_dict.keys():
            if dist[name] < math_min and not sptset[name]:
                math_min = dist[name]
                min_name = name
        return min_name

    # input the name of a professor as a string, return related professors as a rank list
    def dijkstra(self, src):
        if src not in self.prof_name_dict.keys():
            min_edit_dist = 10.5
            for name in self.prof_name_dict.keys():
                if nltk.edit_distance(src, name) < min_edit_dist:
                    src = name
                    min_edit_dist = nltk.edit_distance(src, name)
            if min_edit_dist == 10.5:
                print("Please add this professor: " + src + " to the database before searching.")
                return {}

        dist_dict = {name: math.inf for name in self.prof_name_dict.keys()}
        dist_dict[src] = 0
        sptset = {name: False for name in self.prof_name_dict.keys()}
        # which stands for "shortest path tree"

        for count in range(5):
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            u = self.min_distance_node(dist_dict, sptset)
            sptset[u] = True
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for name in self.prof_name_dict.keys():
                if name not in self.get_professor_node(u).get_connections():
                    continue
                if not sptset[name] and dist_dict[name] > dist_dict[u] + self.get_professor_node(u).get_weight(
                        name):
                    dist_dict[name] = dist_dict[u] + self.get_professor_node(u).get_weight(name)
        return dist_dict

    # returns a rank list of related professor to the give professor based only on key words
    # Use Dijkstra's algorithm to return a list of (name, int) pairs,
    # sorted based on the int part, with smaller value meaning more closely related
    def related_professors(self, src_prof):
        dist_dict = self.dijkstra(src_prof)
        rank_list = []
        for prof in dist_dict:
            rank_list.append((prof, dist_dict[prof]))
        rank_list.sort(key=lambda x: x[1])
        return rank_list


if __name__ == '__main__':
    npmi_data = mysql.connector.connect(
        host="localhost",
        user="root",
        password="262956",
        database="forward",
    )
    npmi_cursor = npmi_data.cursor()
    print("npmi data connected")
    fos_data = mysql.connector.connect(
        host="104.198.163.126",
        user="root",
        password="yEBpALG6zHDoCFLn",
        database="project"
    )
    fos_cursor = fos_data.cursor()
    print("keywords data connected")
    relation_graph = Graph(fos_cursor, npmi_cursor)
    print("relation graph constructed")

    # to populate the website database, uncomment the following codes:
    #
    # fos_cursor.execute("SELECT keyword FROM Keywords")
    # rank_list = fos_cursor.fetchall()
    # for k in rank_list:
    #     print(k[0])
    #     rank_map = relation_graph.populate_for_focus(k[0])
    #     for r in rank_map.keys():
    #         fos_cursor.execute("INSERT INTO Similar (Keyword, Similar_Prof, Similar_Factor) " +
    #                            "VALUES ('" + k[0] + "', '" + r + "', " + str(rank_map[r]) + " )")
    #
    print(relation_graph.rank_list_of_professors(["security", "data"]))

    # to populate the website database, uncomment the following codes:
    #
    # for prof in relation_graph.prof_name_dict.keys():
    #     relation_list = relation_graph.related_professors(prof)
    #     for pair in relation_list:
    #         if pair[0] == prof:
    #             continue
    #         fos_cursor.execute("INSERT INTO Related (Prof, Related_Prof, Related_Factor) " +
    #                            "VALUES ('" + prof + "', '" + pair[0] + "', " + str(pair[1]) + " )")
    print(relation_graph.related_professors("Jiawei Han"))
    #
    print(relation_graph)
    # fos_data.commit()
