# Analogical-LLM
Multi-agent approach based on LangGraph to apply analogical reasoning of LLM to enhance its innovation problem solving

## Setup
Make sure you are using Python 3.11
```
python3 --version
```

### Clone repo
```
git clone https://github.com/maobupa/Analogical-LLM.git

cd Analogical-LLM
```
### Create an environment and install dependencies
```
python3 -m venv analogical-lc-env

source analogical-lc-env/bin/activate

pip install -r requirements.txt
```
### Set up OpenAI API Key (instruction for MacOS only). If you don't have one, can sign up [here](https://openai.com/index/openai-api/)

In terminal, open the shell configuration file using the command: 
```
nano ~/.zshrc
```
(If you're using bash instead of zsh, use ~/.bashrc instead.)

go to the bottom and add this: 
```
export OPENAI_API_KEY="your_openai_api_key"
```
Press Control + X to save and exit

apply the changes:
```
source ~/.zshrc
```
Test if the API Key is set up successfully
```
echo $OPENAI_API_KEY 
```
should print out the key 

### Open jupyter notebook to run the Prototype.ipynb file
```
jupyter notebook 
```
