# Trackr Version 1.0

## Overview
Trackr is a tool that uses linear regression models to predict profit values. This tool is intended for use by retail businesses looking to increase their yearly profit margins.

### Features

| Feature                | Description                                                                                         |
| ----------------       | -------------                                                                                       |
| **Open File button**   | Opens a dialog box to retrieve the user data file for analysis.                                     |
| **Open File**          | Opens file explorer dialog.                                                                         |
| **Select Input**       | Selects independent variables that predict your outcome                                             |
|**Select Output**       | Selects dependent variables in relation to the input.                                               |
| **Confirm Selections** | Generates the data once input and output selected. A dialog appears when this button is selected.   |
|**Generate model**      | Creates linear regression chart and the model formula.                                              |

## System Requirements
| Operating system | Requirements |
| ---------------- | -------------            |
| Windows          | *Windows XP or higher    |
| Mac              | *Mac OS 11 or higher     |

## Installation Instructions

## Using Trackr

### Opening data files
To start using Trackr, you must open a data file. Trackr works with Excel (.xls), Data Base (.db), and Comma Separated Values (.csv) files.
1. Open Trackr and select Open File. <br>
   The File Explorer dialog appears.
2. Select a file > Open. <br>
   The Linear Regression chart appears with data values. <br>
   ![2024-11-12_12-24-32](https://github.com/user-attachments/assets/1684d3a5-e3a9-4041-99ce-18c156f69298)
   Note: Trackr can only work with excel, Data Base, and CSV files. <br>
3. Select values for input and output.
4.  Select Confirm Selections > OK. <br>
   The Preprocessing Options selections appear.
   
### Processing and saving data files
You can process each file to remove not a number (NaN) values, fill with mean, median, or a constant value. Note that you must remove NaN values if they are in your data file before you generate a model.

1. Select your preprocessing option values, then select Gernerate model > OK. <br>
   The model formula graph appears with the description box.
2. Select the description box and write a description. <br>
![2024-11-12_12-26-51](https://github.com/user-attachments/assets/6f2ee389-feed-4bbe-9c32-22ba9dca6bfb)
   Note: You must write a description in order to save the file.
4. Select Save Model. <br>
   The File explorer dialog appears. 
5. Select Save > OK.

### Loading saved data files


## Contributing to Trackr

To contribute, please contact the creator of Trackr through GitHub (Fiz Garrido Escudero). We welcome any contributions to this project. 

### Guidelines
**Contribution Process**:
  1. Fork the repository.
  2. Create a new branch for your feature or bug fix.
  3. Make any changes, then commit.
  4. Submit a pull request.

### Reporting Issues
If you find a bug or want to suggest a feature, please open an issue [here](https://github.com/fizge/1-SENECA-UDC_Coil_Proyect/issues/new).

### Documentation
Please update documentation as needed.

## Acknowledgements 
