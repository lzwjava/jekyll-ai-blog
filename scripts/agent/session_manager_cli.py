import sys
import os
import threading
import queue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.llm.openrouter_client import call_openrouter_api_with_messages

# Dictionary to store sessions, each with a name, conversation history, and status
sessions = {}
current_session = None
# Queue to handle responses from background threads
response_queue = queue.Queue()


def call_api_in_background(session_name, conversation):
    try:
        answer = call_openrouter_api_with_messages(conversation)
        response_queue.put((session_name, answer))
    except Exception as e:
        response_queue.put((session_name, str(e)))
    finally:
        sessions[session_name]["status"] = "idle"


def main():
    print("Hello! I'm GitHub Copilot. Manage multiple AI chat sessions.")
    print("Commands:")
    print("- new <name>: Create a new session with given name")
    print("- list: List all sessions")
    print("- a <name>: Attach to a session")
    print("- ask <message>: Send message to AI for current session")
    print("- exit or quit: Stop the program")

    global current_session
    while True:
        # Check for responses from background threads
        while not response_queue.empty():
            session_name, result = response_queue.get()
            if isinstance(result, str) and result.startswith("Error"):
                print(f"Error for session {session_name}: {result}")
            else:
                if result:
                    sessions[session_name]["history"].append(
                        {"role": "assistant", "content": result}
                    )
                    if session_name == current_session:
                        print(f"**AI Response for {session_name}:**\n{result}")
                else:
                    print(f"No response received for session {session_name}.")
            response_queue.task_done()

        session_info = (
            f"Current Session: {current_session if current_session else 'None'}"
        )
        user_input = input(f"{session_info} You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if user_input.startswith("new "):
            name = user_input[4:].strip()
            if name:
                if name not in sessions:
                    sessions[name] = {"history": [], "status": "idle"}
                    print(f"Created session: {name}")
                else:
                    print(f"Session {name} already exists")
            else:
                print("Please provide a session name")

        elif user_input == "list":
            if sessions:
                print("Sessions:")
                for name in sessions:
                    status = (
                        f"Status: {sessions[name]['status']}"
                        if name == current_session
                        else ""
                    )
                    attached = "Attached" if name == current_session else ""
                    print(f"- {name} {attached} {status}")
            else:
                print("No sessions available")

        elif user_input.startswith("a "):
            name = user_input[2:].strip()
            if name in sessions:
                current_session = name
                print(f"Attached to session: {name}")
            else:
                print(f"Session {name} does not exist")

        elif user_input.startswith("ask "):
            if current_session:
                message = user_input[4:].strip()
                if message:
                    if sessions[current_session]["status"] == "busy":
                        print(
                            f"Session {current_session} is currently busy. Try again later."
                        )
                    else:
                        sessions[current_session]["history"].append(
                            {"role": "user", "content": message}
                        )
                        sessions[current_session]["status"] = "busy"
                        print(
                            f"Sending message to AI for session {current_session} in background..."
                        )
                        thread = threading.Thread(
                            target=call_api_in_background,
                            args=(
                                current_session,
                                sessions[current_session]["history"],
                            ),
                        )
                        thread.daemon = True
                        thread.start()
                else:
                    print("Please provide a message to send.")
            else:
                print("No session attached. Use 'a <name>' to attach to a session")

        else:
            print("Unknown command. Use new, list, a, ask, exit")


if __name__ == "__main__":
    main()
