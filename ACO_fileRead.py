import vrplib

class FileRead():
    def __init__(self, path):
        self.path = path


    def instanceTaker(self):
        
        instance = vrplib.read_instance(self.path)
        # print(instance["stations_coord"].shape)
        # print(len(instance["edge_weight"]))
        # print(instance["node_coord"][1])
        # print(instance["edge_weight"][48][0])
        # print(instance["energy_capacity"])
        # print(instance["edge_weight"])
        return instance


fileInst = FileRead("benchmark.evrp")
a = fileInst.instanceTaker()
