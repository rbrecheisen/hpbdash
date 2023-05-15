from ..models import ReportModel, ReportItemModel


class ReportRenderer:

    def __init__(self, report):
        self.report_name = report.name
        self.report_items = ReportItemModel.objects.filter(report=report)

    def execute(self):
        print(self.report_name)
        for report_item in self.report_items:
            print(f' - {report_item.sql_statement}')
