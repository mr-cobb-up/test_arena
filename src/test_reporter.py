import os
import pandas as pd
from datetime import datetime


class TestReporter:
    def __init__(self):
        self.results = []
        self.report_path = self._create_report_path()

    def _create_report_path(self):
        # 프로젝트 루트의 reports 폴더 생성
        report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(report_dir, exist_ok=True)

        # 날짜를 포함한 파일명 생성
        filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return os.path.join(report_dir, filename)

    def add_result(self, test_case, status, message, duration=None, screenshot_path=None):
        result = {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Test Case': test_case,
            'Status': status,
            'Message': message,
            'Duration (s)': duration,
            'Screenshot': screenshot_path
        }
        self.results.append(result)
        self._save_to_excel()  # 결과가 추가될 때마다 저장

    def _save_to_excel(self):
        df = pd.DataFrame(self.results)

        # 엑셀 스타일 설정
        writer = pd.ExcelWriter(self.report_path, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Test Results')

        # 워크시트 가져오기
        worksheet = writer.sheets['Test Results']

        # 열 너비 자동 조정
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

        writer.close()