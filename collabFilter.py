
"""
Executing code: 
Python collabFilter.py ratings-dataset.tsv Kluver 'The Fugitive' 10

Changes Log
- Oct. 26, 2015
1. due date extend to Oct. 27, 2015, final check
2. recovery judgement for invalid input file and user id

- Oct. 24, 2015
1. change logic for updated requirement, If all similarities are same, sort them by descending order of user id for K nearest neighbors.

- Oct. 22, 2015
1. remove tips description
2. remove parameters judgement
3. add judgement for predict when denominator is 0

- Oct. 21, 2015
1. get rid of round function

- Oct. 20, 2015
1. modify file name as firstname_lastname_collabFilter.py
2. modify executing code based on new filename
3. add parameter validation inside initialize method
4. add exit state description

"""
import sys
import math
import os

class Collaborate_Filter:
    def __init__(self, input_file_name, user_id, movie, k):
        self.input_file_name = input_file_name
        self.user_id = user_id
        self.movie = movie
        self.k = k
        self.dataset = None
        self.uu_dataset = None
        self.ii_dataset = None

    def initialize(self):
        """
        Initialize and check parameters

        """

        # check file exist and if it's a file or dir
        if not os.path.isfile(self.input_file_name):
            self.quit("Input file doesn't exist or it's not a file")
        

        # load data
        self.dataset, self.uu_dataset, self.ii_dataset = self.load_data(self.input_file_name)

        
        # check if user exist
        users = self.uu_dataset.keys()
        if self.user_id not in users:
            self.quit("User ID doesn't exist")

        """
        # check if movie exist
        items = self.ii_dataset.keys()
        if self.movie not in items:
            self.quit("Movie doesn't exist")

        # check k validation
        max_k = len(users) - 1
        min_k = 1
        if self.k < min_k or self.k > max_k:
            self.quit("k value for k nearest neighbors is not valid, it should be inside [" + str(min_k) + ", " +  str(max_k) +"]")
        """
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """                             Pearson Correlation                              """
    """                                                                              """    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def pearson_correlation(self, user1, user2):
        result = 0.0
        user1_data = self.uu_dataset[user1]
        user2_data = self.uu_dataset[user2]

        rx_avg = self.user_average_rating(user1_data)
        ry_avg = self.user_average_rating(user2_data)
        sxy = self.common_items(user1_data, user2_data)

        top_result = 0.0
        bottom_left_result = 0.0
        bottom_right_result = 0.0
        for item in sxy:
            rxs = user1_data[item]
            rys = user2_data[item]
            top_result += (rxs - rx_avg)*(rys - ry_avg)
            bottom_left_result += pow((rxs - rx_avg), 2)
            bottom_right_result += pow((rys - ry_avg), 2)
        bottom_left_result = math.sqrt(bottom_left_result)
        bottom_right_result = math.sqrt(bottom_right_result)

        result = top_result/(bottom_left_result * bottom_right_result)
        return result

    def user_average_rating(self, user_data):
        avg_rating = 0.0
        size = len(user_data)
        for (movie, rating) in user_data.items():
            avg_rating += float(rating)
        avg_rating /= size * 1.0
        return avg_rating

    def common_items(self, user1_data, user2_data):
        result = []
        ht = {}
        for (movie, rating) in user1_data.items():
            ht.setdefault(movie, 0)
            ht[movie] += 1
        for (movie, rating) in user2_data.items():
            ht.setdefault(movie, 0)
            ht[movie] += 1
        for (k, v) in ht.items():
            if v == 2:
                result.append(k)
        return result

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """                             K Nearest Neighbors                              """
    """                                                                              """    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def k_nearest_neighbors(self, user, k):
        neighbors = []
        result = []
        for (user_id, data) in self.uu_dataset.items():
            if user_id == user:
                continue
            upc = self.pearson_correlation(user, user_id)
            # upc = round(upc, 11)
            neighbors.append([user_id, upc])
            # neighbors_ht.setdefault(user_id, upc)   # assume there are not duplicate user_id
        # sorted_neighbors_ht = sorted(neighbors_ht.iteritems(), key=lambda neighbors_ht : neighbors_ht[1], reverse=True)  
        sorted_neighbors = sorted(neighbors, key=lambda neighbors: (neighbors[1], neighbors[0]), reverse=True)   # - for desc sort

        # testitems = [('a', 3), ('o', 5), ('g', 6), ('c', 1), ('b', 1)]
        # sorted_testitems = sorted(testitems, key=lambda testitems: (-testitems[1], testitems[0]))  # - for desc sort

        for i in range(k):
            if i >= len(sorted_neighbors):
                break
            result.append(sorted_neighbors[i])
        return result

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """                                  Predict                                     """
    """                                                                              """    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def predict(self, user, item, k_nearest_neighbors):
        valid_neighbors = self.check_neighbors_validattion(item, k_nearest_neighbors)
        if not len(valid_neighbors):
            return 0.0
        top_result = 0.0
        bottom_result = 0.0
        for neighbor in valid_neighbors:
            neighbor_id = neighbor[0]
            neighbor_similarity = neighbor[1]   # Wi1
            rating = self.uu_dataset[neighbor_id][item] # rating i,item
            top_result += neighbor_similarity * rating
            bottom_result += neighbor_similarity
        result = top_result/bottom_result
        return result

    def check_neighbors_validattion(self, item, k_nearest_neighbors):
        result = []
        for neighbor in k_nearest_neighbors:
            neighbor_id = neighbor[0]
            # print item
            if item in self.uu_dataset[neighbor_id].keys():
                result.append(neighbor)
        return result

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """                             Helper Functions                                 """
    """                                                                              """    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def load_data(self, input_file_name):
        """
        load data and return three outputs for extention purpose
        only one output is enough in practice (uu_dataset)

        """
        input_file = open(input_file_name, 'rU')
        dataset = []
        uu_dataset = {}
        ii_dataset = {}
        for line in input_file:
            row = str(line)
            row = row.split("\t")
            row[2] = row[2][:-1]
            dataset.append(row)

            """
            user-user dataset: [0: Movie Name  1: Rating]

            """
            uu_dataset.setdefault(row[0], {})
            uu_dataset[row[0]].setdefault(row[2], float(row[1]))
            # uu_dataset[row[0]].append([row[2],row[1]])

            """
            item-item dataset: [0: user id  1: Rating]

            """
            ii_dataset.setdefault(row[2], {})
            ii_dataset[row[2]].setdefault(row[0], float(row[1]))
            # ii_dataset[row[2]].append([row[0], row[1]])
        return dataset, uu_dataset, ii_dataset

    def display(self, k_nearest_neighbors, prediction):
        for neighbor in k_nearest_neighbors:
            print neighbor[0], neighbor[1]
        print "\n"
        print prediction

    def quit(self, err_desc):
        tips = "\n" + "TIPS: " + "\n"   \
                + "--------------------------------------------------------" + "\n" \
                + "Pragram name: lingzhe_teng_collabFilter.py" + "\n" \
                + "First parameter: Input File, e.g. ratings-dataset.tsv" + "\n" \
                + "Second parameter:  User ID, e.g. Kluver" + "\n" \
                + "Thrid parameter:  Movie, e.g. The Fugitive" + "\n" \
                + "Fourth parameter: K, e.g. 10" + "\n" \
                + "--------------------------------------------------------" + "\n" \
                + "Note:" + "\n" \
                + "Please use double quotation marks, such as \"USER\'S ID\" or \"MOVIEW\'S NAME\", for User ID and Moview parameters" + "\n" 


        raise SystemExit('\n'+ "PROGRAM EXIT: " + err_desc + ', please check your input' + '\n' + tips)



if __name__ == '__main__':

    # publish
    input_file_name = sys.argv[1]   # ratings-dataset.tsv
    user_id = sys.argv[2]   # user name
    movie = sys.argv[3]     # movie name
    k = int(sys.argv[4])    # k neighbors

    # test
    # input_file_name = "ratings-dataset.tsv"
    # user_id = "Kluver"
    # movie = 'The Fugitive'
    # k = 10

    cf = Collaborate_Filter(input_file_name, user_id, movie, k)
    cf.initialize()
        

    # cf.pearson_correlation(user_id, user_id)
    # cf.pearson_correlation("Flesh", "Nathan_Studanski")

    k_nearest_neighbors = cf.k_nearest_neighbors(user_id, k)
    # cf.k_nearest_neighbors("Flesh", 2)

    prediction = cf.predict(user_id, movie, k_nearest_neighbors)
    cf.display(k_nearest_neighbors, prediction)

    # test
    # print input_file_name
    # print user_id
    # print movie
    # print k









