import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.insights import Insights
from src.ISO_CMMI_Analyzer import ChecklistAnalysis


def plot_kpi_charts(data, insights, kpis):
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

    # On-Time Delivery Bar Chart
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(data["Project"], data["OnTimeDelivery"])
    ax2.set_title("On-Time Delivery Rate by Project")
    ax2.set_xlabel("Project")
    ax2.set_ylabel("On-Time Delivery Rate (%)")

    canvas2 = FigureCanvasTkAgg(fig2, chart_frame)
    canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

    # Budget Variance Bar Chart
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.bar(data["Project"], data["BudgetVariance"], color=["green" if v >= 0 else "red" for v in data["BudgetVariance"]])
    ax3.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax3.set_title("Budget Variance by Project")
    ax3.set_xlabel("Project")
    ax3.set_ylabel("Budget Variance")

    canvas3 = FigureCanvasTkAgg(fig3, chart_frame)
    canvas3.get_tk_widget().grid(row=0, column=2, padx=10, pady=10)

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




def main():
    # File path for the mock data
    DATA_FILE = "SQA_Project/data/mock_data.csv"

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

        # Generate insights
        insights_generator = Insights()
        insights = insights_generator.generate_insights(kpis, validated_data)
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
        plot_kpi_charts(validated_data, insights,kpis)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
