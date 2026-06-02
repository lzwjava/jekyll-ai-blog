# Base class for all flip-flops
class FlipFlop:
    def __init__(self):
        self.Q = 0  # Current state (output)
        self.Q_next = 0  # Next state (to be updated on clock tick)

    def get_output(self):
        return self.Q

    def tick(self):
        self.Q = self.Q_next  # Update state on clock tick


# RS Flip-Flop
class RSFlipFlop(FlipFlop):
    def update(self, S, R):
        if S == 1 and R == 1:
            print("Warning: Invalid state (S=1, R=1) - No change")
            return
        elif S == 1 and R == 0:
            self.Q_next = 1  # Set
        elif S == 0 and R == 1:
            self.Q_next = 0  # Reset
        # If S=0, R=0, maintain previous state (no change to Q_next)


# D Flip-Flop
class DFlipFlop(FlipFlop):
    def update(self, D):
        self.Q_next = D  # Output will become D on next clock tick


# JK Flip-Flop
class JKFlipFlop(FlipFlop):
    def update(self, J, K):
        if J == 0 and K == 0:
            pass  # No change
        elif J == 0 and K == 1:
            self.Q_next = 0  # Reset
        elif J == 1 and K == 0:
            self.Q_next = 1  # Set
        elif J == 1 and K == 1:
            self.Q_next = 1 - self.Q  # Toggle


# T Flip-Flop
class TFlipFlop(FlipFlop):
    def update(self, T):
        if T == 0:
            pass  # No change
        elif T == 1:
            self.Q_next = 1 - self.Q  # Toggle


# Function to get valid binary input (0 or 1)
def get_binary_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value in [0, 1]:
                return value
            print("Please enter 0 or 1.")
        except ValueError:
            print("Invalid input. Please enter 0 or 1.")


# Main simulation function
def simulate_flip_flop():
    print("Welcome to the Flip-Flop Simulator!")
    print("Choose a flip-flop to test:")
    print("1. RS Flip-Flop")
    print("2. D Flip-Flop")
    print("3. JK Flip-Flop")
    print("4. T Flip-Flop")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "5":
        print("Goodbye!")
        return

    if choice == "1":
        ff = RSFlipFlop()
        print("\nRS Flip-Flop: Enter S and R (0 or 1).")
        while True:
            S = get_binary_input("Enter S: ")
            R = get_binary_input("Enter R: ")
            ff.update(S, R)
            ff.tick()
            print(f"Output Q: {ff.get_output()}")
            if input("Continue? (y/n): ").lower() != "y":
                break

    elif choice == "2":
        ff = DFlipFlop()
        print("\nD Flip-Flop: Enter D (0 or 1).")
        while True:
            D = get_binary_input("Enter D: ")
            ff.update(D)
            ff.tick()
            print(f"Output Q: {ff.get_output()}")
            if input("Continue? (y/n): ").lower() != "y":
                break

    elif choice == "3":
        ff = JKFlipFlop()
        print("\nJK Flip-Flop: Enter J and K (0 or 1).")
        while True:
            J = get_binary_input("Enter J: ")
            K = get_binary_input("Enter K: ")
            ff.update(J, K)
            ff.tick()
            print(f"Output Q: {ff.get_output()}")
            if input("Continue? (y/n): ").lower() != "y":
                break

    elif choice == "4":
        ff = TFlipFlop()
        print("\nT Flip-Flop: Enter T (0 or 1).")
        while True:
            T = get_binary_input("Enter T: ")
            ff.update(T)
            ff.tick()
            print(f"Output Q: {ff.get_output()}")
            if input("Continue? (y/n): ").lower() != "y":
                break

    else:
        print("Invalid choice. Try again.")

    simulate_flip_flop()  # Restart the menu


# Run the simulator
if __name__ == "__main__":
    simulate_flip_flop()
