# Trackr Internal Documentation
This documentation provides essential background information for the Trackr project team, covering all foundational details about the
Trackr software and its users. The purpose of this resource is to keep team members informed of the context that guides the project, and provide new team members background information on project goals, platforms used, the users, and methodology.

## Project Background
This project was created by four student developers in the Universidade da Coruna and two technical writers in Seneca Polytechnic working together as part of a Collaborative Online Learning Project (COIL) for a semester using an agile development process.<br>
The purpose of Trackr is to predict data from data sets. The data sets that are input into the application must be database, excel, pickle, or comma-seperated value files. The output datasets can be saved and uploaded only as pickle files. 

### Goals
The goal of the project was to create an application that gives the users a simple visual interface of linear regression models from data stores in the mentioned files, and allows users to make predictions with them. The users can use the application to: <br>
- Save data models
- Load data models
- Make predictions using loaded data models

### Audience
The intended audience of Trackr are small to medium-scale business owners with low to average technical expertise who want to gain data-based insights that can inform their decisions.  Trackr can be of use to make other industry-specific predictions from users of different professions, such as e-commerce and education.
[User Persona graphic to be added] 

### Platforms and Technology 
Trackr was created using a vartiety of tools and platforms to create a simple and user-friendly application. <br>
The development platforms used were: <br>

**Python**
- Python was used as the programming language because of the large ammount of libraries that can be used alongside the language. The libraries used were pandas for data analysis and manipulation, tkinter for creating the GUI, and joblib for saving and loading large datasets.

**Data File Formats**
The datasets that were used to create Trackr were:
- Database files (.db)
- Excel files (.xls)
- Pickle files (.pkl)
- CSV files (.csv)

 **Collaboration Tools**
The teams collaborated using:
- WhatsApp: This tool was used to contact team members throughout the project.
- GitHub: This tool was used to store code files and documentation.
- Visual Studio Code: This tool was used by the programmers to create the project.
- Zoom: This tool was used to collaborate using video conferencing.

## What is AI? 
Artificial Intelligence (AI) is a technology that enables computers and machines to stimulate human abilities, comprehension, problem solving, and even creativity. AI systems can analyze large amounts of data to recognize patterns and adapt over time, constantly learning and adapting from new data.

## What is Linear Regression? 
Linear regression is a method in data science and machine learning that helps predict future outcomes by finding a straight-line relationship between two variables. The independent variable is the known data, and the dependent variable is what we want to predict. This method can be used to make informed guesses about things like sales, age, housing prices, and product costs. 

### The Linear Regression Model

In simple linear regression, a line is formed based on the data points of the independent and dependent variables. The line consists of two parts:
* A slope - Displays how the dependent variable changes each time there is a change in the independent variable.
* Intercept -This is the predicted value of the dependent variable when the independent variable is zero.

The purpose of this line is to make future predictions by showing a clear, straightforward relationship between
the two variables given the data.

### How does Trackr use Linear Regression and AI? 
Trackr allows users to effortlessly create and work with linear regression models, helping businesses predict profits using past data. By uploading an existing spreadsheet to Trackr, users can quickly generate a linear regression model, while AI enhances the results by delivering actionable insights. This process requires minimal effort and no advanced technical knowledge, making data-driven predictions accessible to everyone.

