
# Contributing Guide

Thank you for your interest in contributing to our project! This document outlines how you can contribute, particularly if you're focusing on **documentation**. Below are the steps for adding content to the `README.md` and **GitHub Pages**.

## Prerequisites

Before you start, ensure you have the following:
- A GitHub account.
- Access to the project's main repository.
- Basic knowledge of Markdown. If you're not familiar with it, check out [this basic Markdown guide](https://www.markdownguide.org/basic-syntax/).
- Access to the appropriate branch where the documentation contribution will be made.

## Steps to contribute to the documentation

### 1. Clone the repository
Before making any changes, clone the repository to your local machine:
```bash
git clone https://github.com/fizge/1-SENECA-UDC_Coil_Proyect.git
cd 1-SENECA-UDC_Coil_Proyect
```

### 2. Create a new branch
All contributions should be made in a new branch. To create one, use the following command:
```bash
git checkout -b your-branch-name
```
Example:
```bash
git checkout -b documentation-user-guide
```

### 3. Add content to the `README.md`
The `README.md` file contains general information about the project. To add or modify any section:

1. Open the `README.md` file in your preferred text editor.
2. Add the necessary information following the style guidelines of the project (e.g., clear section headers, bullet points, etc.).

Example of adding a new section:
```markdown
## How to Use the Application

1. Navigate to the home screen.
2. Upload a CSV, Excel, or SQLite file containing your data.
3. Select the type of regression model you want to generate (simple or multiple).
4. Click on "Generate Model" to view the results and predictions.
```

3. After editing, save the file.

### 4. Update the GitHub Pages
If your contribution involves updating the GitHub Pages:

1. Navigate to the folder that contains the content for the GitHub Pages (typically `/docs` or similar).
2. Edit or add the necessary Markdown files to update the website content.
3. If you're not sure where to add content, consult the team for guidance.

### 5. Commit your changes
Once you've made the changes, commit them with a descriptive message:
```bash
git add .
git commit -m "Updated user guide in README and GitHub Pages"
```

### 6. Push your changes and create a pull request
Push your changes to the remote repository:
```bash
git push origin your-branch-name
```

Then, create a pull request from GitHub, providing a clear description of the changes you made.

---

By following these steps, you'll help maintain a clear and organized process for updating the documentation. If you have any questions or need clarification, feel free to reach out to the team!

Happy documenting!

