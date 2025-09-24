import math
import os
import random
import sys

from utils import pdf
from utils.unicodes import UNICODE_THETA, UNICODE_DEGREE_CIRCLE, UNITCODE_PI


class ArcLength:
    def __init__(self):
        self.title = "Arc Length"
        pass

    def calculate_length_with_degree(self, radius, degree)->tuple[int, int]:
        common_divisor = math.gcd(2 * radius * degree, 360)
        simplified_numerator = 2 * radius * degree // common_divisor
        simplified_denominator = 360 // common_divisor
        return simplified_numerator, simplified_denominator

    def calculate_length_with_radian(self, radius, radian)->int:
        return radius * radian

    def generate_problem(self)->tuple[str, str]:
        problem_text, answer_text = None, None

        problem_type_list = ['degree', 'radian']
        problem_type = random.choice(problem_type_list)

        if problem_type == 'degree':
            radius = random.randint(1, 100)
            degree = random.randint(1, 360)
            numerator, denominator = self.calculate_length_with_degree(radius, degree)

            if denominator == 1:
                answer_text = f"{numerator} {UNITCODE_PI} or {numerator * math.pi}"
            else:
                answer_text = f"{numerator} / {denominator} {UNITCODE_PI} or {numerator / denominator * math.pi}"

            problem_text = f"r = {radius}, {UNICODE_THETA} = {degree} {UNICODE_DEGREE_CIRCLE}"

        else:
            radius = random.randint(1, 100)
            degree = random.randint(0, 200) / 100
            answer_text = self.calculate_length_with_radian(radius, degree)

            problem_text = f"r = {radius}, {UNICODE_THETA} = {degree} rad"

        return problem_text, answer_text
    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None

        while problem_text is None:
            problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} {answer_text}")

        return problem_text, answer_text

    def generate_practice(self, number_of_problems: int = 10):
        num_of_problems = 0
        problem_list = []
        answer_list = []

        while num_of_problems < number_of_problems:
            problem, answer = self.get_problem_answer()
            problem_list.append(problem)
            answer_list.append(answer)
            num_of_problems += 1

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        module_path = os.path.join(parent_dir, "pdf_handling")

        if module_path not in sys.path:
            sys.path.append(module_path)

        try:
            pdf.generate_pdf_files(f"{self.title} Problems", problem_list, num_column=2, row_spacing=70)
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2, row_spacing=14)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    ArcLength().generate_practice(100)

if __name__ == "__main__":
    main()
