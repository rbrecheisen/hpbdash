from ..models import ReportModel, ReportItemModel


class ReportRenderer:

    def __init__(self, report):
        self.report = report

    def execute(self):
        print(self.report.name)
        for query in self.report.queries:
            print(f' - {query.sql_statement}')
