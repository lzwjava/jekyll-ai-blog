from jpype import startJVM, JVMNotFoundException, isJVMStarted, JClass


class JavaAgentConnector:
    def __init__(
        self, jar_path="/path/to/java-agent.jar", agent_class="com.example.Agent"
    ):
        self.jar_path = jar_path
        self.agent_class = agent_class
        self.agent_instance = None

    def connect(self):
        """Start JVM and load Java agent"""
        try:
            if not isJVMStarted():
                startJVM(f"-Djava.class.path={self.jar_path}", "-ea")

            # Load the agent class
            AgentClass = JClass(self.agent_class)
            self.agent_instance = AgentClass()
            print(f"Connected to Java agent: {self.agent_class}")
            return True
        except JVMNotFoundException:
            print("JVM not found. Ensure Java is installed.")
            return False
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def get_jvm_info(self):
        """Get JVM information"""
        if not self.agent_instance:
            print("Not connected to agent")
            return None
        try:
            return self.agent_instance.getJVMInfo()
        except Exception as e:
            print(f"Error getting JVM info: {e}")
            return None

    def get_memory_usage(self):
        """Get memory usage statistics"""
        if not self.agent_instance:
            print("Not connected to agent")
            return None
        try:
            return self.agent_instance.getMemoryUsage()
        except Exception as e:
            print(f"Error getting memory usage: {e}")
            return None

    def get_thread_info(self):
        """Get thread information"""
        if not self.agent_instance:
            print("Not connected to agent")
            return None
        try:
            return self.agent_instance.getThreadInfo()
        except Exception as e:
            print(f"Error getting thread info: {e}")
            return None

    def disconnect(self):
        """Disconnect from agent"""
        self.agent_instance = None
        print("Disconnected from Java agent")


# Usage example
if __name__ == "__main__":
    agent = JavaAgentConnector()

    if agent.connect():
        # Get JVM info
        jvm_info = agent.get_jvm_info()
        print("JVM Info:", jvm_info)

        # Get memory usage
        memory = agent.get_memory_usage()
        print("Memory Usage:", memory)

        # Get thread info
        threads = agent.get_thread_info()
        print("Thread Info:", threads)

        agent.disconnect()
