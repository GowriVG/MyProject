import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Function to get user input for constraints
def get_constraints():
    constraints = []
    while True:
        try:
            num_constraints = int(input("Enter the number of constraints: ").strip())
            if num_constraints < 1:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
    for i in range(num_constraints):
        while True:
            try:
                print(f"Enter coefficients for constraint {i+1} (format: a b c op for ax + by op c, where op is <=, >=, or =):")
                a, b, c, op = input().split()
                a, b, c = float(a), float(b), float(c)
                if op not in ['<=', '>=', '=']:
                    print("Invalid operator. Use '<=', '>=', or '='.")
                    continue
                constraints.append((a, b, c, op))
                break  # Exit loop if input is valid
            except ValueError:
                print("Invalid input. Please enter three numeric values followed by '<=', '>=', or '='.")
    return constraints

# Function to get user input for the objective function
def get_objective():
    while True:
        try:
            print("Enter coefficients for the objective function (format: a b for Z = ax + by):")
            a, b = map(float, input().split())
            return a, b
        except ValueError:
            print("Invalid input. Please enter two numeric values separated by spaces.")

# Function to find intersection points of constraints
def find_intersection_points(constraints):
    intersection_points = []
    for (a1, b1, c1, _), (a2, b2, c2, _) in combinations(constraints, 2):
        A = np.array([[a1, b1], [a2, b2]])
        B = np.array([c1, c2])
        try:
            intersection = np.linalg.solve(A, B)
            if all(p >= 0 for p in intersection):  # Ensuring non-negative region
                intersection_points.append(intersection)
        except np.linalg.LinAlgError:
            continue
    return np.array(intersection_points) if intersection_points else np.array([])

# Function to evaluate the objective function at multiple points
def evaluate_objective(points, a, b, optimization_type):
    if points.size == 0:
        print("No feasible region found. No solution exists.")
        exit()
    values = [a * p[0] + b * p[1] for p in points]
    if optimization_type == 'max':
        optimal_value = max(values)
    else:
        optimal_value = min(values)
    optimal_points = [points[i] for i, v in enumerate(values) if v == optimal_value]
    return optimal_points, optimal_value

# Function to plot constraints, feasible region, and optimal points
def plot_solution(constraints, x_values, optimal_points):
    feasible_x = []
    feasible_y = []
    
    for a, b, c, op in constraints:
        if b != 0:
            y_values = (c - a * x_values) / b
            plt.plot(x_values, y_values, label=f'{a}x + {b}y {op} {c}', linestyle='solid')
        else:
            # Handle vertical lines (b = 0)
            plt.axvline(x=c / a, label=f'{a}x {op} {c}', linestyle='solid')
    
    # Find feasible region points
    for x in np.linspace(0, 10, 100):
        for y in np.linspace(0, 10, 100):
            if all(
                (a * x + b * y <= c if op == '<=' else 
                 a * x + b * y >= c if op == '>=' else 
                 np.isclose(a * x + b * y, c)) 
                for a, b, c, op in constraints
            ):
                feasible_x.append(x)
                feasible_y.append(y)
    
    # Shade feasible region
    plt.scatter(feasible_x, feasible_y, color='lightblue', s=5, alpha=0.5)
    
    # Plot optimal points
    for idx, optimal_point in enumerate(optimal_points):
        plt.plot(optimal_point[0], optimal_point[1], 'ro', label=f'Optimal Point {idx+1}')
        plt.axhline(optimal_point[1], color='red', linestyle='dotted')
        plt.axvline(optimal_point[0], color='red', linestyle='dotted')
        plt.text(optimal_point[0], optimal_point[1], f'({optimal_point[0]:.2f}, {optimal_point[1]:.2f})', fontsize=12, color='black', ha='right')
    
    # Add labels, legend, and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.legend()
    plt.title('Graphical Solution of LPP')
    plt.show()

# Main program
def main():
    constraints = get_constraints()
    a, b = get_objective()
    
    while True:
        optimization_type = input("Enter 'max' for maximization or 'min' for minimization: ").strip().lower()
        if optimization_type in ('max', 'min'):
            break
        print("Invalid input. Please enter 'max' or 'min'.")
    
    x_values = np.linspace(0, 10, 100)
    intersection_points = find_intersection_points(constraints)
    optimal_points, optimal_value = evaluate_objective(intersection_points, a, b, optimization_type)
    
    if len(optimal_points) > 1:
        print("Multiple Optimal Solutions Found:")
    
    for idx, optimal_point in enumerate(optimal_points, start=1):
        print(f"Optimal Solution {idx}: x = {optimal_point[0]:.2f}, y = {optimal_point[1]:.2f}")
    print(f"{'Maximum' if optimization_type == 'max' else 'Minimum'} Value of Z = {optimal_value:.2f}")
    
    plot_solution(constraints, x_values, optimal_points)

# Run the program
if __name__ == "__main__":
    main()