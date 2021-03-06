import vk_api
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class User(object):

    def __init__(self, login='+79856211067', password='Sport1998!', id=61373152, id_point_out=None):
        """

        :param login:
        :param password:
        :param id:
        :param id_point_out: id друга, коорого надо выделить
        """
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
        self.api = vk_session.get_api()
        self.nodes = None
        self.count_nodes = None
        self.adj_matrix = None
        # self.G = nx.Graph()
        self.id = id
        # self.match_dict = None
        self.flag_self = False
        self.index_point_out = None
        self.id_point_out = id_point_out

    def set_friends(self):
        d = self.api.friends.get(user_id=self.id)
        if self.flag_self:
            d['items'].append(self.id)

        self.nodes = np.array(d['items'])
        self.count_nodes = len(self.nodes)
        print('count nodes: ', self.count_nodes)
        self.adj_matrix = pd.DataFrame(0, dtype='int64', index=self.nodes, columns=self.nodes)

    def set_relations(self):
        for i in range(self.count_nodes):
            if (self.id_point_out is not None) and (self.nodes[i] == self.id_point_out):
                print('i= ', i)
                print('find point out id')
                self.index_point_out = i
            if i % 20 == 0:
                print('function set relations progress: ', i / self.count_nodes)
            try:
                d = self.api.friends.get(user_id=self.nodes[i])
            except:
                continue
            cur_friends = np.array(d['items'])
            common_friends = np.intersect1d(self.nodes, cur_friends, assume_unique=True)
            self.adj_matrix.loc[self.nodes[i], common_friends] = 1
            self.adj_matrix.loc[common_friends, self.nodes[i]] = 1

id_point_out = None
U = User()
U.set_friends()
U.set_relations()
G = nx.from_numpy_matrix(U.adj_matrix.values)
if id_point_out is not None:
    node_color = ['b']*U.count_nodes
    node_color[U.index_point_out] = 'r'
else:
    node_color = 'b'
nx.draw(G, with_labels=False, font_weight='bold', node_size=10, node_color=node_color)
plt.savefig('network_kek.png')
nx.write_gpickle(G, "kek.gpickle")
# plt.show()
