# StatWizard Version 1.0

## Overview
StatWizard is a tool that uses linear regression models to predict profit values. This tool is intended for use by retail businesses looking to increase their yearly profit margins. Users can use their own data model stored as an excel, data base, or comma separated values (csv) file to generate data predictions by adding their own values.

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
Before downloading StatWizard, ensure your device meets the system requirements. While the installation process differs slightly for Mac and Windows, the StatWizard interface and features are identical on both platforms.

### To install StatWizard 
1. On your browser, visit StatWizard's [Download page](www.placeholderstatwizardweb.com).
2. Select the download link that fits your system requirements (See System Requirements Table)
STILL EDITING :))) - Cristine

## Using StatWizard

### StatWizard interface


### Opening data files
To start using StatWizard, you must open a data file. StatWizard works with Excel (.xls), Data Base (.db), and Comma Separated Values (.csv) files.
1. Open StatWizard and select Open File. <br>
   The File Explorer dialog appears.
2. Select a file > Open. <br>
   The Linear Regression chart appears with data values. <br>
   ![2024-11-12_12-24-32](https://github.com/user-attachments/assets/1684d3a5-e3a9-4041-99ce-18c156f69298)
   Note: StatWizard can only work with excel, Data Base, and CSV files. <br>
3. Select values for input and output.
4.  Select Confirm Selections > OK. <br>
   The Preprocessing Options selections appear.
   
### Processing and saving data files
You can process each file to remove not a number (NaN) values, fill with mean, median, or a constant value. Note that you must remove NaN values if they are in your data file before you generate a model.

1. Select your preprocessing option values, then select Gernerate model > OK. <br>
   The model formula graph appears with the description box.
2. Select the description box and write a description. <br>
![image](https://github.com/user-attachments/assets/d1aa1ec1-bfaa-4a35-98bd-b36f90196bc9) <br>
   Note: You must write a description in order to save the file.
4. Select Save Model. <br>
   The File explorer dialog appears. 
5. Select Save > OK.

### Predicting values from data files
1. From the formula graph dialog, select Input value.
2. Input a number for the y value, then select Output Prediction. <br>
   The prediction appears below the Input value.
3. Select Save Model to save the prediction.


### Loading saved data files
1. From the main menu, select Load Model <br>
   The File Explorer dialog appears.
2. Select a previously saved file > Open > OK. <br>
   The saved model will appear.


## Contributing to StatWizard

To contribute, please contact the creator of StatWizard through GitHub (Fiz Garrido Escudero). We welcome any contributions to this project. 

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
