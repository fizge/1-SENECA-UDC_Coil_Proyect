# DataPilot Version 1.0

DataPilot uses linear regression models to predict profit values. This tool is designed for retail businesses aiming to:  

- **Increase yearly profit margins**  
- **Identify data trends**  
- **Analyze data to make informed decisions for a business**  

You can use your own data models stored as an Excel (.xls), database (.db), or comma-separated value (.csv) file to generate data predictions by selecting the independent variables (features) and dependent variables (target) to create a prediction model.  

## Getting Started with DataPilot  

Welcome to DataPilot! Before you start using DataPilot and the features designed to simplify data analysis to achieve your business goals, you will need to familiarize yourself with important parts of the interface. This section will help you get started by covering device requirements and introducing DataPilot’s main functions.  

### System Requirements  

DataPilot works on both Mac (macOS) and Windows. The download file varies slightly depending on your operating system, but the interface is the same on both platforms. For detailed device and download requirements, see [Table 1.1](#table-11-system-requirements). 

| Operating System | Requirements                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| **Windows**       | **System**: Windows XP or higher<br>**Processor**: Intel Core i5 or equivalent<br>**Memory**: 6 GB RAM minimum<br>**Storage**: 500 MB of free disk space |
| **Mac**           | **System**: macOS<br>**Processor**: Apple M1 or M2<br>**Memory**: 6 GB RAM minimum<br>**Storage**: 500 MB of free disk space |  

<a id="table-11-system-requirements"></a>
**Table 1.1:** System requirements for Mac and Windows devices.

### Navigating the DataPilot Interfaces  

Once you review if your device is compatible, you can download DataPilot to your desktop and start using all of its data analysis features. DataPilot has three main interfaces, each with its own features:  

1. **Loading a model interface**  
2. **Model generating interface**  
3. **Graph interface**  

#### Loading a Model Interface  

After starting the application, the loading interface appears. Here, you can upload your existing data files or load a past DataPilot model using the **Open File** and **Load Model** buttons(See [Figure 1](#figure-1-loading-interface). To learn more about loading models, see "Opening Data Files".

![image](https://github.com/user-attachments/assets/96f756fd-28fd-42dd-a83d-e0afa58852c9)
<a id="figure-1-loading-interface"></a> 
**Figure 1:** Loading a Model Interface with button features.  

#### Model Generating Interface  

When you upload a data file, additional features appear to help you customize the linear regression model (See [Figure 2](#figure-2-model-generating-interface)). These features include:  

- **Select Input** and **Select Output** dropdowns: Choose variables to plot in your linear regression model.  
- **Confirm Selections** button: Finalize your variable selection.
  
![image](https://github.com/user-attachments/assets/367a3fde-78b2-4ddc-b9bf-5e4a7e423cd0)
<a id="figure-2-model-generating-interface"></a>  
**Figure 2:** Model Generating Interface with button features.  

Confirming your selections make the **Preprocessing Options** drop-down and the **Generate Model** button appear (See [Figure 3](#figure-3-preprocessing-options)). These features allow you to customize your linear regression models by filling empty variables.

![image](https://github.com/user-attachments/assets/80afc017-3c6a-4134-9157-f14f06591bfd)
<a id="figure-3-preprocessing-options"></a>  
**Figure 3:** Preprocessing options and Generate Model buttons.  

#### Graph Interface  

Generating a model loads the graph interface, displaying the linear regression model that features the details you select. In [Figure 4](#figure-4-graph-interface), you can see the key features that allow you to view information about the model, create descriptions and make specific predictions with the **Predict button**. Lastly, you can save your model with the **Save** button.

![image](https://github.com/user-attachments/assets/ff434a7b-9f2b-4e00-b259-3cce0cd9f7bb)
<a id="figure-4-graph-interface"></a>  
**Figure 4:** The Graph Interface with key features and buttons.  

## Using DataPilot  

To use DataPilot, make sure your data file is up to date and all data is correctly defined. You can use DataPilot to process and save data sets, generate models for data analysis and predictions, and reload saved models for continuous analysis and customization. 

### Opening Data Files  

To start using DataPilot, open a data file. DataPilot works with Excel (.xls), Data Base (.db), and Comma Separated Value (.csv) files. 
**Note:** Input refers to independent variables, while output refers to dependent variables.  

**To open a data file:**  

1. Open DataPilot and select **Start > Open File**.  
   *The File Explorer dialog appears.*  
2. Select a compatible file > **Open**.  
   *The data chart appears.*  
3. Select variables for **Select Input** and **Select Output** > **Confirm Selections**.  
   *The Preprocessing options appear.*
   
![image](https://github.com/user-attachments/assets/471d5e6b-3485-4946-b8a0-c02b56705e07) <br>
**Figure 5:** The preprocessing options and 'Generate model' button appear when 'Confirm Selections' is selected

### Processing and Saving Data Files  

You can process each file to remove not a number (NaN) values, fill with the mean, median, or constant value. The mean value is the average value in a dataset, the median is the middle value in a dataset, and the constant value is an unchanging value.
**Note:** You must remove NaN values if they are in your data file before you generate a model.

**To process and save a file:**  

1. Select your preprocessing option values > **OK**.  
2. Select **Generate Model** > **OK**.  
   *The model formula graph appears with the Description field and Model Information.*  
3. Select **Save Model**.  
   *The Save As dialog appears.*  
4. Enter a file name, then select **Save > OK**.  

**Note:** You can change the file path from the dialog box. By default, it will save to your Desktop.

### Predicting Values From Data Files

DataPilot can predict values quickly from your data. Once you process the data model, you can start predicting values using the model formula. This can be particularly useful for predicting sales and identifying data trends.
**Note:** Data files can only be saved as pickle files (.pkl).

**To predict a value:**  

1. From the generated model, enter a number in the prediction field.
   ![image](https://github.com/user-attachments/assets/5beec88f-c587-4688-af02-689f60564164) <br>
   **Figure 6:** The prediction value section, indicating a prediction value field and Predict button.
2. Select **Predict**.  
   *The prediction result text appears.* <br>
   ![image](https://github.com/user-attachments/assets/4b0efd01-b840-4691-8119-35fca3480967) <br>
   **Figure 7:** The prediction value result text appears after the Predict button is selected. <br>
   **Note:** If you do not see this text result, you may need to maximize the DataPilot window to full screen. 
3. Select **Save Model** to save the prediction.  

### Loading Models
If you saved a model onto your desktop, you can load the file and work with the dataset. This is useful for customized data sets you want to retrieve to work on over time.

**To load a model**

1.	From the DataPilot dialog, select **Load Model.**
   *The File Explorer dialog appears.*
2.	Select a previously saved .pkl file 
3.	Select **Open > OK.**
   *The previously generated model appears.*


## Glossary  

### Column  
A column holds the values of each variable from your dataset. For example, a dataset related to a business would feature columns such as “Total Sales,” “Number of Customers,” and “Average Transaction values” from a dataset they upload to DataPilot.  

### Dataset  
A dataset is a collection of data that are organized in rows and columns. They often take the form of Excel, database, or Comma-Separated Value files, for example.  

### Independent and Dependent Variables  
- **Independent Variable**: The input in a linear regression model that is used to predict the output data. In DataPilot, independent variables are data that is known.  
- **Dependent Variable**: The output or predicted result that is dependent on the changes based on the independent variable. In DataPilot, dependent variables are the data that you want to predict.  

### Input and Output  
- **Input**: The input is data you are required to provide for DataPilot to make predictions. The input required in DataPilot is the independent variable.  
- **Output**: The output is the prediction result generated by the model based on your input data.  

### Latitude and Longitude  
- **Latitude**: A coordinate that indicates how far east or west a data point is from the y-axis on a linear regression model graph. In DataPilot, the latitude is your independent variable.  
- **Longitude**: A coordinate that indicates how far north or south a data point is from the y-axis on a linear regression model graph. In DataPilot, the longitude is your dependent variable.  

### Linear Regression Model  
A data analytical model that helps make predictions based on the relationships between an independent and dependent variable.  

### MSE (Mean Squared Error)  
A MSE or Mean Squared Error is a number that indicates how far the results of your linear regression model is from the input data. In DataPilot, you can see the MSE in the Model Information box after generating a model.  

### R2 (R-Squared)  
R2 or R-Squared is a number between 0 and 1 that shows you how close your linear regression model fits your input data. A result closer to 1 means that it is a more accurate prediction. In DataPilot, you can view the R2 in the Model Information box after generating a model.  

### Variable  
Variables are a type of data in your dataset that can change. In DataPilot, you have to choose variables from your uploaded dataset under the Input and Output dropdown lists. This step occurs when you need to confirm your selections.  
  

## Contributing to DataPilot  

Please contact the creators of DataPilot through GitHub to discuss contributions to the application. We welcome any contributions to this project if you discuss them with us first. We have created guidelines for the contribution process below. Carefully look through the steps and contact us if you have questions.  

**Contribution Process**
- Fork the repository, making sure not to override any code in the main branch.  
- Create a new branch for your features or bug fixes.  
- Make the necessary changes, then commit to your branch.  
- Submit a pull request. The creators will be notified and will contact you when the request is confirmed, or if more information is needed before the changes are approved.  

**Reporting Issues**
If you find a bug within DataPilot, please open an issue [**here**](https://github.com/fizge/1-SENECA-UDC_Coil_Proyect/issues/new). The creators will get back to you as soon as possible.  

## Acknowledgments  

DataPilot would not have been possible without the Collaborative Online International Learning program (COIL) conducted between Canada and Spain. The people, communities, and sources that made this project possible are:  

- **Program facilitators**: The suggestions and feedback of the instructors facilitating this program were detrimental to designing and writing for DataPilot. These program facilitators are:  
  - **Amy Briggs**: Program co-ordinator and instructor of the Technical Communications Graduate Certificate Program at Seneca Polytechnic.  
  - **Alberto Jose Alvarellos Gonzalez**: Artificial intelligence professor at the Universidade da Coruna.  

- **Open-Source communities**: The tools, open-source projects, and guidance that significantly inspired the development and writing process for DataPilot are:  
  - [**FlowFuse**](https://github.com/FlowFuse):The readme created by FlowFuse inspired the design of DataPilot’s readme.  
  - [**GitHub Docs Quickstart for writing on GitHub**](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github): The information about writing with markup helped DataPilot writers create and format this readme.  

Thank you for being part of our journey!  

