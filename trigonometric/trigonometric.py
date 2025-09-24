import math
import os
import sys
import random
from fractions import Fraction
from sympy import sqrt, Rational, simplify

from utils import pdf
from utils.unicodes import UNICODE_SQUARE_ROOT, UNICODE_DEGREE_CIRCLE


class Trigonometric():
    """
        삼각함수의 덧셈 정리를 사용하여 sin, cos, tan 문제와 분수 형태의 답을 생성하는 클래스
        """

    # 특수각의 sin, cos 값을 Fraction 객체로 미리 정의합니다.
    # tan는 sin/cos으로 계산합니다.
    # SymPy의 Rational과 sqrt를 사용하여 특수각 값을 정의합니다.
    SPECIAL_VALUES = {
        0: {'sin': Rational(0), 'cos': Rational(1)},
        30: {'sin': Rational(1, 2), 'cos': Rational(1, 2) * sqrt(3)},  # 1/2 * sqrt(3)
        45: {'sin': Rational(1, 2) * sqrt(2), 'cos': Rational(1, 2) * sqrt(2)},  # 1/2 * sqrt(2)
        60: {'sin': Rational(1, 2) * sqrt(3), 'cos': Rational(1, 2)},  # 1/2 * sqrt(3)
        90: {'sin': Rational(1), 'cos': Rational(0)},
        180: {'sin': Rational(0), 'cos': Rational(-1)},
    }

    def __init__(self):
        self.title = "Trigonometric"
        pass

    def get_tan(self, angle):
        """특정 각도의 tan 값을 계산하여 반환합니다."""
        if angle % 180 == 90 or angle % 180 == -90:
            # 90도, 270도 등 (tan이 정의되지 않거나 무한대)
            return 'undefined'
        if angle < 0:
            angle = angle % 360  # 각도를 [0, 360) 범위로 정규화

        sin_val = self.SPECIAL_VALUES.get(angle, {}).get('sin')
        cos_val = self.SPECIAL_VALUES.get(angle, {}).get('cos')

        if sin_val is None or cos_val is None:
            # 특수각 범위 외의 각도는 처리하지 않습니다.
            return None

        if cos_val == 0:
            return 'undefined'

        # 분수 형태를 유지하기 위해 Fraction 객체를 사용합니다.
        # math.sqrt 값이 포함되어 있어 Fraction으로 바로 변환은 어렵지만,
        # 이 코드에서는 문자열로 분수를 표현하는 데 초점을 맞춥니다.
        # 따라서, 여기서는 문자열로 반환하는 로직을 따르겠습니다.
        if math.sqrt(2) in [sin_val.numerator, cos_val.numerator]:
            # 루트가 포함된 값의 정확한 tan 계산은 복잡하므로,
            # 단순화를 위해 특수각이 아닌 경우를 배제합니다.
            return sin_val / cos_val if cos_val != 0 else 'undefined'

        return sin_val / cos_val if cos_val != 0 else 'undefined'

    def get_value(self, angle, func):
        """특수각의 sin, cos 값을 반환합니다. 180도를 넘거나 음수인 경우를 처리합니다."""

        # 각도를 [0, 360) 범위로 정규화
        angle = angle % 360
        if angle < 0:
            angle += 360

        # 4사분면 주기성을 이용해 [0, 90] 범위의 값으로 변환
        sign = 1

        if angle > 270:  # 4사분면 (270 ~ 360)
            angle = 360 - angle
            if func == 'sin':
                sign = -1
            elif func == 'tan':
                sign = -1
        elif angle > 180:  # 3사분면 (180 ~ 270)
            angle = angle - 180
            if func == 'sin':
                sign = -1
            elif func == 'cos':
                sign = -1
            elif func == 'tan':
                sign = 1  # 양수
        elif angle > 90:  # 2사분면 (90 ~ 180)
            angle = 180 - angle
            if func == 'cos':
                sign = -1
            elif func == 'tan':
                sign = -1

        if func == 'tan':
            # tan 값은 sin/cos으로 계산
            sin_val = self.SPECIAL_VALUES.get(angle, {}).get('sin', 0)
            cos_val = self.SPECIAL_VALUES.get(angle, {}).get('cos', 0)
            if cos_val == 0:
                return 'undefined'
            return sign * (sin_val / cos_val)

        value = self.SPECIAL_VALUES.get(angle, {}).get(func, 0)
        return sign * value

    def format_radical_fraction(self, value):
        """루트(sqrt)가 포함된 분수를 LaTeX 형태로 문자열 포맷팅"""

        # Fraction 객체를 문자열로 변환 (루트 포함된 값은 math.sqrt를 사용)
        if isinstance(value, str) and value == 'undefined':
            return '정의되지 않음 (Undefined)'

        if isinstance(value, (int, float, Fraction)):
            # Fraction 객체 처리
            if isinstance(value, Fraction):
                numerator = value.numerator
                denominator = value.denominator
            else:
                # 정수나 실수(0)인 경우
                numerator = value
                denominator = 1

            # 여기서 Fraction 객체 내에 math.sqrt(2), math.sqrt(3)가 있는지 확인하는 로직이 필요하지만,
            # math.sqrt 결과는 float이므로 Fraction 객체에 직접 들어가지 않습니다.
            # 따라서, 코드를 단순화하여 특수각 값만 처리하도록 구현하겠습니다.
            # 만약 math.sqrt를 포함한 값을 처리하려면, 기호화된 수학 라이브러리(sympy)가 필요합니다.

            # 여기서는 특수각 조합으로 나오는 값들(예: (sqrt(6)-sqrt(2))/4)을
            # LaTeX 분수 형태로 출력하는 예시를 보여줍니다.

            # 이 문제는 일반적인 파이썬의 한계를 넘어 SymPy 같은 라이브러리를 써야
            # 루트를 포함한 분수를 깔끔하게 처리할 수 있습니다.

            # 임시로 가장 흔한 분수 값만 Fraction의 기본 기능으로 포맷팅합니다.
            if denominator == 1:
                return str(numerator)

            # 이 예제에서는 SymPy를 사용하지 않으므로, 일반적인 분수 형태로만 출력합니다.
            return f"{numerator}/{denominator}"

        return str(value)


    def calculate_trigonometric_addition_subtraction(self, trigonometric, angle1, angle2, operation)->str:

        trigonometic_answer_map = {'sin15': f'{UNICODE_SQUARE_ROOT}6/4 - {UNICODE_SQUARE_ROOT}2/4',
                                   'sin30': '1/2',
                                   'sin45': f'{UNICODE_SQUARE_ROOT}2/2',
                                   'sin60': f'{UNICODE_SQUARE_ROOT}3/2',
                                   'sin75': f'{UNICODE_SQUARE_ROOT}6/4 + {UNICODE_SQUARE_ROOT}2/4',
                                   'sin90': '1',
                                   'sin105': f'{UNICODE_SQUARE_ROOT}6/4 + {UNICODE_SQUARE_ROOT}2/4',
                                   'sin120': f'{UNICODE_SQUARE_ROOT}3/2',
                                   'sin135': f'{UNICODE_SQUARE_ROOT}2/2',
                                   'sin150': '1/2',
                                   'sin210': '-1/2',
                                   'sin225': f'-{UNICODE_SQUARE_ROOT}2/2',
                                   'sin240': f'{UNICODE_SQUARE_ROOT}3/2',
                                   'sin270': '-1',
                                   'cos15': f'{UNICODE_SQUARE_ROOT}6/4 + {UNICODE_SQUARE_ROOT}2/4',
                                   'cos30': f'{UNICODE_SQUARE_ROOT}3/2',
                                   'cos45': f'{UNICODE_SQUARE_ROOT}2/2',
                                   'cos60': '1/2',
                                   'cos75': f'{UNICODE_SQUARE_ROOT}6/4 - {UNICODE_SQUARE_ROOT}2/4',
                                   'cos90': '0',
                                   'cos105': f'{UNICODE_SQUARE_ROOT}2/4 - {UNICODE_SQUARE_ROOT}6/4',
                                   'cos120': '-1/2',
                                   'cos135': f'-{UNICODE_SQUARE_ROOT}2/2',
                                   'cos150': f'-{UNICODE_SQUARE_ROOT}3/2',
                                   'cos210': f'-{UNICODE_SQUARE_ROOT}3/2',
                                   'cos225': f'-{UNICODE_SQUARE_ROOT}2/2',
                                   'cos240': '-1/2',
                                   'cos270': '-0',
                                   'tan15': f'2 - {UNICODE_SQUARE_ROOT}3',
                                   'tan30': f'{UNICODE_SQUARE_ROOT}3/3',
                                   'tan45': '1',
                                   'tan60': f'{UNICODE_SQUARE_ROOT}3',
                                   'tan75': f'2 + {UNICODE_SQUARE_ROOT}3',
                                   'tan90': 'undefined',
                                   'tan105': f'{UNICODE_SQUARE_ROOT}3 - 2',
                                   'tan120': f'-{UNICODE_SQUARE_ROOT}3',
                                   'tan135': '-1',
                                   'tan150': f'-{UNICODE_SQUARE_ROOT}3/3',
                                   'tan210': f'{UNICODE_SQUARE_ROOT}3/3',
                                   'tan225': '1',
                                   'tan240': f'{UNICODE_SQUARE_ROOT}3',
                                   'tan270': 'undefined',
                                   }
        # ----------------------------------------------------
        # 2. 덧셈 정리를 이용한 정답 계산
        # ----------------------------------------------------
        angle_final = angle1 + angle2 if operation == '+' else angle1 - angle2

        if trigonometric == 'tan' and angle_final == 90:
            return "undefined"

        # 각 A, B의 sin, cos 값 가져오기
        sinA = self.get_value(angle1, 'sin')
        cosA = self.get_value(angle1, 'cos')
        sinB = self.get_value(angle2, 'sin')
        cosB = self.get_value(angle2, 'cos')

        if trigonometric == 'sin':
            # sin(A ± B) = sinA cosB ± cosA sinB
            term1 = sinA * cosB
            term2 = cosA * sinB

            if trigonometric == '+':
                result = term1 + term2
            else:
                result = term1 - term2

        elif trigonometric == 'cos':
            # cos(A ± B) = cosA cosB ∓ sinA sinB
            term1 = cosA * cosB
            term2 = sinA * sinB

            if trigonometric == '+':
                result = term1 - term2  # 부호 반대
            else:
                result = term1 + term2  # 부호 반대

        if trigonometric == 'tan':
            # sin(A ± B) = sinA cosB ± cosA sinB
            term1 = sinA * cosB
            term2 = cosA * sinB

            if trigonometric == '+':
                sin_result = term1 + term2
            else:
                sin_result = term1 - term2

            # cos(A ± B) = cosA cosB ∓ sinA sinB
            term1 = cosA * cosB
            term2 = sinA * sinB

            if trigonometric == '+':
                cos_result = term1 - term2  # 부호 반대
            else:
                cos_result = term1 + term2  # 부호 반대

            result = sin_result / cos_result

        # ----------------------------------------------------
        # 3. 정답 포맷팅
        # ----------------------------------------------------

        # **참고**: `self.get_value`에서 반환된 값은 `math.sqrt(2)`와 같은 float을 포함하는
        # `Fraction` 객체입니다. 파이썬의 표준 `Fraction`은 루트를 포함하지 못합니다.
        # 따라서, 이 코드는 루트가 포함된 값을 `Fraction` 객체로만 표현하는 데는 한계가 있습니다.
        # 이 예제에서는 계산된 `result`를 문자열로 간결하게 표현합니다.

        # 가장 흔한 답들을 문자열로 치환하여 분수 표현을 시뮬레이션합니다.
        answer_text = ""

        if angle_final == 75 or angle_final == 15:  # 75 = 30+45 or 15 = 45-30
            if trigonometric == 'sin':
                if angle_final == 75:
                    answer_text = "(\u221a6 + \u221a2) / 4"
                else:
                    answer_text = "(\u221a6 - \u221a2) / 4"
            elif trigonometric == 'cos':
                if angle_final == 75:
                    answer_text = "(\u221a6 - \u221a2) / 4"  # sin(15)와 동일
                else:
                    answer_text = "(\u221a6 + \u221a2) / 4"  # sin(75)와 동일

        elif angle_final == 105 or angle_final == 90:
            # sin(105) = (√6 + √2)/4, cos(105) = (√2 - √6)/4
            if trigonometric == 'sin':
                answer_text = "(\u221a6 + \u221a2) / 4"
            elif trigonometric == 'cos':
                answer_text = "(\u221a2 - \u221a6) / 4"

        # 특수각 값이 나오면 Fraction으로 처리 (예: sin(90) = 1)
        if angle_final in [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 210, 225, 240, 270]:
            answer_text = trigonometic_answer_map[f"{trigonometric}{angle_final}"]

        return answer_text

    def generate_problem(self)->(str, str):

        trigonometric = ['sin', 'cos', 'tan']
        angle_list = [30, 45, 60, 90, 180]

        trigonometric_choice = random.choice(trigonometric)
        angle_choice = random.sample(angle_list, 2)
        operation_choice = random.choice(['+', '-'])
        angle1 = angle_choice[0]
        angle2 = angle_choice[1]
        if operation_choice == '-' and angle2 > angle1 :
                angle1, angle2 = angle2, angle1

        # 문제 각도 (A ± B)
        angle_final = angle1 + angle2 if operation_choice == '+' else angle1 - angle2


        problem_text = f"{trigonometric_choice}({angle1}{UNICODE_DEGREE_CIRCLE}{operation_choice}{angle2}{UNICODE_DEGREE_CIRCLE}) = "
        answer_text = self.calculate_trigonometric_addition_subtraction(trigonometric_choice, angle1, angle2, operation_choice)
        return problem_text, answer_text

    def get_problem_answer(self) -> (str, str):

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
            pdf.generate_pdf_files(f"{self.title} Answers", answer_list, num_column=2)
            print("PDF 파일이 성공적으로 생성되었습니다.")
        except ImportError:
            print("Error: 'pdf_handling' 모듈을 찾을 수 없습니다.")
        except AttributeError:
            print("Error: 'pdf_handling' 모듈에 'generate_pdf_files' 함수가 없습니다.")

def main():
    Trigonometric().generate_practice(100)

if __name__ == "__main__":
    main()