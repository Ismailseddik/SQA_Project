import plotly.express as px
import plotly.graph_objects as go

class Visualization:
    def __init__(self):
        """
        Initialize the Visualization class.
        """
        pass

    def generate_csat_chart(self, data):
        """
        Generate a line chart for Customer Satisfaction (CSAT).
        :param data: A Pandas DataFrame containing the required columns.
        :return: A Plotly figure object.
        """
        try:
            fig = px.line(data, x='Project', y='CSAT', title='Customer Satisfaction Over Projects', markers=True)
            fig.update_layout(yaxis_title='CSAT (%)', xaxis_title='Project')
            print("CSAT chart generated successfully.")
            return fig
        except Exception as e:
            print(f"Error generating CSAT chart: {e}")
            return None

    def generate_on_time_chart(self, data):
        """
        Generate a bar chart for On-Time Delivery Rate.
        :param data: A Pandas DataFrame containing the required columns.
        :return: A Plotly figure object.
        """
        try:
            fig = px.bar(data, x='Project', y='OnTimeDelivery', title='On-Time Delivery Rate by Project', text='OnTimeDelivery')
            fig.update_layout(yaxis_title='On-Time Delivery Rate (%)', xaxis_title='Project')
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            print("On-Time Delivery Rate chart generated successfully.")
            return fig
        except Exception as e:
            print(f"Error generating On-Time Delivery chart: {e}")
            return None

    def generate_budget_chart(self, data):
        """
        Generate a pie chart for Budget Variance.
        :param data: A Pandas DataFrame containing the required columns.
        :return: A Plotly figure object.
        """
        try:
            fig = px.pie(data, names='Project', values='BudgetVariance', title='Budget Variance Distribution')
            print("Budget Variance chart generated successfully.")
            return fig
        except Exception as e:
            print(f"Error generating Budget Variance chart: {e}")
            return None

