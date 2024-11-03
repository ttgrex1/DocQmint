# gui/app.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from gui.api_keys_window import APIKeysWindow
from gui.about_window import AboutWindow
from services.indexing import DocumentIndexer
from services.querying import LLMQueryService
from utils.env_manager import load_environment, get_env_variable

class LLMChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("DocQmint")
        self.master.geometry("1200x700+20+20")  # Set the window size to 800x600
        self.master.configure(bg='black')

        # Load environment variables
        env = load_environment()
        self.groq_api_key = env['GROQ_API_KEY']
        self.openai_api_key = env['OPENAI_API_KEY']
        self.admin_password = env['ADMIN_PASSWORD']
        self.master_password = 'docQmint2024'

        # Menu bar with 'Settings' and 'About'
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="API Keys", command=self.open_api_key_window)
        
        # Add About menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="About", command=self.open_about_window)

        # Frame for provider selection
        provider_frame = tk.Frame(self.master, bg='black')
        provider_frame.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

        self.provider_var = tk.StringVar(value='Groq')  # Default provider
        self.provider_var.trace('w', self.update_model_dropdown)

        groq_radio = tk.Radiobutton(provider_frame, text="Groq", variable=self.provider_var, value='Groq', bg='black', fg='white', selectcolor='black')
        groq_radio.pack(side=tk.LEFT)

        openai_radio = tk.Radiobutton(provider_frame, text="OpenAI", variable=self.provider_var, value='OpenAI', bg='black', fg='white', selectcolor='black')
        openai_radio.pack(side=tk.LEFT)

        # Model selection dropdown
        self.model_var = tk.StringVar(self.master)
        self.groq_models = ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "llama-3.2-90b-text-preview", "mixtral-8x7b-32768"]
        self.openai_models = ["gpt-4o-mini", "gpt-3.5-turbo"]
        self.model_var.set(self.groq_models[0])  # default value
        self.dropdown = tk.OptionMenu(self.master, self.model_var, *self.groq_models)
        self.dropdown.config(bg='darkgrey', fg='black', width=20)
        self.dropdown.pack(pady=10)

        # Reset chat button
        self.reset_button = tk.Button(self.master, text="Reset Chat", command=self.reset_chat, bg='darkgrey', fg='red')
        self.reset_button.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

        # Text box for conversation history
        self.conversation_box = ScrolledText(self.master, wrap=tk.WORD, bg='black', fg='white', font=('Arial', 12))
        self.conversation_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Configure tags for user and assistant messages
        self.conversation_box.tag_config('user', foreground='cyan')  # Set User text color
        self.conversation_box.tag_config('assistant', foreground='white')  # Set Assistant text color
        self.conversation_box.tag_config('source', foreground='Orange')  # Set Source text color to blue
        self.conversation_box.tag_config('source_label', foreground='Orange', font=('Arial', 12, 'bold'))

        # Choose Folder button
        self.folder_button = tk.Button(self.master, text="Choose Folder", command=self.choose_folder, bg='darkgrey', fg='black')
        self.folder_button.pack(pady=10)

        # Frame for input box and send button
        input_frame = tk.Frame(self.master, bg='black')
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        # Multi-line text entry for user input (2-3 sentences high)
        self.user_input = tk.Text(input_frame, font=('Arial', 12), bg='grey', fg='black', height=3, wrap=tk.WORD)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Bind the Return key to the send_input function
        self.user_input.bind("<Return>", self.send_input)

        # Send button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_input, bg='darkgrey', fg='green', state='disabled')
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Initialize components
        self.indexer = DocumentIndexer()
        self.vector_store = None
        self.current_folder = None
        self.messages = []

        # Placeholder for query service; will be initialized after indexing
        self.query_service = None

    def open_api_key_window(self):
        api_key_window = tk.Toplevel(self.master)
        api_keys_window = APIKeysWindow(
            api_key_window,
            groq_api_key_var=tk.StringVar(value='********'),
            openai_api_key_var=tk.StringVar(value='********'),
            admin_password=self.admin_password,
            on_save_callback=self.refresh_api_keys
        )

    def refresh_api_keys(self):
        # Reload API keys from environment
        self.groq_api_key = get_env_variable('GROQ_API_KEY', '')
        self.openai_api_key = get_env_variable('OPENAI_API_KEY', '')

    def open_about_window(self):
        AboutWindow(self.master)

    def update_model_dropdown(self, *args):
        provider = self.provider_var.get()
        menu = self.dropdown['menu']
        menu.delete(0, 'end')

        if provider == 'Groq':
            models = self.groq_models
        else:
            models = self.openai_models

        for model in models:
            menu.add_command(label=model, command=lambda value=model: self.model_var.set(value))

        # Set default model
        if models:
            self.model_var.set(models[0])
        else:
            self.model_var.set('')

    def send_input(self, event=None):
        user_text = self.user_input.get("1.0", tk.END).strip()  # Get text from Text widget
        if user_text:
            if self.vector_store is None:
                self.update_conversation("Please choose a folder first.")
                return "break"
            self.update_conversation("User: " + user_text, 'user')
            response, sources = self.query_service.query_documents_and_llm(user_text)
            self.update_conversation(f"Assistant: {response}", 'assistant')
            self.update_sources(sources)
            self.user_input.delete("1.0", tk.END)  # Clear the Text widget after sending
        return "break"  # Prevent default <Return> behavior (new line)

    def update_conversation(self, text, tag='assistant'):
        self.conversation_box.insert(tk.END, text + '\n', tag)
        self.conversation_box.yview(tk.END)

    def update_sources(self, sources):
        self.conversation_box.insert(tk.END, "Sources:\n", 'source_label')
        for i, source in enumerate(sources):
            source_basename = os.path.basename(source)
            tag_name = f"source_{i}"
            self.conversation_box.insert(tk.END, f"{i+1}. {source_basename}\n", tag_name)
            self.conversation_box.tag_config(tag_name, foreground='green', underline=1)
            # Bind the tag to the callback function
            self.conversation_box.tag_bind(tag_name, "<Button-1>", lambda event, s=source: self.open_source_file(s))

    def open_source_file(self, source):
        try:
            if os.path.exists(source):
                if os.name == 'nt':
                    os.startfile(source)
                elif os.name == 'posix':
                    if sys.platform == 'darwin':
                        subprocess.call(['open', source])
                    else:
                        subprocess.call(['xdg-open', source])
            else:
                messagebox.showerror("Error", f"File not found: {source}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def reset_chat(self):
        self.conversation_box.delete('1.0', tk.END)
        self.messages = []

    def choose_folder(self):
        new_folder = filedialog.askdirectory()
        if new_folder:
            if self.current_folder != new_folder:
                self.current_folder = new_folder
                index_folder = os.path.join(new_folder, 'faiss_index')
                if os.path.exists(index_folder):
                    try:
                        self.indexer.load_vector_store(index_folder)
                        self.vector_store = self.indexer.vector_store
                        self.send_button.config(state=tk.NORMAL)
                        self.update_conversation("Vector store loaded successfully.")
                    except Exception as e:
                        self.update_conversation(f"Error loading vector store: {e}")
                else:
                    try:
                        self.indexer.index_documents(new_folder)
                        self.vector_store = self.indexer.vector_store
                        self.send_button.config(state=tk.NORMAL)
                        self.update_conversation("Documents have been indexed successfully.")
                    except Exception as e:
                        self.update_conversation(f"Error indexing documents: {e}")

                # Initialize the query service
                self.query_service = LLMQueryService(
                    vector_store=self.vector_store,
                    groq_api_key=self.groq_api_key,
                    openai_api_key=self.openai_api_key,
                    model_var=self.model_var,
                    provider_var=self.provider_var
                )
