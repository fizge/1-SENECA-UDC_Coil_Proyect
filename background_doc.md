# StatWizard Internal Documentation
This documentation provides essential background information for the StatWizard project team, covering all foundational details about the
StatWizard software and its users. The purpose of this resource is to keep team members informed of the context that guides the project, and provide new team members background information on project goals, platforms used, the users, and methodology.

## Project Background
This project was created by four student developers in the Universidade da Coruna and two technical writers in Seneca Polytechnic working together as part of a Collaborative Online Learning Project (COIL) for a semester using an agile development process. This project leverages international perspectives to create a universal tool to deliver an accessible, user-friendly solution for data analytics.<br>

The purpose of StatWizard is to predict data from data sets. The data sets that are input into the application must be database, excel, pickle, or comma-separated value files. The output datasets can be saved and uploaded only as pickle files. 


### Goals
The goal of the project was to create an application that gives users a simple visual interface of linear regression models from data sets and allows users to make predictions. The users can use the application to: <br>
- Save data models
- Upload data models stored on their device
- Make predictions using data models

### Audience
The intended audience of StatWizard are small to medium-scale business owners with low to average technical expertise who want to gain data-based insights that can inform their decisions. StatWizard can be used to make other industry-specific predictions by users in different professions, such as e-commerce and education.

StatWizard's priority is to create an intuitive tool that simplifies data processing, allowing users to quickly gain actionable insights. By focusing on accessibility and ease of use, we aim to empower our audience with the confidence to use data analytics without requiring advanced technical skills or training. While our example below is an example of a target user, always consider the diverse technical backgrounds of users and prioritize features that streamline processes, minimize confusion, and provide clear, impactful insights.

<details>
<summary>View StatWizard’s Target User</summary>

This chart shows the traits, motivations, and pain points of StatWizard's target user:

| User Trait | Description |
| --- | --- |
| Age | 20 + |
| Occupation | Small to medium-scale business owners. |
| Technical Skill Level |  StatWizard users have varying levels of technical expertise, ranging from beginners unfamiliar with data analysis tools to more experienced users seeking a straightforward way to predict profits and make data-driven decisions. |
| Motivations | Our users want to gain more insights about analytics such as saving costs, how to increase yearly profits, etc. |
| Pain Points | Lack of time for self-learning. Long, complex instructions with technical jargon, lack of experience and knowledge of statistics and data analytics, and having to consult multiple external sources to further understand how to use data analytic tools. |
| Expectations | Empathetic and concise instructions that are labelled,  the user’s existing data should be fully compatible with StatWizard’s upload feature. They expect to understand how to use correct input that will result in helpful and informative output results to support their goals. |

</details>

### Platforms and Technology 
StatWizard was created using a variety of tools and platforms to create a simple and user-friendly application. <br>
The development platforms used were:<br>

**Python**<br>
Python was used as the programming language because of the large amount of libraries that can be used alongside the language. The libraries used were pandas for data analysis and manipulation, tkinter for creating the GUI, and joblib for saving and loading large datasets.

**Data File Formats**<br>
The dataset formats that were used to create StatWizard were:
- Database files (.db)
- Excel files (.xls)
- Pickle files (.pkl)
- CSV files (.csv)
  **Note:** StatWizard can only be used with these data file formats.

 **Collaboration Tools**<br>
The development and documentation teams collaborated using:
- [WhatsApp](https://web.whatsapp.com/): This tool was used to contact team members throughout the project.
- [GitHub](https://github.com/): This tool was used to store code files and documentation.
- [Visual Studio Code](https://code.visualstudio.com/): This tool was used by the programmers to create the project.
- [Zoom](https://www.zoom.com/): This tool was used to collaborate using video conferencing.
- [Microsoft Teams](https://www.microsoft.com/en-ca/microsoft-teams/group-chat-software): This tool was used to collaborate using video conferencing and discuss sprints with the product owner.
- [Taiga](https://taiga.io/): This tool was used for agile project management, and for keeping track of sprints and organizing tasks.

## Agile Development Process
StatWizard was created using agile development methodologies. Agile is a software development method that is used to minimize risks and increase cross-team collaboration. The key factors of agile development are its flexibility to change through an iterative process, collaboration with product owners, and the use of user stories that lead each sprint.<br>

During the cycle, each sprint lasted one week, with the exception of sprint 8 which was 2 weeks long. At the end of each sprint, the developers and technical writers met with the product owner to discuss what aspects of the project were going well, what parts were not going well, and how the next sprint could be improved. After each sprint retrospective, the developers and technical writers met to discuss their progress, goals, and achievements. <br>

**Completed Sprints and Sprint Tasks**
1. Sprint 1: Both teams created Taiga accounts, GitHub accounts, and the code and documentation repository on GitHub. The documentation team began the Documentation Plan.
2. Sprint 2: The documentation team conducted a subject matter expert (SME) interview with the developers and completed the first half of the Documentation Plan. The developers researched Python libraries.
3.  Sprint 3: The documentation team worked on completing the second half of the Documentation Plan. The developers further researched Python libraries (tkinter, PyQt, and wxpython). 
4.  Sprint 4: The documentation team worked on creating the preliminary README and GitHub document. The developer team worked on creating linear models for prediction using the GUI, and improving StatWizard's graphical interface.
5.  Sprint 5: The developers worked on creating file selection and saving features. The documentation team worked on revising the README and GitHub document.
6.  Sprint 6: The developers further worked on the file selection feature, saving features, and creating a polished user interface for StatWizard. The documentation team worked on revising the README by including StatWizard user interface images.
7.  Sprint 7: The developers worked on improving the user interface, incorporating making predictions using an uploaded model, and recovering previously saved models. The documentation team worked on revising the README to include these new features.
8.  Sprint 8: The documentation team worked on completing the GitHub documentation and README. The developers worked on revising the user interface to make it user friendly.

## AI, Machine Learning, and Linear Regression
Understanding these concepts is integral to understanding how StatWizard functions. 

### Artificial Intelligence (AI) and Machine Learning (ML)
**Machine Learning (ML)** is a subset of **Artificial Intelligence (AI)**, but it is not necessarily the same. AI is a technology that enables computers and machines to stimulate human abilities, comprehension, problem solving. AI can analyze large amounts of data to recognize patterns and adapt over time, constantly learning and adapting from new data that it is given.

While StatWizard’s processes rely on data to improve its output, it does not use AI explicitly. Instead, Machine Learning works by analyzing input data to identify patterns and make predictions. StatWizard relies on these processes to improve its output by building models that predict outcomes based on the datasets it processes. It uses ML techniques to create accurate and reliable predictions tailored to user data.



### Linear Regression
Linear regression is a type of machine-learning algorithm that helps predict future outcomes by finding a straight-line relationship between two variables. The independent variable is the known data, and the dependent variable is what we want to predict. This method can be used to make informed guesses about variables such as sales, age, housing prices, and product costs. StatWizard uses Simple Linear Regression, which means that the model will produce the relationship between 1 independent variable (known data) and 1 dependent variable (the value to predict).

**Features of the Linear Regression Model**

In simple linear regression, a line is formed based on the data points of the independent and dependent variables. The line consists of two parts:
* **A slope** - Displays how the dependent variable changes each time there is a change in the independent variable, specifically for every unit increase in the independent variable. It shows the strength and direction of the relationship between the two variables.
+ **Intercept** - The value of the dependent variable when the independent variable equals zero. It represents the starting point or baseline value in the absence of any effect from the independent variable.
* **Line of best fit/ Regression line** - This line minimizes the error between the predicted and actual values, ensuring the smallest possible difference across all data points. It represents the relationship between the dependent and independent variables. 

The purpose of this line is to make future predictions by showing a clear, straightforward relationship between
the two variables given the data.

### How does StatWizard use Linear Regression and Machine Learning? 
StatWizard allows users to effortlessly create and work with linear regression models, helping businesses predict profits using past data. By uploading an existing spreadsheet to StatWizard, users can quickly generate a linear regression model, while AI enhances the results by delivering actionable insights. This process requires minimal effort and no advanced technical knowledge, making data-driven predictions accessible to everyone.

## Project Specific Information
This section explains who StatWizard was created by, their role in the project, and the role of the documentation team. <br>

**Developer Team** <br>
- Fiz Garrido: Lead developer.
- Manuel Conde: Developer.
- Yeyi Zheng: Developer.
- Pablo Diaz: Developer.

**Documentation Team** <br>
Both writers worked each sprint to develop clear, accurate, end-user and internal user documentation. The goal of the documentation team was to create clear, accurate, concise documentation tailored to both end user needs and developer needs. This meant ensuring that the user's needs were considered when creating both the README and GitHub documentation. The end user needs were to understand how to use StatWizard easily, without having a technical background. The developer needs were to understand StatWizard requirements, how to set up the correct environment to recreate the tool, and understand how the tool was created. <br>

The documentation team delivers documents that refer to the [Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) and follow [Github's Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

The documentation team members are:

- Cristine Buizon: Writer of the GitHub documentation (Introduction, Project Background, AI, Machine Learning, and Linear Regression) and the README.
- Hasti Noushabadi: Writer of the GitHub documentation (Project Background, Agile Development Process, and Project Specific Information) and the and README.
