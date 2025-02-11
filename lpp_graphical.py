import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
def constraint1(x):
    return (6 - 2 * x) / 3  # Example: 2x + 3y <= 6

def constraint2(x):
    return (4 - x) / 2      # Example: x + 2y <= 4

# Define the objective function
def objective(x):
    return (8 - 4 * x) / 3  # Example: Maximize Z = 4x + 3y

# Define the range for x values
x_values = np.linspace(0, 5, 100)

# Plot the constraints
plt.plot(x_values, constraint1(x_values), label=r'$2x + 3y \leq 6$')
plt.plot(x_values, constraint2(x_values), label=r'$x + 2y \leq 4$')

# Fill the feasible region
y1 = constraint1(x_values)
y2 = constraint2(x_values)
plt.fill_between(x_values, 0, np.minimum(y1, y2), where=(y1 >= 0) & (y2 >= 0), color='gray', alpha=0.5)

# Plot the objective function
plt.plot(x_values, objective(x_values), label=r'$Z = 4x + 3y$', linestyle='dashed')

# Find the intersection point of the constraints
A = np.array([[2, 3], [1, 2]])
B = np.array([6, 4])
intersection = np.linalg.solve(A, B)

# Plot the intersection point
plt.plot(intersection[0], intersection[1], 'ro', label='Optimal Point')

# Add labels and legend
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True)
plt.legend()
plt.title('Graphical Solution of LPP')

# Show the plot
plt.show()

# Print the optimal solution
print(f"Optimal Solution: x = {intersection[0]:.2f}, y = {intersection[1]:.2f}")
print(f"Maximum Value of Z = {4 * intersection[0] + 3 * intersection[1]:.2f}")