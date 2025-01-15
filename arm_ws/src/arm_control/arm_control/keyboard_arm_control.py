#!/usr/bin/env python3

# Import necessary ROS2 and Python libraries
import rclpy  # ROS2 library for initializing and managing nodes
from rclpy.node import Node  # Base class for creating ROS2 nodes
from geometry_msgs.msg import Twist  # Message type for velocity commands
import termios  # Library for controlling terminal input settings
import sys  # Provides access to system-specific parameters and functions
import tty  # Library for terminal control functions

# Define a class for controlling the robotic arm using keyboard input
class KeyboardArmControl(Node):
    def __init__(self):
        # Initialize the ROS2 node with the name 'keyboard_arm_control'
        super().__init__('keyboard_arm_control')
        
        # Create a publisher to send Twist messages on the '/arm_cmd_vel' topic
        self.publisher_ = self.create_publisher(Twist, '/arm_cmd_vel', 10)
        
        # Log a message indicating that the node is initialized
        self.get_logger().info('Keyboard Arm Control Node Initialized')
        
        # Start the keyboard input loop
        self.run()

    # Method to capture a single key press from the terminal
    def get_key(self):
        
        try:
            # Set the terminal to raw mode to read single key presses
            tty.setraw(sys.stdin.fileno())
            
            # Read one character from the standard input
            key = sys.stdin.read(1)
        finally:
            # Restore the terminal settings to normal mode
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
        
        # Return the key pressed
        return key

    # Main method to process keyboard input and publish Twist messages
    def run(self):
        # Create a Twist message object to store velocity commands
        msg = Twist()
        try:
            # Infinite loop to continuously read keyboard input
            while True:
                # Get a key press from the user
                key = self.get_key()
                
                # Map key presses to arm movements
                if key == 'w':  # 'w' key: Move arm up
                    msg.linear.z += 0.1  # Increment z-axis linear velocity
                elif key == 's':  # 's' key: Move arm down
                    msg.linear.z -= 0.1  # Decrement z-axis linear velocity
                elif key == 'a':  # 'a' key: Rotate arm left
                    msg.angular.z += 0.1  # Increment z-axis angular velocity
                elif key == 'd':  # 'd' key: Rotate arm right
                    msg.angular.z -= 0.1  # Decrement z-axis angular velocity
                elif key == 'q':  # 'q' key: Quit the program
                    self.get_logger().info('Quitting...')
                    break  # Exit the loop and terminate the node
                else:
                    continue  # Ignore any other key presses
                
                # Publish the updated velocity command
                self.publisher_.publish(msg)
                
                # Log the published command for debugging
                self.get_logger().info(f'Publishing: {msg}')
        except KeyboardInterrupt:
            self.get_logger().info('Keyboard Interrupt received, stopping node...')
        finally:
            self.get_logger().info('Shutting down Keyboard Arm Control Node...')


# Main entry point for the script
def main(args=None):
    # Initialize the ROS2 system
    rclpy.init(args=args)
    
    # Create an instance of the KeyboardArmControl node
    node = KeyboardArmControl()
    
    try:
        rclpy.spin(node)  # Keep the node running
    except KeyboardInterrupt:
        pass  # Graceful shutdown on interrupt
    finally:
        node.destroy_node()  # Explicitly destroy the node
        rclpy.shutdown()  # Clean up ROS2
        print("Node has been shut down.")  # Ensure user feedback after shutdown

# Standard Python script entry point
if __name__ == '__main__':
    main()
