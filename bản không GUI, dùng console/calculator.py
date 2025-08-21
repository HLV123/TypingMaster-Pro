# calculator.py

def calculate_wpm(user_input: str, elapsed_time: float) -> float:
    """
    Calculates Words Per Minute (WPM).
    A "word" is defined as 5 characters.
    """
    if elapsed_time == 0:
        return 0.0
    
    num_chars = len(user_input)
    # The standard formula for WPM
    wpm = (num_chars / 5) / (elapsed_time / 60)
    return wpm

def calculate_accuracy(original_sentence: str, user_input: str) -> float:
    """
    Calculates the accuracy of the user's typing.
    """
    correct_chars = 0
    original_len = len(original_sentence)

    for i in range(original_len):
        try:
            if user_input[i] == original_sentence[i]:
                correct_chars += 1
        except IndexError:
            # User typed less than the original sentence
            break
            
    if original_len == 0:
        return 0.0
        
    accuracy = (correct_chars / original_len) * 100
    return accuracy