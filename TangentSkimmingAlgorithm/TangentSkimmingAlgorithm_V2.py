import csv
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Lists to store the voltage and time values from the CSV file
y_vals = []
x_vals = []

# Function to calculate the area under the curve using Simpson's rule
def getArea(voltages, timeStamps):
    area = integrate.simpson(y=voltages, x=timeStamps)
    return area

# Function to read data from the CSV file
def readDataFromCSV(filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            x_vals.append(float(row[0]))
            y_vals.append(float(row[1]))

def find_positive_half_cycle_indices(voltages, timeStamps, pos_peaks, pos_drop_peaks, slope_threshold=0.1):
    adjusted_indices = []
    temp_indices = []
    indices = []
    find_start_index = True
    positive_voltages = [volt if volt >= 0 else 0 for volt in voltages]

    # Compute differences and slopes
    slopes = np.diff(positive_voltages) / np.diff(timeStamps)

    # Apply threshold to slopes
    significant_rising_slopes = slopes * (np.abs(slopes) >= slope_threshold)
    significant_falling_slopes = slopes * (np.abs(slopes) >= slope_threshold)

    # Find indices where slope changes from non-positive to positive (rising edge start)
    rising_start_indices = np.where((significant_rising_slopes > 0) & (np.roll(significant_rising_slopes, 1) <= 0))[0]

    # Find indices where slope changes from positive to non-positive (falling edge end)
    falling_end_indices = np.where((significant_falling_slopes >= 0) & (np.roll(significant_falling_slopes, 1) < 0))[0]

    # Remove indices where y values are not greater than 0.1
    rising_start_indices = [index for index in rising_start_indices if positive_voltages[index] < 0.5]
    falling_end_indices = [index for index in falling_end_indices if positive_voltages[index] < 0.5]
    
    for start_index in rising_start_indices:
        find_start_index = True
        for end_index in falling_end_indices:
            if end_index > start_index:
                temp_indices.append((start_index, end_index))
                find_start_index = False
                break;
    
    if find_start_index:
        temp_indices.append((rising_start_indices[-1], len(positive_voltages) - 1))

    for start, end in temp_indices:
        for peak in pos_peaks:        
            if start<= peak <= end:
                indices.append((start, end))
                break;

    # Adjust indices based on peak positions within the positive half cycles
    for start, end in indices:
        range_pos_peaks = [p for p in pos_peaks if start <= p <= end]
            
        if len(range_pos_peaks) >= 2:
            pos_peak_start = range_pos_peaks[0]
            pos_peak_end = range_pos_peaks[-1]
            
            range_neg_peaks = [n for n in pos_drop_peaks if pos_peak_start <= n <= pos_peak_end]
            if range_neg_peaks:
                for neg_peak in range_neg_peaks:
                    adjusted_indices.append((start, neg_peak))
                    start = neg_peak

        adjusted_indices.append((start, end))
    
    return adjusted_indices

# Function to find positive peaks in the voltage data
def find_positive_peaks(voltages):
    pos_peaks, _ = find_peaks(voltages, height = 0.5)
    return [peak for peak in pos_peaks if voltages[peak] > 0]

# Function to find peaks of the negative slope (indicating positive drop) in the voltage data
def find_positive_drop_peaks(voltages):
    neg_peaks, _ = find_peaks(-voltages)
    return [peak for peak in neg_peaks if voltages[peak] > 0]

# Function to find the area of the positive half cycles
def findArea(pos_indices, voltages, timeStamps):
    colors = ['lightblue', 'lightgreen', 'black', 'pink', 'red', 'black'] 
    pos_area_list = []

    for i, (start, end) in enumerate(pos_indices):

        x_range = timeStamps[start:end + 1]
        y_signal = voltages[start:end + 1]

        slope_line_x = np.array([timeStamps[start], timeStamps[end]])
        slope_line_y = np.array([voltages[start], voltages[end]])
        plt.plot(slope_line_x, slope_line_y, 'b--')
        y_slope_line = np.interp(x_range, slope_line_x, slope_line_y)

        area_below_slope = getArea(y_slope_line, x_range)
        full_area = getArea(y_signal, x_range)
        
        area_above_slope = full_area - area_below_slope
        
        plt.fill_between(x_range, y_slope_line, color=colors[i % len(colors)], alpha=0.3)
        plt.fill_between(x_range, y_signal, y_slope_line, color="yellow", alpha=0.3)
        
        pos_area_list.append(area_above_slope)

    return pos_area_list

# Function to calculate areas of positive half cycles
def CalculateArea(voltages, timeStamps):
    pos_peaks = find_positive_peaks(voltages)
    pos_drop_peaks = find_positive_drop_peaks(voltages)
    pos_indices = find_positive_half_cycle_indices(voltages, timeStamps, pos_peaks, pos_drop_peaks)
    area = findArea(pos_indices, voltages, timeStamps)

    return pos_peaks, area

if __name__ == "__main__":
    # Read data from the CSV file
    readDataFromCSV("Voltage_readings_testcases.csv")
    
    # Convert lists into NumPy arrays
    voltages = np.array(y_vals)
    timeStamps = np.array(x_vals)
    
    # Plot the voltage vs. time graph
    plt.plot(timeStamps, voltages)

    # Calculate area of positive half cycles
    peak, area = CalculateArea(voltages, timeStamps)
    
    # Annotate peaks with the calculated areas
    for i in range(0, len(peak)):
        plt.annotate(f"{area[i]:.2f}", (timeStamps[peak[i]], voltages[peak[i]]))
    
    # Highlight the peaks on the plot
    plt.scatter(timeStamps[peak], voltages[peak], color='red', marker='x')
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.title('Voltage vs Time')
    plt.legend()
    plt.show()
