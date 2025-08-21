# ui.py

def display_welcome():
    """Displays a welcome message."""
    print("--- Typing Speed Calculator ---")
    print("Type the sentence below as fast and accurately as you can.")

def display_sentence(sentence: str):
    """Displays the sentence for the user to type."""
    print("\nSentence to type:")
    print(f'"{sentence}"')

def get_user_input() -> str:
    """Gets typing input from the user."""
    input("Press Enter when you are ready to start...")
    print("\nStart typing now!")
    user_text = input("> ")
    return user_text

def display_results(wpm: float, accuracy: float, time_taken: float):
    """Displays the final results."""
    print("\n--- Results ---")
    print(f"Time taken: {time_taken:.2f} seconds")
    print(f"Your typing speed: {wpm:.2f} WPM")
    print(f"Accuracy: {accuracy:.2f}%")
    print("----------------")