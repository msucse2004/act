import os
import random
import sys

from utils import pdf


class Sequence:
    def __init__(self):
        self.title = "Sequence"
        self.sequences_type = ["geometric", "arithmetic", "combined"]
        self.requested_type = []
        self.sequences = []
        self.current_sequence_type = None
        self.initialize_sequences(None)
        self.common_differnece = 0
        self.common_ratio = 0

    def arithmetic_sequence_nth_term(self, a1, n, d):
        return a1 + (n - 1) * d

    def geometric_sequence_nth_term(self, a1, n, r):
        return a1 * r ** (n - 1)

    def combined_sequence_nth_term(self, a1, n, r, d):
        if n == 1 or n == 0:
            return a1
        else:
            return r * self.combined_sequence_nth_term(a1, n - 1, r, d) + d

    def sequence_sum(self, s, e):
        sum = 0
        for i in range(s, e + 1):
            sum += self.sequences[i]
        return sum

    def initialize_sequences(self, sequence_type:str=None):
        coef = random.randint(-10, 10)
        init_value = random.randint(1, 10)
        if random.choice([True, False]):
            init_value = init_value * -1

        if sequence_type == 'geometric' or sequence_type is None:
            # coef = coef // 2
            while coef == 0 or coef == 1 or  abs(coef) > 5:
                coef = random.randint(-5, 5)

            init_value = init_value // 10
            while init_value == 0:
                init_value = random.randint(-10, 10)


        self.sequences.clear()
        self.sequences.append(init_value)
        self.current_sequence_type = sequence_type
        if sequence_type == "arithmetic":
            self.common_differnece = coef
            for i in range(0, 100):
                self.sequences.append(self.arithmetic_sequence_nth_term(init_value, i + 2, self.common_differnece))

        elif sequence_type == "geometric":
            self.common_ratio = coef
            for i in range(0, 100):
                self.sequences.append(self.geometric_sequence_nth_term(init_value, i + 2, self.common_ratio))

        elif sequence_type == "combined":
            while True:
                self.common_ratio = random.randint(-5, 5)
                self.common_differnece = random.randint(-10, 10)
                if (self.common_ratio - 1) != 0 and self.common_differnece % (self.common_ratio - 1) == 0 and abs(self.common_ratio) > 1:
                    break  #

            for i in range(0, 100):
                self.sequences.append(self.combined_sequence_nth_term(init_value, i + 2, self.common_ratio, self.common_differnece))

        else:
            print("Invalid sequence type")


    def make_sequence_problem(self, sequences_type:str=None):

        """
        문제 유형
        등차수열
        1. 다음 수열의 n항을 구하시오
        2. 공차를 구하시오
        3. 몇번째 term 인지 구하시오
        4. 등차수열 처음으로 100보다 크게 되는 항
        5. 첫째항이 -5, 제 10항이 13 일때 첫째항부터 제 10항 까지 합
        6. 첫째항이 4, 공차가 3 일때 제 8항까지 합
        7. 첫째항부터 제 4항까지 합이 32, 첫째항부터 제 10항까지의 합이 140인 등차수열의 첫째항과 공차를 구하시오

        등비수열
        1. 등비수열의 공비를 구하시오
        2. 제 3항이 9, 제 4항이 3인 등비수열의 제 5항을 구하시오
        3. 연이율이 2%이고 1년마다 복리로 매년 초에 100만원씩 10년동안 적립할때, 10년째 말의 적립금의 원리합계를 구하시오 (단 1.02^10 = 1.2로 계산한다)
        4. 제1항 부터 제 5항까지 등비수열의 합
        5. 등비수열의 합이 > 128을 만족시키는 n 의 최소값을 구하시오
        6. 모든항이 양수이고 첫째항부터 제 2항까지의 합이 4, 첫째항부터 제4항 까지의 합이 40인 등비수열의 첫째항과 공비를 구하시오
        7. 어떤 세균이 1회 분열할 때마다 그 수가 2배씩 증가한다, 처음 세균수가 1일때 그 세균의 수가 1024 이상이 되려면 최소한 몇번 분열해야 하는가
        8. 등비수열 An 에 대하여 a3=2, a5=250일 때 공비를 구하시오
        """

        self.initialize_sequences(sequences_type)
        problem_text, answer_text = None, None

        if sequences_type == "arithmetic":
            required_term = random.randint(6, 100)
            required_term2 = random.randint(10, 100)
            arithmetic_problem_type = [
                f"[{', '.join(str(self.sequences[i]) for i in range(0, 10))}, ...] find {required_term}th term",
                f"[{', '.join(str(self.sequences[i]) for i in range(0, 10))}, ...] find Common Differnece",
                f"[{', '.join(str(self.sequences[i]) for i in range(0, 10))}, ...] find which term {self.sequences[required_term]} is.",
                f"In Arithmetic sequences, a1: {self.sequences[1]}, a{required_term}: {self.sequences[required_term]}, sum from 1st term to {required_term}th term",
                f"a1: {self.sequences[1]}, Common Difference: {self.sequences[2] - self.sequences[1]}, sum from 1st term to {required_term}th term",
                f"In Arithmetic sequences, sum of 1st term to {required_term}th term is {self.sequence_sum(1, required_term)} and sum of 1st term to {required_term2}th term is {self.sequence_sum(1, required_term2)} find 1st term"
            ]
            arithmetic_answer = [f"{self.sequences[required_term]}",
                                 f"{self.sequences[2] - self.sequences[1]}",
                                 f"{required_term}",
                                 f"{self.sequence_sum(1, required_term)}",
                                 f"{self.sequence_sum(1, required_term)}",
                                 f"{self.sequences[1]}"
                                 ]
            random_item = random.choice(arithmetic_problem_type)
            random_index = arithmetic_problem_type.index(random_item)


            problem_text = arithmetic_problem_type[random_index]
            answer_text = arithmetic_answer[random_index]
            pass
        elif sequences_type == "geometric":
            required_term = random.randint(6, 10)
            required_term2 = random.randint(1, 5)
            geometric_problem_type = [
                f"[{', '.join(str(self.sequences[i]) for i in range(0, 10))}, ...] find {required_term}th term",
                f"[{', '.join(str(self.sequences[i]) for i in range(0, 10))}, ...] find Common Ratio",
                f"[{', '.join(str(self.sequences[i]) for i in range(0, 10))}, ...] find which term {self.sequences[required_term]} is.",
                f"In geometry sequences, a1: {self.sequences[1]}, a{required_term}: {self.sequences[required_term]}, sum from 1st term to {required_term}th term",
                f"a1: {self.sequences[1]}, Common Ratio: {self.sequences[2] // self.sequences[1]}, sum from 1st term to {required_term}th term"

            ]
            geometric_answer = [f"{self.sequences[required_term]}",
                                f"{self.sequences[2] // self.sequences[1]}",
                                f"{required_term}",
                                f"{self.sequence_sum(1, required_term)}",
                                f"{self.sequence_sum(1, required_term)}",
                                f"{self.sequences[1]}"
                                ]
            random_item = random.choice(geometric_problem_type)
            random_index = geometric_problem_type.index(random_item)


            problem_text = geometric_problem_type[random_index]
            answer_text = geometric_answer[random_index]
            pass
        elif sequences_type == "combined":
            required_term = random.randint(3, 8)

            combined_problem_type = [
                f"Multiplying by {self.common_ratio}, and adding {self.common_differnece}, if 1st term is {self.sequences[1]}, find {required_term}th term"
            ]

            combined_answer = [f"{self.sequences[required_term]}"

                               ]
            random_item = random.choice(combined_problem_type)
            random_index = combined_problem_type.index(random_item)


            problem_text = combined_problem_type[random_index]
            answer_text = combined_answer[random_index]

        else:
            print(f"Invalid sequences type: {sequences_type}")

        return problem_text, answer_text

    def generate_problem(self)->tuple[str, str]:
        problem_text, answer_text = None, None

        type_choice = random.choice(self.requested_type)
        problem_text, answer_text = self.make_sequence_problem(type_choice)

        return problem_text, answer_text
    def get_problem_answer(self) -> tuple[str, str]:
        problem_text, answer_text = None, None

        while problem_text is None:
            problem_text, answer_text = self.generate_problem()
        print(f"{problem_text} : {answer_text}")

        return problem_text, answer_text

    def generate_practice(self, requested_type:list[str], number_of_problems: int = 10):
        num_of_problems = 0
        problem_list = []
        answer_list = []

        if "all" in requested_type:
            self.requested_type = self.sequences_type
        else:
            self.requested_type = requested_type

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
    # requested type: "geometric", "arithmetic", "combined", "all"
    Sequence().generate_practice(["all"], 100)

if __name__ == "__main__":
    main()