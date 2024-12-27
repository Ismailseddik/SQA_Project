import os
import pandas as pd

def generate_mock_data():
    """
    Generates a mock_data.csv file with sample data for the dashboard.
    Saves it in the same directory as this Python file.
    """
    # Sample mock data
    mock_data = {
        "Project": ["Project1", "Project2", "Project3", "Project4", "Project5"],
        "CSAT": [85, 78, 92, 88, 90],  # Customer satisfaction scores
        "OnTimeDelivery": [95, 85, 90, 88, 92],  # On-time delivery rates
        "BudgetVariance": [2, -3, 0, 1, -2]  # Budget variance
    }

    # Convert to DataFrame
    mock_data_df = pd.DataFrame(mock_data)

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # File path for the CSV in the same directory
    file_path = os.path.join(script_dir, "mock_data.csv")

    # Save DataFrame to CSV
    mock_data_df.to_csv(file_path, index=False)
    print(f"Mock data saved to {file_path}")

# Generate the mock data when this script is run
if __name__ == "__main__":
    generate_mock_data()
