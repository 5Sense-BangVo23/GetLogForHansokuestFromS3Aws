# GetLogForHansokuestFromS3Aws


### python3 -m venv venv

### source venv/bin/activate 

### Or:  deactivate

### python3 < the_file >


### export PYENV_VERSION=$(cat .env | grep PYENV_VERSION | cut -d '=' -f2)
### direnv allow .


rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt