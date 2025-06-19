How to run:

1.Create a virtualenv:: python3 -m venv env

2.Activate virtualenv:: source env/bin/activate (on linux)
                        env\Scripts\activate (on windows)

3.Install the dependencies needed to run:: 
    1.pip install -r Requirements.txt 
    2.python -m spacy download en_core_web_sm

4.Run Main.py:: python3 Main.py

5.To create executable file :
pyinstaller --onefile --add-data "D:\\vstate-chatbot\\env\\Lib\\site-packages\\en_core_web_sm\\en_core_web_sm-3.8.0;en_core_web_sm" --add-data "D:\\vstate-chatbot\\env\\Lib\\site-packages\\contractions\\data\\;contractions\\data" --add-data "D:\\vstate-chatbot\\env\\Lib\\site-packages\\autocorrect\\data\\;autocorrect\\data" --add-data "D:\\vstate-chatbot\\KEYFILE.txt;." --add-data "D:\\vstate-chatbot\\Logging_file;." --add-data "D:\\vstate-chatbot\\files\\;files" Main.py 
