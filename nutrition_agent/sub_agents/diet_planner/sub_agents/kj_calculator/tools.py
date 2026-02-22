def nutrition_calculator(expression: str) -> str:
    """
    Evaluates mathematical expressions for nutrition logic.
    Args:
        expression: A math string like '(8700 - 2500) / 4.18'
    """
    # 1 kcal = 4.184 kJ (Standard Australian Conversion)
    try:
        # Using a simple eval for demo purposes
        result = eval(expression)
        return f"Calculation Result: {result:.2f}"
    except Exception as e:
        return f"Math Error: {str(e)}"

def check_daily_limit(current_kj: float, target_kj: float) -> str:
    """Compares current intake against the Australian daily target."""
    if current_kj > target_kj:
        diff = current_kj - target_kj
        return f"Over limit by {diff:.2f} kJ. Suggestions: Increase activity or reduce next meal."
    else:
        diff = target_kj - current_kj
        return f"Under limit by {diff:.2f} kJ. You have room for a healthy snack!"