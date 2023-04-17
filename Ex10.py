
class TestEx10:
    phrase = input("Set a phrase: ")
    assert len(phrase) <= 15, f"Длина строки должна быть не более 15 символов"
    print(f"Длина строки: {len(phrase)} символов")
