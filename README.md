# DocQmint

DocQmint is a document query and language model interaction tool with an intuitive graphical interface built in Python. Users can upload and index documents, query them using large language models (LLMs) like Groq and OpenAI, and securely manage API keys. This tool is designed for efficient document retrieval and chat-based interaction with indexed data, making it ideal for research, customer support, and information management.

App look:

![Main APP](https://github.com/user-attachments/assets/ac85f4e7-f8d2-4b0a-b18b-afdf6e22119f)

App Indexing:

![indexed](https://github.com/user-attachments/assets/60cac3bf-f5a4-4956-92bf-bb3b71a6cff5)

App Response:

![Response](https://github.com/user-attachments/assets/e51dab03-1c7f-41e4-87c1-51437d647c6e)

---

## Features

- **Document Upload and Indexing**: Upload documents from a folder, automatically indexing them for fast retrieval.
- **Multi-Provider LLM Querying**: Choose between Groq and OpenAI for querying indexed documents.
- **Secure API Key Management**: Easily add, delete, or update API keys with an admin-protected settings menu.
- **Graphical Interface**: Intuitive GUI built with Tkinter for smooth navigation and interaction.
- **Document Context Search**: Retrieve documents relevant to your query, with responses from the selected language model.
- **Document Indexing**: DocQmint employs OpenAI's API for indexing, with an approximate cost of $0.01 per folder of documents.
- **Language Model Interaction**: The tool utilizes Groq's LLMs for querying and interacting with the indexed data, benefiting from Groq's rapid inference speeds.
- **API Key Management**: Users can securely manage their OpenAI and Groq API keys within the application. [Default password is: admin ]
- **Use Cases**: DocQmint is ideal for research, customer support, and information management, offering efficient document retrieval (RAG) and chat-based interaction with indexed data.

---

## Requirements

Before you install and run DocQmint, ensure you have the following dependencies:

- **Python 3.8 or later**
- `pip` (Python package installer)

**Python Packages**: Listed in `requirements.txt`, including:
- `tkinter` (for GUI components)
- `requests` (for API requests)
- `numpy`, `faiss-cpu` (for document indexing and similarity search)
- `python-dotenv` (for environment variable management)
- `langchain_community`, `langchain_openai` (for document loading and language model interaction)

---

## Installation

### 1. Clone the Repository

```bash
Change the name of example.env file to .env and edit the file by adding your Groq API key and your OpenAI API key

git clone https://github.com/ttgrex1/DocQmint.git
cd DocQmint
2. Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to keep your dependencies isolated:
bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

3. Install the Required Packages
Install the necessary packages listed in requirements.txt:

bash
pip install -r requirements.txt

## Configuration
API Keys and Environment Variables
DocQmint requires API keys for interacting with the Groq and OpenAI models, along with an admin password for API key management. These values should be stored in a .env file in the root directory of the project for security.

Create a .env file in the root directory.

Add the following keys, replacing the placeholder values with your actual API keys and desired admin password:
[plaintext]
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
ADMIN_PASSWORD=your_admin_password # This will be a made up password by you
Save the .env file.

Usage
Running the Application
To launch DocQmint, run the following command:

bash
python main.py
This opens the main application window.

## Navigating the Interface
Selecting a Document Folder:

Click the "Choose Folder" button to select a folder containing documents (PDF, txt, word, csv or other supported formats). DocQmint will automatically index these documents.
Choosing a Provider:

### In the top menu, choose between Groq and OpenAI to select the language model provider for querying. The models for each provider can be selected from a dropdown menu.
Settings (API Key Management):

### Navigate to Settings > API Keys to view, add, or delete API keys.
Admin access is required to make changes. Enter the admin password to enable API key management.
Starting a Query:

Type your query in the input box at the bottom of the screen.
Click Send or press Enter to query the indexed documents. The language model will respond based on the content of your documents.
Viewing About Information:

Under the About menu, view information about the current version of DocQmint and the author.

## Capabilities
DocQmint’s core features allow it to function as a powerful document search and LLM interaction tool. Here’s a breakdown of its key capabilities:

Document Indexing: Index documents in a folder, allowing for quick retrieval and relevance-based search. The app uses FAISS to create embeddings and perform similarity searches.
Contextual Responses: The app sends user queries along with document contexts to the selected language model, enhancing the relevance of responses.
API Key Management: Easily add, delete, or update API keys for different providers. The settings are admin-protected, ensuring only authorized users can manage API keys.
Multi-Provider LLM Support: Switch between Groq and OpenAI models for document-based queries, with options to select specific models for each provider.
Troubleshooting
Environment Variables Not Loaded:

Make sure your .env file is in the project root directory, formatted as shown above, and contains valid API keys.
Ensure .env is listed in .gitignore to keep it secure.
Missing Python Packages:

Run pip install -r requirements.txt to install all required packages.
If there are issues with specific packages, try installing them individually (e.g., pip install faiss-cpu).
Issues with API Key Management:

If you cannot save or retrieve API keys, verify that you have admin access and the correct password.
By following this guide, users can install, configure, and run DocQmint, taking full advantage of its document retrieval and LLM interaction capabilities. For additional questions, please reach out via the repository’s Issues tab!
