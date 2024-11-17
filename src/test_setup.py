
import os
import sys
import pyautogui
import logging
from datetime import datetime

class QAEnvironmentSetup:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f'qa_test_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def check_environment(self):
        try:
            # Python 버전 확인
            logging.info(f"Python 버전: {sys.version}")

            # 화면 해상도 확인
            screen_width, screen_height = pyautogui.size()
            logging.info(f"화면 해상도: {screen_width}x{screen_height}")

            # 프로젝트 구조 확인
            project_root = os.path.dirname(os.path.dirname(__file__))
            required_folders = ['config', 'images', 'logs', 'src']

            for folder in required_folders:
                folder_path = os.path.join(project_root, folder)
                if os.path.exists(folder_path):
                    logging.info(f"폴더 확인: {folder} ✓")
                else:
                    logging.error(f"폴더 없음: {folder} ✗")

            logging.info("환경 점검 완료!")
            return True

        except Exception as e:
            logging.error(f"환경 점검 중 오류 발생: {str(e)}")
            return False

if __name__ == "__main__":
    setup = QAEnvironmentSetup()
    setup.check_environment()# src/test_setup.py
import os
import sys
import pyautogui
import logging
from datetime import datetime

class QAEnvironmentSetup:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f'qa_test_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def check_environment(self):
        try:
            # Python 버전 확인
            logging.info(f"Python 버전: {sys.version}")

            # 화면 해상도 확인
            screen_width, screen_height = pyautogui.size()
            logging.info(f"화면 해상도: {screen_width}x{screen_height}")

            # 프로젝트 구조 확인
            project_root = os.path.dirname(os.path.dirname(__file__))
            required_folders = ['config', 'images', 'logs', 'src']

            for folder in required_folders:
                folder_path = os.path.join(project_root, folder)
                if os.path.exists(folder_path):
                    logging.info(f"폴더 확인: {folder} ✓")
                else:
                    logging.error(f"폴더 없음: {folder} ✗")

            logging.info("환경 점검 완료!")
            return True

        except Exception as e:
            logging.error(f"환경 점검 중 오류 발생: {str(e)}")
            return False

if __name__ == "__main__":
    setup = QAEnvironmentSetup()
    setup.check_environment()