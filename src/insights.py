class Insights:
    def __init__(self):
        """
        Initialize the Insights class.
        """
        pass

    def generate_insights(self, kpis, data):
        """
        Generate actionable insights based on calculated KPIs and project-specific data.
        :param kpis: A dictionary containing KPI values.
        :param data: The original project data.
        :return: A list of actionable insights.
        """
        try:
            insights = []

            # Insight for CSAT
            if kpis.get('Average CSAT', 0) < 80:
                insights.append("Customer satisfaction is below the desired threshold. Focus on improving communication with clients and addressing their concerns effectively.")
            else:
                insights.append("Customer satisfaction is at an acceptable level. Continue maintaining high-quality delivery.")

            # Insight for On-Time Delivery Rate
            if kpis.get('On-Time Delivery Rate', 0) < 90:
                insights.append("On-time delivery rate is below 90%. Consider optimizing project schedules and improving time management practices.")
            else:
                insights.append("On-time delivery rate is excellent. Maintain the current project scheduling strategies.")

            # Insight for Budget Variance (Project-Specific)
            over_budget_projects = data[data['BudgetVariance'] < 0]['Project'].tolist()
            under_budget_projects = data[data['BudgetVariance'] > 0]['Project'].tolist()

            if over_budget_projects:
                insights.append(f"The following projects are over budget: {', '.join(over_budget_projects)}. Review cost management strategies for these projects.")
            if under_budget_projects:
                insights.append(f"The following projects are staying within or under budget: {', '.join(under_budget_projects)}. Consider re-evaluating resource allocation to optimize usage.")

            print("Insights generation successful.")
            return insights

        except Exception as e:
            print(f"An unexpected error occurred during insight generation: {e}")
            return None

