def gcd(x:int, y:int)->int:
    """두 수의 최대공약수(GCD)를 계산합니다."""
    while y:
        x, y = y, x % y
    return x

def lcm(x:int, y:int)->int:
    """
    두 수의 최소 공배수(LCM)를 계산합니다.
    LCM(x, y) = (|x * y|) / GCD(x, y)
    """
    # x나 y가 0이면 최소 공배수는 0입니다. (정의에 따라)
    if x == 0 or y == 0:
        return 0
    # 최소 공배수 공식 적용
    # abs() 함수를 사용하여 x * y의 절댓값을 취합니다.
    # GCD가 이미 정의되어 있으므로 이를 활용합니다.
    return abs(x * y) // gcd(x, y)