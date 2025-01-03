import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.insights import Insights
from src.ISO_CMMI_Analyzer import ChecklistAnalysis
import os

def plot_trends(data, trends, parent_frame):
    """
    Visualizes trends in the data as additional line plots.
    :param data: The project dataset.
    :param trends: Detected trends for specific columns.
    :param parent_frame: The parent frame in which to embed the trend charts.
    """
    # Create a figure for the trend charts
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Plot trends for each column
    for idx, column in enumerate(['CSAT', 'OnTimeDelivery', 'BudgetVariance']):
        ax.plot(data["Project"], data[column], marker="o", label=f"{column} Trend")
        # Add trend annotations (if trends list is populated)
        if idx < len(trends):
            ax.text(
                len(data["Project"]) - 1, 
                data[column].iloc[-1], 
                trends[idx], 
                fontsize=9, 
                verticalalignment="center", 
                horizontalalignment="right"
            )

    # Set the chart title and labels
    ax.set_title("Trend Visualization")
    ax.set_xlabel("Project")
    ax.set_ylabel("Values")
    ax.legend()

    # Embed the figure in the parent frame
    canvas = FigureCanvasTkAgg(fig, parent_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



def plot_kpi_charts(data, insights, kpis, trends):
    """
    Generates Matplotlib charts for KPIs and embeds them in a horizontally scrollable Tkinter window.
    Displays averages and insights in a resizable panel.
    """
    root = tk.Tk()
    root.title("KPI Dashboard")

    # Create a paned window for resizable layout
    paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Create a scrollable frame for the charts
    charts_frame = tk.Frame(paned_window)
    paned_window.add(charts_frame)

    # Add a canvas for the charts
    canvas = tk.Canvas(charts_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(charts_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    chart_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=chart_frame, anchor="nw")

    # Configure the canvas scroll region
    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    chart_frame.bind("<Configure>", configure_canvas)

    # Customer Satisfaction Line Chart
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(data["Project"], data["CSAT"], marker="o")
    ax1.set_title("Customer Satisfaction Over Projects")
    ax1.set_xlabel("Project")
    ax1.set_ylabel("CSAT (%)")

    canvas1 = FigureCanvasTkAgg(fig1, chart_frame)
    canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
    plt.close(fig1)  # Close the figure to free memory

    # On-Time Delivery Bar Chart
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(data["Project"], data["OnTimeDelivery"])
    ax2.set_title("On-Time Delivery Rate by Project")
    ax2.set_xlabel("Project")
    ax2.set_ylabel("On-Time Delivery Rate (%)")

    canvas2 = FigureCanvasTkAgg(fig2, chart_frame)
    canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
    plt.close(fig2)  # Close the figure to free memory

    # Budget Variance Bar Chart
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.bar(data["Project"], data["BudgetVariance"], color=["green" if v >= 0 else "red" for v in data["BudgetVariance"]])
    ax3.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax3.set_title("Budget Variance by Project")
    ax3.set_xlabel("Project")
    ax3.set_ylabel("Budget Variance")

    canvas3 = FigureCanvasTkAgg(fig3, chart_frame)
    canvas3.get_tk_widget().grid(row=0, column=2, padx=10, pady=10)
    plt.close(fig3)  # Close the figure to free memory

    # Create a frame for insights and averages
    insights_frame = tk.Frame(paned_window)
    paned_window.add(insights_frame)

    insights_label = tk.Label(insights_frame, text="Averages and Insights", font=("Arial", 16, "bold"))
    insights_label.pack(anchor="w", padx=10, pady=5)

    insights_text = tk.Text(insights_frame, wrap=tk.WORD, height=10, font=("Arial", 12))
    insights_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Add averages to the insights section
    insights_text.insert(tk.END, "Average KPI Values:\n")
    insights_text.insert(tk.END, f"- Average CSAT: {kpis['Average CSAT']:.2f}%\n")
    insights_text.insert(tk.END, f"- On-Time Delivery Rate: {kpis['On-Time Delivery Rate']:.2f}%\n")
    insights_text.insert(tk.END, f"- Average Budget Variance: {kpis['Average Budget Variance']:.2f}\n\n")

    # Add insights
    insights_text.insert(tk.END, "Insights:\n")
    for insight in insights:
        insights_text.insert(tk.END, f"- {insight}\n")

    insights_text.config(state=tk.DISABLED)  # Make the text widget read-only

    # Properly terminate mainloop on window close
    def on_closing():
        print("Exiting GUI...")
        root.destroy()
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind the close button
    root.mainloop()


def collect_user_data():
    """
    Provides a GUI interface for users to input data manually.
    :return: A pandas DataFrame containing the user-provided data.
    """
    input_window = tk.Tk()
    input_window.title("KPI Dashboard - Enter Project Data")
    input_window.geometry("600x500")
    input_window.configure(bg="#eaf2f8")

    # Add a header with styling
    header = tk.Label(input_window, text="Enter Project Data", font=("Helvetica", 20, "bold"), bg="#eaf2f8", fg="#34495e")
    header.pack(pady=10)

    # Add a description below the header
    description = tk.Label(
        input_window, 
        text="Please enter the data for each field below. Ensure consistency across all rows.", 
        font=("Arial", 12), bg="#eaf2f8", fg="#7f8c8d", wraplength=500, justify="center"
    )
    description.pack(pady=10)

    # Create a frame for the input fields
    input_frame = tk.Frame(input_window, bg="#eaf2f8")
    input_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Define fields without percentages
    fields = ["Project", "CSAT", "OnTimeDelivery", "BudgetVariance"]
    entries = []

    def validate_input():
        """Validate input dynamically."""
        try:
            for entry in entries[1:]:  # Skip 'Project' field
                values = entry.get("1.0", tk.END).strip().split("\n")
                # Check if all values are numeric
                if not all(v.strip().replace(".", "").isdigit() for v in values):
                    entry.config(bg="#f9ebea")  # Red background for invalid input
                else:
                    entry.config(bg="#eafaf1")  # Green background for valid input
        except Exception:
            pass

    def submit_data():
        """Collect data from entry fields and store it in a DataFrame."""
        try:
            projects = []
            for i, entry in enumerate(entries):
                column_data = entry.get("1.0", tk.END).strip().split("\n")
                projects.append(column_data)

            # Ensure equal number of rows in all columns
            if len(set(len(col) for col in projects)) > 1:
                raise ValueError("All columns must have the same number of rows.")

            # Construct a DataFrame
            data_dict = {fields[i]: projects[i] for i in range(len(fields))}
            user_data = pd.DataFrame(data_dict)

            # Convert numeric columns to appropriate data types
            user_data["CSAT"] = pd.to_numeric(user_data["CSAT"])
            user_data["OnTimeDelivery"] = pd.to_numeric(user_data["OnTimeDelivery"])
            user_data["BudgetVariance"] = pd.to_numeric(user_data["BudgetVariance"])

            # Close the input window
            input_window.destroy()

            # Process the data
            process_and_plot(user_data)
        except Exception as e:
            messagebox.showerror("Input Error", f"An error occurred: {e}")

    def reset_fields():
        """Reset all fields to default."""
        for entry in entries:
            entry.delete("1.0", tk.END)

    # Create input labels and text areas in a grid layout
    for i, field in enumerate(fields):
        label = tk.Label(input_frame, text=f"{field}:", font=("Arial", 12), bg="#eaf2f8", fg="#34495e")
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        text_area = tk.Text(input_frame, height=3, width=30, font=("Arial", 10), relief=tk.GROOVE, bd=2)
        text_area.grid(row=i, column=1, padx=10, pady=5)
        text_area.bind("<KeyRelease>", lambda e: validate_input())
        entries.append(text_area)

    # Create a frame for buttons
    button_frame = tk.Frame(input_window, bg="#eaf2f8")
    button_frame.pack(pady=20)

    # Add a submit button
    submit_button = tk.Button(button_frame, text="Submit Data", font=("Arial", 12, "bold"), bg="#28a745", fg="white",
                              relief=tk.RAISED, bd=3, command=submit_data)
    submit_button.grid(row=0, column=0, padx=10)

    # Add a reset button
    reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12, "bold"), bg="#dc3545", fg="white",
                             relief=tk.RAISED, bd=3, command=reset_fields)
    reset_button.grid(row=0, column=1, padx=10)

    input_window.mainloop()


def process_and_plot(user_data):
    """
    Process the user-provided data and pass it to the existing functions for analysis and visualization.
    :param user_data: A pandas DataFrame containing the user-provided data.
    """
    try:
        # Validate data
        required_columns = ['Project', 'CSAT', 'OnTimeDelivery', 'BudgetVariance']
        data_ingestion = DataIngestion(required_columns=required_columns)
        validated_data = data_ingestion.validate_data(user_data)

        if validated_data is None:
            print("Error: Data validation failed.")
            return

        # Process data to calculate KPIs
        data_processing = DataProcessing()
        kpis = data_processing.calculate_kpis(validated_data)

        if kpis is None:
            print("Error: KPI calculation failed.")
            return

        # Detect trends
        trends = []
        for column in ['CSAT', 'OnTimeDelivery', 'BudgetVariance']:
            trend = data_processing.detect_trends(validated_data, column)
            if trend:
                trends.append(trend)

        # Debug: Print trends to ensure they are being calculated
        print("Trends detected:", trends)

        # Generate insights
        insights_generator = Insights()
        insights = insights_generator.generate_insights(kpis, validated_data)

        # Add detected trends to insights
        insights.append("Detected Trends:")
        for trend in trends:
            insights.append(f"- {trend}")

        # ISO/CMMI Checklist Evaluation
        checklist = ChecklistAnalysis()

        print("\nCollecting responses for ISO 9001 Checklist:")
        iso_responses = checklist.collect_responses(checklist.iso_9001_checklist)

        print("\nCollecting responses for CMMI Checklist:")
        cmmi_responses = checklist.collect_responses(checklist.cmmi_checklist)

        checklist_summary = checklist.generate_summary(iso_responses, cmmi_responses)

        # Include checklist summary in insights
        insights.append("ISO/CMMI Checklist Evaluation Summary:")
        for key, value in checklist_summary.items():
            insights.append(f"- {key}: {value}")

        # Plot KPI charts in a GUI and display insights
        plot_kpi_charts(validated_data, insights, kpis, trends)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def main():
    """
    Main function to either load static data or allow user to enter data dynamically.
    """
    
    print("Select Mode:")
    print("1. Load Data from File")
    print("2. Enter Data Manually")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        # File path for the mock data
        DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "mock_data.csv")
        print("Current working directory:", os.getcwd())
        try:
            # Load data
            required_columns = ['Project', 'CSAT', 'OnTimeDelivery', 'BudgetVariance']
            data_ingestion = DataIngestion(required_columns=required_columns)
            raw_data = data_ingestion.load_data(DATA_FILE)

            if raw_data is None:
                print("Error: Data could not be loaded.")
                return

            # Validate data
            validated_data = data_ingestion.validate_data(raw_data)
            if validated_data is None:
                print("Error: Data validation failed.")
                return

            # Process data to calculate KPIs
            data_processing = DataProcessing()
            kpis = data_processing.calculate_kpis(validated_data)

            if kpis is None:
                print("Error: KPI calculation failed.")
                return

            # Detect trends
            trends = []
            for column in ['CSAT', 'OnTimeDelivery', 'BudgetVariance']:
                trend = data_processing.detect_trends(validated_data, column)
                if trend:
                    trends.append(trend)

            # Generate insights
            insights_generator = Insights()
            insights = insights_generator.generate_insights(kpis, validated_data)
            # Add detected trends to insights
            insights.append("Detected Trends:")
            for trend in trends:
                insights.append(f"- {trend}")
            # ISO/CMMI Checklist Evaluation
            checklist = ChecklistAnalysis()

            print("\nCollecting responses for ISO 9001 Checklist:")
            iso_responses = checklist.collect_responses(checklist.iso_9001_checklist)

            print("\nCollecting responses for CMMI Checklist:")
            cmmi_responses = checklist.collect_responses(checklist.cmmi_checklist)

            checklist_summary = checklist.generate_summary(iso_responses, cmmi_responses)

            # Include checklist summary in insights
            insights.append("ISO/CMMI Checklist Evaluation Summary:")
            for key, value in checklist_summary.items():
                insights.append(f"- {key}: {value}")

            # Plot KPI charts in a GUI and display insights
            plot_kpi_charts(validated_data, insights, kpis, trends)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif choice == "2":
        collect_user_data()

    else:
        print("Invalid choice. Please restart the program.")

if __name__ == "__main__":
    main()
