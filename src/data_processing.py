import pandas as pd

class DataProcessing:
    def __init__(self):
        """
        Initialize the DataProcessing class.
        """
        pass

    def calculate_kpis(self, data):
        """
        Calculate KPIs from the input data.
        :param data: A Pandas DataFrame containing the required columns.
        :return: A dictionary with calculated KPIs.
        """
        try:
            # Calculate KPIs
            avg_csat = data['CSAT'].mean()
            on_time_rate = data['OnTimeDelivery'].mean()
            avg_budget_variance = data['BudgetVariance'].mean()

            kpis = {
                'Average CSAT': avg_csat,
                'On-Time Delivery Rate': on_time_rate,
                'Average Budget Variance': avg_budget_variance,
            }

            print("KPI Calculation Successful.")
            return kpis

        except KeyError as ke:
            print(f"Key Error: Missing column {ke} in the dataset.")
        except Exception as e:
            print(f"An unexpected error occurred during KPI calculation: {e}")

        return None

    def detect_trends(self, data, column):
        """
        Detect trends in the specified column.
        :param data: A Pandas DataFrame containing the column to analyze.
        :param column: The column to analyze for trends.
        :return: A trend description string.
        """
        try:
            trend = ""

            if column in data.columns:
                slope = data[column].diff().mean()

                if slope > 0:
                    trend = f"The {column} is generally increasing."
                elif slope < 0:
                    trend = f"The {column} is generally decreasing."
                else:
                    trend = f"The {column} shows no significant trend."

                print(f"Trend analysis for {column}: {trend}")
                return trend
            else:
                raise KeyError(f"Column '{column}' not found in the dataset.")

        except KeyError as ke:
            print(f"Key Error: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred during trend detection: {e}")

        return None


