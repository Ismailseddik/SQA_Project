import pandas as pd

class DataIngestion:
    def __init__(self, required_columns):
        """
        Initialize the DataIngestion class.
        :param required_columns: List of required columns in the input data.
        """
        self.required_columns = required_columns

    def load_data(self, file_path):
        """
        Load data from a CSV file and validate its structure.
        :param file_path: Path to the CSV file.
        :return: A Pandas DataFrame if valid, None otherwise.
        """
        try:
            # Load the data
            data = pd.read_csv(file_path)

            # Validate required columns
            if all(column in data.columns for column in self.required_columns):
                print("Data loaded successfully.")
                return data
            else:
                missing_cols = [col for col in self.required_columns if col not in data.columns]
                raise ValueError(f"Missing required columns: {missing_cols}")

        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except ValueError as ve:
            print(f"Validation Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None

    def validate_data(self, data):
        """
        Validate the data for missing values and correct data types.
        :param data: The input Pandas DataFrame.
        :return: A cleaned and validated DataFrame if valid, None otherwise.
        """
        try:
            # Check for missing values
            if data.isnull().values.any():
                print("Warning: Missing values detected. Filling with defaults.")
                data.fillna(0, inplace=True)  # Fill missing values with 0 (customize as needed)

            # Example data type validation (add as required)
            for col in self.required_columns:
                if data[col].dtype not in ['int64', 'float64', 'object']:
                    raise ValueError(f"Column '{col}' has invalid data type: {data[col].dtype}")

            print("Data validation successful.")
            return data

        except ValueError as ve:
            print(f"Validation Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred during validation: {e}")

        return None

# Example usage
if __name__ == "__main__":
    # Define the required columns for the dashboard
    required_columns = ['Project', 'CSAT', 'OnTimeDelivery', 'BudgetVariance']

    # Initialize the DataIngestion class
    data_ingestion = DataIngestion(required_columns=required_columns)

    # Load and validate the data
    file_path = "data/mock_data.csv"  # Path to your mock data CSV file
    raw_data = data_ingestion.load_data(file_path)

    if raw_data is not None:
        validated_data = data_ingestion.validate_data(raw_data)
        if validated_data is not None:
            print(validated_data.head())  # Display the first few rows of the validated data
