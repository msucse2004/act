import os
import random
import sys

from utils import pdf
from utils.factor import gcd
from utils.unicodes import UNICODE_MATH_X


class FactorTrinomial:
    def __init__(self):
        self.title = "Factor Trinomial"
        pass

    def factor_trinomial(self, a:int, b:int, c:int)->tuple[int, tuple[int, int, int], tuple[int, int, int]]:
        """
        ax^2 + bx + c 형태의 삼항식을 인수분해합니다.
        (a*c 방법 사용)
        """
        if a == 0:
            return None, None, None

        g_common = gcd(abs(a), gcd(abs(b), abs(c)))
        a0, b0, c0 = a // g_common, b // g_common, c // g_common

        ac = a0 * c0

        for m in range(-abs(ac), abs(ac) + 1):
            if m != 0 and ac % m == 0:
                n = ac // m
                if m + n == b0:
                    g1 = gcd(a0, m)
                    a1 = a0 // g1
                    c1 = m // g1

                    a2 = g1
                    c2 = c0 // c1

                    # x항 계수 부호 정리
                    if a1 < 0 and a2 < 0:
                        a1, c1 = -a1, -c1
                        a2, c2 = -a2, -c2

                    return g_common, (None, a1, c1), (None, a2, c2)
        return None, None, None

    def get_term_string(self, a:int, b:int, c:int)->str:
        # print(f"trinomial_to_unicode({a}, {b}, {c})")
        if a is None or a == 0:
            term_a = ""
        else:
            if a == 1:
                term_a = f"{UNICODE_MATH_X}{chr(178)}"
            elif a == -1:
                term_a = f"-{UNICODE_MATH_X}{chr(178)}"
            else:
                term_a = f"{a}{UNICODE_MATH_X}{chr(178)}"
        if b > 0:
            if b == 1:
                term_b = f"+ {UNICODE_MATH_X}".strip()
            else:
                term_b = f"+ {b}{UNICODE_MATH_X}".strip()
        elif b is None or b == 0:
            term_b = ""
        else:
            if b == -1:
                term_b = f"-{UNICODE_MATH_X}".strip()
            else:
                term_b = f"- {b * -1}{UNICODE_MATH_X}".strip()

        if c > 0:
            term_c = f"+ {c}".strip()
        elif c is None or c == 0:
            term_c = ""
        else:
            term_c = f"- {c * -1}".strip()
        # 모든 항을 합쳐서 문자열 생성
        equation = f"{term_a} {term_b} {term_c}".strip()

        # 맨 앞에 불필요한 '+'나 공백 제거
        if equation.startswith("+ "):
            equation = equation[2:]

        return equation

    def generate_problem(self)->tuple[str, str]:

        # a x² + b x + c
        a = random.randint(0, 10)

        if random.choice([True, False]):
            a = a * -1
        b = random.randint(-100, 100)
        c = random.randint(-100, 100)

        gcd_value, term1, term2 = self.factor_trinomial(a, b, c)

        common_factor = "" if gcd_value == 1 else str(gcd_value)

        if term1: # a x² + b x + c
            coef_a1, coef_b1, coef_c1 = term1
            coef_a2, coef_b2, coef_c2 = term2

        else:
            print(f"{self.get_term_string(a, b, c)} is unavailable for factoring")
            return None, None

        problem_text = f"{self.get_term_string(a, b, c)} = "
        answer_text = ""

        if coef_b1 < 0:
            answer_text =  f"{common_factor}({self.get_term_string(coef_a1, coef_b1, coef_c1)}) ({self.get_term_string(coef_a2, coef_b2, coef_c2)}) or -{common_factor} ({self.get_term_string(coef_a1, -coef_b1, -coef_c1)}) ({self.get_term_string(coef_a2, coef_b2, coef_c2)})"
        elif coef_b2 < 0:
            answer_text = f"{common_factor}({self.get_term_string(coef_a1, coef_b1, coef_c1)}) ({self.get_term_string(coef_a2, coef_b2, coef_c2)}) or -{common_factor} ({self.get_term_string(coef_a1, coef_b1, coef_c1)}) ({self.get_term_string(coef_a2, -coef_b2, -coef_c2)})"
        else:
            answer_text = f"({common_factor}{self.get_term_string(coef_a1, coef_b1, coef_c1)}) ({self.get_term_string(coef_a2, coef_b2, coef_c2)})"


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
    FactorTrinomial().generate_practice(100)

if __name__ == "__main__":
    main()