import matplotlib.pyplot as plt
import numpy as np
import time

class RectangleGrid:
    def __init__(self, grid):
        self.loc_grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def linear_search(self, value):
        for y in range(self.height):
            for x in range(self.width): 
                if self.loc_grid[y][x] == value:
                    return y, x
        return None

    def divconq_search(self, value, x_from, x_to, y_from, y_to):

        if x_from > x_to or y_from > y_to:
            return None

        x_mid = (x_from + x_to) // 2
        y_mid = (y_from + y_to) // 2

        if value == self.loc_grid[y_mid][x_mid]:
            return y_mid, x_mid

        elif value < self.loc_grid[y_mid][x_mid]:
            left_result = self.divconq_search(value, x_from, x_mid - 1, y_from, y_to)
            if left_result is not None:
                return left_result

            top_right_result = self.divconq_search(value, x_mid, x_to, y_from, y_mid - 1)
            if top_right_result is not None:
                return top_right_result

        else:
            lower_result = self.divconq_search(value, x_from, x_to, y_mid + 1, y_to)
            if lower_result is not None:
                return lower_result

            top_right_result = self.divconq_search(value, x_mid + 1, x_to, y_from, y_mid)
            if top_right_result is not None:
                return top_right_result

        return None


def generate_grid(size):
    return np.random.randint(low=1000, high=100000, size=(size, size))


def run_experiment(grid_size):
    grid = generate_grid(grid_size)

    # target value is bottom right corner
    target_value = grid[grid_size - 1][grid_size - 1]
    rectangle = RectangleGrid(grid)

    # Measure linear search
    start_time = time.time()
    linear_search_result = rectangle.linear_search(target_value)
    linear_search_time = time.time() - start_time
    print (" linear search time: ", linear_search_time)
    linear_search_cells = rectangle.height * rectangle.width

    # Measure divide and conquer search
    start_time = time.time()
    divide_conquer_result = rectangle.divconq_search(target_value, 0, rectangle.width - 1, 0, rectangle.height - 1)
    divide_conquer_time = time.time() - start_time
    print (" divide and conquer time: ", divide_conquer_time)
    divide_conquer_cells = grid_size * 4  # Assuming worst-case scenario

    return linear_search_cells, divide_conquer_cells, linear_search_time, divide_conquer_time


def plot_results(grid_sizes, linear_search_cells, divide_conquer_cells, linear_search_time, divide_conquer_time):
    plt.figure(figsize=(12, 6))

    # Plot Number of Scanned Cells
    plt.subplot(1, 2, 1)
    plt.plot(grid_sizes, linear_search_cells, label='Linear Search')
    plt.plot(grid_sizes, divide_conquer_cells, label='Divide and Conquer')
    plt.xlabel('Grid Size')
    plt.ylabel('Number of Scanned Cells')
    plt.title('Comparison: Number of Scanned Cells')
    plt.legend()

    # Plot Running Time
    plt.subplot(1, 2, 2)
    plt.plot(grid_sizes, linear_search_time, label='Linear Search')
    plt.plot(grid_sizes, divide_conquer_time, label='Divide and Conquer')
    plt.xlabel('Grid Size')
    plt.ylabel('Running Time (seconds)')
    plt.title('Comparison: Running Time')
    plt.legend()

    plt.tight_layout()
    plt.show()



def main():
    grid_sizes = [2, 3, 4, 5, 6, 7, 8, 9, 10 ,15, 20, 60]  # Adjust the grid sizes as desired
    linear_search_cells = []
    divide_conquer_cells = []
    linear_search_time = []
    divide_conquer_time = []

    for size in grid_sizes:
        linear_cells, divide_cells, linear_time, divide_time = run_experiment(size)
        linear_search_cells.append(linear_cells)
        divide_conquer_cells.append(divide_cells)
        linear_search_time.append(linear_time)
        divide_conquer_time.append(divide_time)

    plot_results(grid_sizes, linear_search_cells, divide_conquer_cells, linear_search_time, divide_conquer_time)


if __name__ == '__main__':
    main()
