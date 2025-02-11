import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define rocker switch parameters
pivot_x, pivot_y = 0, 0  # Pivot point of the rocker
arm_length = 5  # Length of the rocker arm (cm)
max_angle = 30  # Maximum rotation angle (degrees) of the switch
desired_lift = 2  # Desired vertical lift of the unpressed side (cm)

# Calculate the required rotation angle to achieve 2 cm lift
required_angle = np.degrees(np.arcsin(desired_lift / arm_length))

# Ensure it does not exceed the switch's natural max angle
if required_angle > max_angle:
    required_angle = max_angle

# Convert angles to radians
max_angle_rad = np.radians(max_angle)
required_angle_rad = np.radians(required_angle)

# Generate points for the switch in motion
angles = np.linspace(-required_angle_rad, required_angle_rad, 20)
end_x = pivot_x + arm_length * np.sin(angles)
end_y = pivot_y - arm_length * np.cos(angles)

# Create figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-arm_length - 1, arm_length + 1)
ax.set_ylim(-arm_length - 1, arm_length + 1)
ax.set_aspect('equal')
ax.set_title("Rocker Switch Motion Simulation")

# Initialize rocker arm line
rocker_line, = ax.plot([], [], 'o-', lw=3, label="Rocker Switch")

# Stopper position (mechanical constraint)
stopper_x = [pivot_x + arm_length * np.sin(required_angle_rad)]
stopper_y = [pivot_y - arm_length * np.cos(required_angle_rad)]
ax.plot(stopper_x, stopper_y, 'ro', label="Stopper (Limit)")

# Animation function
def update(frame):
    rocker_line.set_data([pivot_x, end_x[frame]], [pivot_y, end_y[frame]])
    return rocker_line,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(angles), interval=50, repeat=True)

plt.legend()
plt.show()
