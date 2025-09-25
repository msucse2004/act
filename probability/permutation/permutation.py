import os
import random
import sys

from utils import pdf
from utils.unicodes import SUBSCRIPT_NUMBERS

ANSWER_UPPER_LIMIT = 1e7

class Permutation:
    def __init__(self):
        self.title = "Permutation"
        pass

    def factorial(self, n):
        if n == 0:
            return 1
        else:
            return n * self.factorial(n - 1)

    def permutation(self, n, r):
        return self.factorial(n) // self.factorial(n - r)

    def generate_permutation_problem(self):
        n = random.randint(10, 20)
        r = random.randint(2, 4)

        return n, r, self.permutation(n, r)

    def _to_subscript(self, number: int) -> str:
        """Converts an integer into a string of subscript characters."""
        return "".join(SUBSCRIPT_NUMBERS[digit] for digit in str(number))


    def generate_problem(self)->tuple[str, str]:
        problem_text, answer_text = None, None
        answer = ANSWER_UPPER_LIMIT + 1
        while answer > ANSWER_UPPER_LIMIT:
            n, r, answer = self.generate_permutation_problem()
            subscript_n = self._to_subscript(n)
            subscript_r = self._to_subscript(r)
            problem_text = f"{subscript_n} P {subscript_r} ="
            answer_text = f"{answer}"

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
    Permutation().generate_practice(10)

if __name__ == "__main__":
    main()