import numpy as np
import matplotlib.pyplot as plt

class ChaosGame:
    """
    This is a class representing ngons.

    Attributes:

    n (int): Number of corners in ngon
    r (float): Decimal number within (0,1) included in itereating algorithm
    """
    def __init__(self, n, r):
        """
        The constructor for ChaosGame class.

        Parameters:
            n (int): Number of corners i ngon
            r (float): Decimal number within (0,1) included in itereating algorithm.
        """
        if isinstance(n, int) and n >= 3:
            self.n = n
        else:
            raise ValueError("n must be of type integer and >= 3")
        if 0 < r < 1:
            self.r = r
        else:
            raise ValueError("r must be float within range of (0,1)")

        self._generate_ngon()
        self._starting_point()
        self.iterate(self.N)

    def _generate_ngon(self):
        """Genereates the corners of the ngon"""
        vertices = np.zeros((self.n, 2))
        theta = np.linspace(0, 2*np.pi, self.n, endpoint = False)

        for i in range(self.n):
            vertices[i] = [np.sin(theta[i]), np.cos(theta[i])]

        self.vertices = vertices

    def plot_ngon(self):
        """Plots ngon"""
        plt.scatter(*zip(*self.X_f), s = 0.1, marker = ".")
        plt.axis("equal")
        plt.axis("off")
        plt.show()

    def _starting_point(self):
        """Choosing a random startingpoint inside of ngon"""
        self.N = 10000
        X = np.zeros((self.N+5, 2))

        weights = np.random.random(self.n)
        weights /= np.sum(weights)
        weights = weights[:, None]
        strt_point = np.sum(weights*self.vertices, axis = 0)
        X[0, :] = strt_point

        self.X_i = X

    def iterate(self, steps, discard = 5):
        """
        Iterates 5 times, then discards these points. iterates 10000 more times and stores the values

        Prameters:
            steps (int): amount of steps in iteration
            discard (int): number of elements discarded from start of iterated lists
        """
        rand_int_lst = np.zeros(steps + discard)
        for i in range(steps+discard-1):
            rand_int = np.random.randint(0, self.n)
            rand_int_lst[i+1] = rand_int
            rand_corn = self.vertices[rand_int]
            self.X_i[i+1] = self.r*self.X_i[i] + (1 - self.r)*rand_corn

        self.X_f = self.X_i[discard:]
        self.rand_int_lst = rand_int_lst[discard:]

    def plot(self, color = False, cmap = "jet"):
        """Plots the points with corresponding colors"""
        if color == False:
            color = "k"
        if color == True:
            color = self._compute_color()

        plt.scatter(*zip(*self.X_f), s = 0.2, marker = ".", c = color, cmap = cmap)
        plt.axis("equal")
        plt.axis("off")

    def show(self, color = False, cmap = "jet"):
        self.plot(color, cmap)
        plt.show()

    def _compute_color(self):
        """Creates a color array C"""
        C = np.zeros(self.N)
        C[0] = self.rand_int_lst[0]

        for i in range(self.N - 1):
            C[i+1] = (C[i] + self.rand_int_lst[i+1])/2

        return C

    def savepng(self, outfile, color = False, cmap = "jet"):
        """Saves figures as .png files"""
        if outfile[-4:] == ".png":
            self.plot(color, cmap)
            plt.savefig(outfile, dpi = 1000)
            plt.show() # måtte legge til en show for at bildene ikke skulle lagres oppå hverandre
        else:
            if "." not in outfile:
                self.plot(color)
                plt.savefig(outfile, dpi = 1000)
                plt.show() # måtte legge til en show for at bildene ikke skulle lagres oppå hverandre
            else:
                raise NameError("Wrong file extension added to output file_name. Remove extension.")



if __name__ == "__main__":

    # Using plot_ngon() to plot ngons for n = 3, 4, 5, , 7 and 8
    print("\nNgons for n = 3, 4, 5, , 7 and 8 plotted")
    for i, j in zip([3,4,5,6,7,8], [1/2, 1/3, 1/3, 1/4, 1/4, 1/4]):
        CG_1 = ChaosGame(i, j)
        CG_1.plot_ngon()

    # Plotting 1000 starting points with _starting_point() method
    print("\n1000 random points plotted within pentagon.\nLooks like some irregularities outside of pentagon.")
    CG_2 = ChaosGame(5, 1/3)
    X = np.zeros((1000 + 5, 2))
    for i in range(1000 + 5):
        CG_2._starting_point()
        X[i, :] = CG_2.X_i[0]
    X = X[5:]
    plt.scatter(*zip(*X))
    plt.show()

    # Ensuring that the class works as intended by creating figures for n = 3 and r = 1/2
    print("\nPlotting triangle in black and merging colors")
    CG_3 = ChaosGame(3, 1/2)
    CG_3.show()
    CG_3.show(color = True)

    # Saving figures
    print("\nSaved figures")
    CG_4 = ChaosGame(3, 1/2); CG_5 = ChaosGame(4, 1/3)
    CG_6 = ChaosGame(5, 1/3); CG_7 = ChaosGame(5, 3/8); CG_8 = ChaosGame(6, 1/3)
    objects = [CG_4, CG_5, CG_6, CG_7, CG_8]
    shape_names = ["chaos1", "chaos2", "chaos3", "chaos4", "chaos5"]
    for i, j in zip(range(len(objects)), range(len(shape_names))):
        objects[i].savepng(f"figures/{shape_names[j]}", color = True)
