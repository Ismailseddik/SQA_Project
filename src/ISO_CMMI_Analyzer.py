class ChecklistAnalysis:
    def __init__(self):
        """
        Initialize the ChecklistAnalysis class with ISO 9001 and CMMI checklists.
        """
        self.iso_9001_checklist = [
            "Customer requirements are clearly defined and documented.",
            "Quality objectives are established and tracked.",
            "Non-conformities are identified and addressed promptly.",
            "Regular internal audits are conducted.",
            "Customer feedback is regularly reviewed and acted upon."
        ]

        self.cmmi_checklist = [
            "Project planning includes risk management strategies.",
            "Requirements are clearly documented and validated.",
            "Processes are standardized and documented.",
            "Quality assurance activities are integrated into the project lifecycle.",
            "Process improvements are tracked and implemented."
        ]

    def collect_responses(self, checklist):
        """
        Collect responses for a given checklist dynamically.
        :param checklist: A list of checklist items.
        :return: A list of boolean responses.
        """
        print("\nPlease respond to the following checklist items (y/n):")
        responses = []
        for item in checklist:
            response = input(f"- {item} (y/n): ").strip().lower()
            responses.append(response == 'y')
        return responses

    def evaluate_iso_checklist(self, responses):
        """
        Evaluate the ISO 9001 checklist based on responses.
        """
        score = sum(responses)
        total = len(self.iso_9001_checklist)
        compliance = (score / total) * 100

        if compliance == 100:
            level = "Fully Compliant"
        elif compliance >= 75:
            level = "Mostly Compliant"
        elif compliance >= 50:
            level = "Partially Compliant"
        else:
            level = "Non-Compliant"

        return compliance, level

    def evaluate_cmmi_checklist(self, responses):
        """
        Evaluate the CMMI checklist based on responses.
        """
        score = sum(responses)
        total = len(self.cmmi_checklist)
        compliance = (score / total) * 100

        if compliance == 100:
            maturity_level = "Level 5: Optimizing"
        elif compliance >= 75:
            maturity_level = "Level 4: Quantitatively Managed"
        elif compliance >= 50:
            maturity_level = "Level 3: Defined"
        elif compliance >= 25:
            maturity_level = "Level 2: Managed"
        else:
            maturity_level = "Level 1: Initial"

        return compliance, maturity_level

    def generate_summary(self, iso_responses, cmmi_responses):
        """
        Generate a summary of ISO 9001 and CMMI checklist evaluations.
        """
        iso_compliance, iso_level = self.evaluate_iso_checklist(iso_responses)
        cmmi_compliance, cmmi_level = self.evaluate_cmmi_checklist(cmmi_responses)

        return {
            "ISO 9001 Compliance": f"{iso_compliance:.2f}% ({iso_level})",
            "CMMI Maturity Level": f"{cmmi_compliance:.2f}% ({cmmi_level})"
        }
