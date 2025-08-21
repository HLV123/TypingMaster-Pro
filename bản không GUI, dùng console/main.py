# main.py
import time
import sentences
import calculator
import ui

def run_test():
    """Main function to run the typing test."""
    # 1. Welcome message
    ui.display_welcome()

    # 2. Get a random sentence
    sentence_to_type = sentences.get_random_sentence()
    ui.display_sentence(sentence_to_type)

    # 3. Get user input and time it
    # We record time right before and after the input() call
    # Note: A more precise way would involve more complex libraries, 
    # but this is great for a simple project.
    
    # Wait for user to be ready (handled inside get_user_input)
    # The clock starts AFTER they press Enter to be ready
    start_time = time.time()
    user_typed_text = input("> ") # A simplified version of get_user_input for timing
    end_time = time.time()

    # 4. Calculate elapsed time
    elapsed_time = end_time - start_time

    # 5. Calculate results
    wpm = calculator.calculate_wpm(user_typed_text, elapsed_time)
    accuracy = calculator.calculate_accuracy(sentence_to_type, user_typed_text)

    # 6. Display results
    ui.display_results(wpm, accuracy, elapsed_time)

# This makes the script executable
if __name__ == "__main__":
    run_test()