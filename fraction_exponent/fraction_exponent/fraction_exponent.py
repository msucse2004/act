import os
import random
import sys
from fractions import Fraction

from utils import pdf


class FractionExponent:
    def __init__(self):
        self.title = "Fraction Exponent"

    @staticmethod
    def get_divisors(n):
        """
        주어진 자연수 n의 모든 약수를 리스트로 반환합니다.

        Args:
            n: 약수를 구할 자연수 (정수).

        Returns:
            n의 모든 약수를 담은 리스트.
            n이 1보다 작으면 빈 리스트를 반환합니다.
        """
        if not isinstance(n, int) or n < 1:
            print("오류: 1 이상의 정수를 입력해주세요.")
            return []

        divisors = []
        # 1부터 n까지 모든 수를 확인하며 n을 나누어 떨어뜨리는 수를 찾습니다.
        for i in range(1, n + 1):
            if n % i == 0:
                divisors.append(i)
        return divisors

    def generate_fraction(self):

        innerExp = random.randint(2, 4)
        org_numerator = random.randint(1, 5)
        org_denominator = random.randint(1, 5)

        numerator = org_numerator ** innerExp
        denominator = org_denominator ** innerExp

        fractions_base_org = Fraction(org_numerator, org_denominator)

        fraction_base = Fraction(numerator, denominator)

        exp_numerator = random.randint(-3, 3)
        exp_denominator = random.choice(self.get_divisors(innerExp))

        fraction_exponent = Fraction(exp_numerator, exp_denominator)

        #print(
        #    f"({fractions_base_org} ^ {innerExp}) ^ ({fraction_exponent}) printable: {fraction_base} ^ {fraction_exponent}")

        return fractions_base_org, innerExp, fraction_base, fraction_exponent

    def calculate_answer(self, fractions_base_org, innerExp, fraction_base, fraction_exponent):
        adj_fraction_base = fraction_base
        adj_fraction_base_org = fractions_base_org
        adj_fraction_exponent = fraction_exponent

        if fraction_exponent < 0:
            adj_fraction_base = Fraction(fraction_base.denominator, fraction_base.numerator)
            adj_fraction_base_org = Fraction(fractions_base_org.denominator, fractions_base_org.numerator)
            adj_fraction_exponent = -fraction_exponent
            #print(f"adjust: {fraction_base} -> {adj_fraction_base} exp: {fraction_exponent}")

        adj_exponent = Fraction(innerExp, 1) * adj_fraction_exponent

        fraction_ans = Fraction(adj_fraction_base_org.numerator ** adj_exponent,
                                adj_fraction_base_org.denominator ** adj_exponent)

        #print(f"answer: {adj_fraction_base_org} ^ {adj_exponent} = {fraction_ans}")

        return adj_fraction_base_org, adj_exponent, fraction_ans

    def generate_problem(self)->tuple[str, str]:
        problem_text, answer_text = None, None
        fractions_base_org, fraction_base, fraction_exponent = 1, 1, 1
        fraction_exponent = Fraction(1, 1)
        ans_fraction = Fraction(1, 1)

        while fractions_base_org == 1 or fraction_exponent.denominator == 1 or ans_fraction.denominator > 1000 or ans_fraction.numerator > 1000:

            fractions_base_org, innerExp, fraction_base, fraction_exponent = self.generate_fraction()
            ans_base, ans_exp, ans_fraction = self.calculate_answer(fractions_base_org, innerExp, fraction_base,
                                                               fraction_exponent)

        problem_text = f"({fraction_base}) ^ ({fraction_exponent}) = "
        answer_text = ans_fraction

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
    FractionExponent().generate_practice(10)

if __name__ == "__main__":
    main()
