import numpy as np

class OneHotModel:
    def __init__(self):
        self.set_of_functions = set([])

    @staticmethod
    def get_functions(trace):
        def get_function_name(call):
            return (call.split('('))[0].replace(" ", "")
        functions = trace.split('</NXT\>')
        functions = set(map(get_function_name, functions))
        return functions

    def fit(self, traces):
        for trace in traces:
            functions = self.get_functions(trace)
            self.set_of_functions.update(functions)
        self.set_of_functions = list(self.set_of_functions)
        self.set_of_functions.sort()

    def generate_embedding(self, trace):
        def get_index(func):
            return self.set_of_functions.index(func)

        functions = self.get_functions(trace)
        embedding = list(set(map(get_index, functions)))
        one_hot = np.zeros(len(self.set_of_functions))
        for idx in embedding:
            one_hot[idx] = 1
        return one_hot

class AMD:
    def __init__(self, num_neighbors=5):
        super().__init__()
        self.k = num_neighbors

    def calculate_score(self, encodings, new_data):
        vs = encodings.astype('float32')
        new_data = new_data.astype('float32')
        nnsize = self.k
        if len(encodings) < self.k:
            nnsize = len(encodings)
        distances = np.linalg.norm(vs - new_data, axis=1)
        neighbors = np.argpartition(distances, range(0, nnsize))[:nnsize]
        n_d = distances[neighbors]
        return np.mean(n_d)
