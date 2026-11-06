\# EPFO FAQ Management System



A Python-based command-line application that stores, searches, and manages frequently asked questions (FAQs) related to the Employees' Provident Fund Organisation (EPFO).



This project was developed as part of an assignment covering data collection, Python programming, modular code organization, and command-line operations.



\## Project Overview



The application contains the first 20 FAQs from the \*\*Claim \& withdrawals\*\* category of the official EPFO FAQ website.



Each FAQ is stored as a Python dictionary with the following fields:



\- `faq\_number` – Unique FAQ number.

\- `category` – FAQ category.

\- `question` – FAQ question.

\- `answer` – Official FAQ answer.

\- `related\_form` – Related EPF forms, if mentioned.

\- `source\_url` – Source webpage URL.



\## Features



\- Stores 20 EPFO FAQ records.

\- Displays all FAQ records.

\- Searches FAQs using keywords.

\- Counts records by category.

\- Retrieves an individual FAQ using its ID.

\- Supports counting by different fields through the records module.

\- Uses modular Python code for better organization.

\- Provides a command-line interface (CLI).



\## Project Structure



```text

EPFO\_FAQ\_Project/

│

├── app/

│   ├── \_\_init\_\_.py

│   ├── records.py

│   └── cli.py

│

├── data/

│   └── sample\_records.py

│

├── main.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Technologies Used



\- Python 3

\- Git

\- GitHub

\- PowerShell

\- Python Standard Library



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/Vaibhav12312/Genrative-Ai-Agentic-Ai-.git

```



\### 2. Navigate to the project folder



```bash

cd Genrative-Ai-Agentic-Ai-/EPFO\_FAQ\_Project

```



\### 3. Create a virtual environment



```bash

python -m venv .venv

```



\### 4. Activate the virtual environment



\*\*Windows PowerShell:\*\*



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 5. Install dependencies



```bash

pip install -r requirements.txt

```



No external Python packages are currently required.



\## How to Run



Run the following commands from the `EPFO\_FAQ\_Project` directory.



\### Display all FAQs



```bash

python -m app.cli list

```



\### Search FAQs by keyword



```bash

python -m app.cli search "withdrawal"

```



\### Count FAQs by category



```bash

python -m app.cli count

```



\### Retrieve an FAQ by ID



```bash

python -m app.cli get 1

```



\## Application Modules



\### `data/sample\_records.py`



Contains the 20 FAQ records stored as a list of dictionaries.



\### `app/records.py`



Contains the core functions:



\- `load\_records()` – Loads FAQ records.

\- `search()` – Searches FAQ records by keyword.

\- `count\_by()` – Counts records by a selected field.

\- `get\_by\_id()` – Retrieves a record using its FAQ number.



\### `app/cli.py`



Provides command-line access to the FAQ management functions.



\### `main.py`



Main project entry point.



\## Data Source



Official EPFO FAQ website:



https://www.epfo.gov.in/faq-epfo/



\*\*Category:\*\* Claim \& withdrawals



\*\*Number of records:\*\* 20



The FAQ content is provided for educational and informational purposes. Please refer to the official EPFO website for the latest information and applicable rules.



\## Author



\*\*Vaibhav Pavse\*\*



GitHub: https://github.com/Vaibhav12312



\## License



This project is created for educational and learning purposes.

