from interface.models import Role, PossiblePrivilege, Privilege, ListPrivilege


class DAG():
    def __init__(self):
        self.priv_list = dict()
        for priv in Privilege.objects.all():
            if priv.role.role_name not in self.priv_list.keys():
                self.priv_list[priv.role.role_name] = [priv.priv.priv_name]
            else:
                self.priv_list[priv.role.role_name].append(priv.priv.priv_name)

    def create_sketch(self):
        node = []
        node_name = []
        for role in self.priv_list:
            node_name.append([role, set(self.priv_list[role])])
            node.append(set(self.priv_list[role]))
            
        d = 0
        for i in range(len(node)):
            for j in range(i + 1, len(node)):
                interc = node[i] & node[j]
                if(len(interc) < min(len(node[i]), len(node[j])) and len(interc) > 0 and interc not in node):
                    dummy_name = 'dummy' + str(d)
                    node_name.append([dummy_name,interc])
                    node.append(interc)
                    d += 1

        node.sort(key=len, reverse=True)
        name = ["" for i in range(len(node))]
        for i in range(len(node)):
            for j in range(len(node)):
                if(node_name[i][1] == node[j]):
                    name[j] = node_name[i][0]
        adj_mat = [[] for i in range(len(node))]
        tot = [set() for i in range(len(node))]

        self.dfs(adj_mat, node, tot, 0)

        ListPrivilege.objects.all().delete()
        for i in range(len(node)):
            for priv in node[i]:
                ListPrivilege(role=name[i], priv=priv).save()

        # return adj_mat, node


    def dfs(self, adj_mat, node, tot, cur):
        if(cur == len(node)):
            return
        if(len(tot[cur]) > 0):
            self.dfs(adj_mat, node, tot, cur + 1)
            return
        
        for i in range(cur + 1, len(node)):
            self.dfs(adj_mat, node, tot, i)
            if(tot[i].issubset(node[cur]) and (not tot[i].issubset(tot[cur]))):
                if(i not in adj_mat[cur]):
                    adj_mat[cur].append(i)
                tot[cur] = set.union(tot[cur],tot[i])
        
        node[cur] = node[cur] - tot[cur]
        tot[cur] = set.union(tot[cur],node[cur])
    
    # def delete_node(self, node):
    #     self.priv_list.pop(node)
    #     create_sketch()

    # def delete_priv(self, priv):
    #     for key, val in self.priv_list:
    #         if(priv in val):
    #             val.remove(priv)
    #     create_sketch()
    
    # def add_priv_to_node(self, node, priv):
    #     self.priv_list[node].append(priv)
    #     create_sketch()

    # def del_priv_from_node(self, node, priv):
    #     self.priv_list[node].remove(priv)
    #     create_sketch()
