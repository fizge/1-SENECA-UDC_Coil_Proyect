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
- Teams: This tool was used to collaborate using video conferencing and discussing each sprint with the product owner.
- Taiga: This tool was used for agile project management and for keeping track and organizing sprints.

## Agile Development Process
This project was created using the agile development methodologies. Agile is a software development method that is used to minimize risks and increase cross team collaboration. The key factors of agile development are its flexibility to changes through an iterative process, collaboration with product owners, and the use of user stories that lead each sprint. <br>

During the cycle, each sprint lasted one week, with the exception of sprint 8 which was 2 weeks. At the end of each sprint, the developers and technical writers met with the product owner to discuss what aspects of the project were going well, what parts were not going well and how the next sprint could be improved. After each sprint retrospective, the developers and technical writers met to discuss their progress, goals, and achievements. <br>

**Completed Sprints and Sprint Tasks**
1. Sprint 1: Both teams created Taiga, GitHub, code repository, and documentation plan.
2. Sprint 2: The documentation team conducted a subject matter expert (SME) interview with the developers and completed the first half of the documentation plan. The developers researched Python libraries.
3.  Sprint 3: The documentation team worked on completing the second half of the documentation plan. The developers further researched Python libraries (tkinter, PyQt, and wxpython).
4.  Sprint 4: The documentation team worked on creating the preliminary README and GitHub document. The developer team worked on creating linear models for prediction using the GUI, and improving the graphical interface.
5.  Sprint 5: The developers worked on creating file selection and saving features. The documentation team worked on revising the README and GitHub document.
6.  Spring 6: The developers further worked on the file selection, saving features and creating a polished user interface for Trackr. The documentation team worked on revising the README by including Trackr user interface images.
7.  Sprint 7: The developers worked on improving the user interface, incorporating making predictions using an uploaded model, and recovering previously saved models. The documentation team worked on revising the README to include these new features.
8.  Sprint 8: The documentation team worked on completing the GitHub documentation and README. The developers worked on revising the user interface to make it more user friendly.

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

