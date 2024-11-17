# arena_breakout_test.py
import os
import logging
import subprocess
import time
import psutil
from datetime import datetime
import pyautogui


class ArenaBreakoutTest:
    def __init__(self):
        self.launcher_path = r"D:\Arena Breakout Infinite\launcher\arena_breakout_infinite_launcher"
        self.image_dir = r"C:\Users\cobb\PycharmProjects\test2\images"
        self.game_window_title = "Arena Breakout Infinite"
        self.launcher_process = None

        # 로깅 설정
        self.setup_logging()

        # PyAutoGUI 설정
        pyautogui.FAILSAFE = True

    def setup_logging(self):
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'arena_breakout_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def launch_launcher(self):
        try:
            logging.info("런처 실행 시도")
            self.launcher_process = subprocess.Popen(
                self.launcher_path,
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            logging.info("런처 로딩 대기 중...")
            time.sleep(10)  # 런처 로딩 대기

            logging.info("런처가 실행되었습니다.")
            return True

        except Exception as e:
            logging.error(f"런처 실행 중 오류 발생: {str(e)}")
            return False

    def click_start_button(self):
        try:
            logging.info("게임 시작 버튼 찾는 중...")
            image_path = os.path.join(self.image_dir, 'start_button.png')

            if not os.path.exists(image_path):
                logging.error(f"시작 버튼 이미지를 찾을 수 없습니다: {image_path}")
                return False

            start_button = None
            max_attempts = 30

            for attempt in range(max_attempts):
                try:
                    start_button = pyautogui.locateOnScreen(
                        image_path,
                        confidence=0.7,
                        grayscale=True
                    )

                    if start_button:
                        logging.info(f"시작 버튼 찾음: {start_button}")
                        button_x, button_y = pyautogui.center(start_button)
                        pyautogui.click(button_x, button_y)
                        logging.info(f"버튼 클릭: ({button_x}, {button_y})")
                        return True

                except Exception as e:
                    logging.warning(f"시도 {attempt + 1} 실패: {str(e)}")

                time.sleep(1)
                logging.info(f"시도 {attempt + 1}/{max_attempts}")

            logging.error("시작 버튼을 찾을 수 없습니다.")
            return False

        except Exception as e:
            logging.error(f"시작 버튼 클릭 중 오류: {str(e)}")
            return False

    def is_game_running(self):
        try:
            for proc in psutil.process_iter(['name']):
                if 'arena_breakout' in proc.info['name'].lower():
                    return True
            return False
        except Exception as e:
            logging.error(f"프로세스 확인 중 오류: {str(e)}")
            return False

    def take_screenshot(self, name):
        screenshots_dir = 'screenshots'
        os.makedirs(screenshots_dir, exist_ok=True)

        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(screenshots_dir, filename)
        pyautogui.screenshot(path)
        return path

    def close_all(self):
        try:
            # 게임 프로세스 종료
            for proc in psutil.process_iter(['name']):
                if 'arena_breakout' in proc.info['name'].lower():
                    proc.terminate()

            time.sleep(3)

            # 런처 프로세스 종료
            if self.launcher_process:
                self.launcher_process.terminate()

            logging.info("게임과 런처가 종료되었습니다.")

        except Exception as e:
            logging.error(f"종료 중 오류 발생: {str(e)}")


def main():
    test = ArenaBreakoutTest()

    try:
        # 1. 런처 실행
        if test.launch_launcher():
            logging.info("런처 실행 성공")

            # 2. 시작 버튼 클릭
            if test.click_start_button():
                logging.info("게임 로딩 대기 중...")
                time.sleep(20)  # 게임 로딩 대기

                # 3. 게임 실행 확인
                if test.is_game_running():
                    # 스크린샷 저장
                    screenshot_path = test.take_screenshot('game_running')
                    logging.info(f"스크린샷 저장됨: {screenshot_path}")

                    # 30초 동안 게임 실행 상태 유지
                    time.sleep(30)

                    # 4. 게임과 런처 종료
                    test.close_all()
                else:
                    logging.error("게임이 실행되지 않았습니다.")
            else:
                logging.error("게임 시작 버튼 클릭 실패")
        else:
            logging.error("런처 실행 실패")

    except Exception as e:
        logging.error(f"테스트 중 오류 발생: {str(e)}")
        test.close_all()  # 오류 발생 시에도 정리


if __name__ == "__main__":
    main()