#!/usr/bin/env python3
"""Công cụ hỗ trợ tự học toán cơ bản theo hướng hợp lệ.

Tính năng:
- Kiểm tra đáp án người học tự nhập.
- Tạo bài luyện ngẫu nhiên và phản hồi theo bước.
"""

from __future__ import annotations

import ast
import operator
import random
from dataclasses import dataclass


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class SafeEvalError(ValueError):
    """Lỗi khi biểu thức không hợp lệ."""


def safe_eval(expr: str) -> float:
    """Đánh giá biểu thức số học an toàn với AST giới hạn."""

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](_eval(node.operand))
        raise SafeEvalError("Biểu thức chứa cú pháp không được hỗ trợ.")

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise SafeEvalError("Biểu thức không đúng cú pháp.") from exc

    return _eval(tree)


@dataclass
class Problem:
    question: str
    answer: float
    hint: str


def make_problem() -> Problem:
    """Tạo bài toán số học ngẫu nhiên để luyện tập."""
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    c = random.randint(1, 10)
    mode = random.choice(["mix", "pow", "frac"])

    if mode == "mix":
        question = f"({a} + {b}) * {c} - {b}"
        answer = (a + b) * c - b
        hint = "Tính trong ngoặc trước, sau đó nhân rồi mới trừ."
    elif mode == "pow":
        exp = random.randint(2, 3)
        question = f"{a}**{exp} - {b}"
        answer = (a**exp) - b
        hint = "Lũy thừa được thực hiện trước phép cộng/trừ."
    else:
        question = f"({a}/{c}) + ({b}/{c})"
        answer = (a / c) + (b / c)
        hint = "Cùng mẫu số thì cộng tử số rồi giữ nguyên mẫu."

    return Problem(question=question, answer=float(answer), hint=hint)


def is_close(x: float, y: float, tol: float = 1e-9) -> bool:
    return abs(x - y) <= tol


def check_answer() -> None:
    print("\n=== KIỂM TRA ĐÁP ÁN ===")
    expr = input("Nhập đề bài dạng biểu thức (ví dụ: (3/4 + 1/2) * 8): ").strip()
    your = input("Nhập đáp án của bạn: ").strip()

    try:
        correct = safe_eval(expr)
        yours = safe_eval(your)
    except SafeEvalError as exc:
        print(f"Lỗi: {exc}")
        return

    if is_close(correct, yours):
        print("✅ Chính xác! Bạn đang đi đúng hướng.")
    else:
        print(f"❌ Chưa đúng. Giá trị đúng là: {correct}")
        print("Gợi ý: kiểm tra thứ tự ưu tiên phép tính: ngoặc → lũy thừa → nhân/chia → cộng/trừ.")


def practice_round(num_questions: int = 5) -> None:
    print("\n=== LUYỆN TẬP NHANH ===")
    score = 0

    for i in range(1, num_questions + 1):
        p = make_problem()
        print(f"\nCâu {i}: {p.question}")
        raw = input("Đáp án của bạn: ").strip()
        try:
            ans = safe_eval(raw)
        except SafeEvalError:
            print("⚠️  Không đọc được đáp án. Bỏ qua câu này.")
            continue

        if is_close(ans, p.answer):
            print("✅ Đúng")
            score += 1
        else:
            print(f"❌ Sai. Đáp án: {p.answer}")
            print(f"💡 Gợi ý: {p.hint}")

    print(f"\nKết quả: {score}/{num_questions} câu đúng.")


def main() -> None:
    print("CÔNG CỤ HỖ TRỢ TỰ HỌC TOÁN (không gian lận, không tự làm bài hộ)")

    while True:
        print("\nChọn chức năng:")
        print("1) Kiểm tra đáp án tự làm")
        print("2) Luyện tập ngẫu nhiên")
        print("3) Thoát")

        choice = input("Nhập lựa chọn (1/2/3): ").strip()

        if choice == "1":
            check_answer()
        elif choice == "2":
            practice_round()
        elif choice == "3":
            print("Tạm biệt. Chúc bạn học tốt!")
            return
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
