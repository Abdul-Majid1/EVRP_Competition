import matplotlib.pyplot as plt
from ACO import AntColonyOptimization

class graph:

    def dataExtract(self):
        file = open(self.path, 'r')
        numLine = file.readlines()
        counter = 0
        for i in range(0, len(numLine), 202):
            fileName = self.filename[counter]
            data = numLine[i+1:i+201]
            self.ploting_graph(fileName, data)
            counter += 1

    def ploting_graph(self, fileName, data):
        iteration = []
        result = []
        for i in range(0, len(data), 20):
            temp = str.split(data[i], ',')
            iteration.append(temp[0])
            result.append(temp[1])
       
        plt.plot(iteration, result)
        plt.legend()
        plt.xlabel("Number of Iterations")
        plt.ylabel("Minimum Distance Found")
        plt.title(f'{fileName} Analysis')
        
        plt.savefig(fileName+'.png', bbox_inches='tight')


    def avg_min_graph(self):
        # Code For generating Graph
        filename = ["A-n32-k5", "A-n44-k6", "A-n60-k9", "A-n80-k10"]
        iterations = 200
        for i in range(len(filename)):
            temp = AntColonyOptimization(2, 3, iterations, 10, 0.5, filename[i])
            result = temp.ACO_main()
            plt.plot([i for i in range(1, iterations+1)], result[0], label="min")
            plt.plot([i for i in range(1, iterations+1)], result[1], label="avg")
            plt.xlabel('iteration')
            plt.title(f'Plot of average fitness of {filename[i]} against iterations')
            plt.ylabel('fitness')
            plt.legend()
            plt.savefig(f'{filename[i]} for {iterations}+.png')
            plt.close()
    
    def alpha_beta_graph(self):

        # The source of this code is from https://stackoverflow.com/questions/22239691/code-for-line-coefficients-given-two-points


        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        z = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        w = [1348.099397489995, 1009.2277286535249, 882.199860269852, 853.3586743652411,
            843.0602471138308, 812.0323477103043, 827.2248686759375, 824.7540700673145, 810.3706665228863]

        # Create a 4D scatter plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x, y, z, c=w, cmap='viridis')

        # Add a colorbar
        fig.colorbar(scatter, shrink=0.5, aspect=5)

        # Set the plot labels
        ax.set_xlabel('Alpha')
        ax.set_ylabel('Beta')
        ax.set_zlabel('Evaporation Rate')

        # Show the plot
        plt.savefig("Controlled.png")
        plt.show()

a = graph()
a.alpha_beta_graph()