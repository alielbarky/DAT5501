import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic X and Y data and save to a .csv file

def generate_and_save_data(m, b, csv_path="synthetic_data.csv"):
    # Create evenly spaced X values
    x = np.linspace(0, 10, 50)

    # Add random noise to Y values to mimic real data
    noise = np.random.normal(0, 1, size=x.size)

    # Calculate Y using the chosen slope (m) and intercept (b)
    y = m * x + b + noise

    # Save X and Y into a CSV file with column headers
    data = np.column_stack([x, y])
    np.savetxt(csv_path, data, delimiter=",", header="x,y", comments="")

    return x, y # Return values for testing and plotting


# Load the saved CSV file and return X and Y

def load_data(csv_path):
    # Load the numeric values from the CSV file (skip the header row)
    try:
        data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    except Exception as exc:
        # Raise an error if any values in the file are not numeric
        raise ValueError("Non-numeric or malformed data in {}".format(csv_path)) from exc

    # Split into X and Y columns
    return data[:,0], data[:,1]


# Fit a straight line to the loaded data
def fit_line(x, y):
    # Use NumPy’s least squares line fit -> returns slope and intercept
    m_fit, b_fit = np.polyfit(x, y, 1)
    return m_fit, b_fit


# Save a plot 
def save_plot(x, y, m, b, m_fit, b_fit, plot_path="fit_plot.png"):
    
    # Generate a smooth line for plotting
    x_line = np.linspace(x.min(), x.max(), 200)

    # Original line (no noise)
    y_original = m * x_line + b

    # Fitted line from the calculations
    y_fitted = m_fit * x_line + b_fit

    # Plot the scatter + lines
    plt.scatter(x, y, label="Data (plus noise)")
    plt.plot(x_line, y_original, '--', label="Original line")
    plt.plot(x_line, y_fitted, label="Fitted line")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Synthetic Line Fit")
    plt.legend()
    plt.savefig(plot_path)


# Run the full data pipeline when executed directly

if __name__ == "__main__":
    # Choose any slope (m) and intercept (b) for the generated data
    m = 2.0
    b = 1.0

    # Generate and save CSV file
    x, y = generate_and_save_data(m, b)

    # Load the saved CSV file
    x_loaded, y_loaded = load_data("synthetic_data.csv")

    # Fit the line to the noisy data
    m_fit, b_fit = fit_line(x_loaded, y_loaded)

    # Save a plot showing the comparison between original and fitted lines
    save_plot(x_loaded, y_loaded, m, b, m_fit, b_fit)

    # Print values for visual inspection
    print("Original m =", m, "Original b =", b)
    print("Fitted m =", m_fit, "Fitted b =", b_fit)