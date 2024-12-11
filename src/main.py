"""
Main Entry Point for DataPilot

This script initializes and launches the DataPilot application
Modules:
    - scenarios.initial_scenario: Contains the main application class `LinearRegressionAnalyitics`.

Usage:
    Execute this script directly to run the application.

Author: Group 1
Date: [11/12/2024]
"""

from scenarios.initial_scenario import DataPilot

# Check if the script is executed directly
if __name__ == "__main__":
    # Create an instance of DataPilot class
    app = DataPilot()

    # Initialize the main application window
    app.create_window()

    # Display the welcome/presentation screen
    app.gui_presentation()

    # Start the main event loop to keep the application running
    app.v.mainloop()
