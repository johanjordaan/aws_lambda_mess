import os
import shutil
from zipfile import ZipFile
from configparser import ConfigParser

CONFIG_FILE = ".aws_lambda_mess"
REQUIREMENTS_FILE = "requirements.txt"
GITIGNORE_FILE = ".gitignore"
APP_FILE = "app.py"

def new(dirname):
    print('Running new', dirname)

    if os.path.isdir(dirname):
        print(f"[{dirname}] already exists.")
        exit(1)

    os.mkdir(dirname)
    os.chdir(dirname)
    try:
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', CONFIG_FILE), CONFIG_FILE)
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', REQUIREMENTS_FILE), REQUIREMENTS_FILE)
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', GITIGNORE_FILE), GITIGNORE_FILE)
        os.mkdir("src")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', APP_FILE), os.path.join("src", APP_FILE))
        os.mkdir("package")
        os.mkdir("dist")
        os.mkdir("tests")
    except Exception as e:
        print(e)
        os.chdir("..")
        exit(1)


    #framework_dir = os.path.join(os.path.dirname(__file__), "framework")
    #files = [file_name for file_name in os.listdir(framework_dir) if file_name not in ["__pycache__"]]
    #for file in files:
    #    print(f"{os.path.join(framework_dir,file)}")

def build():
    if not os.path.isfile(CONFIG_FILE):
        print("Project not initialised. Please run init")
        exit(1)

    def get_all_file_paths(directory, exclusion_patterns):
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                include = True
                for exclusion_pattern in exclusion_patterns:
                    if exclusion_pattern in filepath:
                        include = False
                if include:
                    file_paths.append(filepath)
        return file_paths

    cfg = ConfigParser()
    cfg.read(CONFIG_FILE)
    print(cfg.get('main','source'))

    exclusion_patterns = ["__pycache__"]
    file_paths = get_all_file_paths("./package", exclusion_patterns) + get_all_file_paths("./aws_lambda_mess", exclusion_patterns)

    print('Running build', __file__ )
    if not os.path.isdir("./build"):
        os.mkdir("./build")
    if not os.path.isdir("./build/aws_lambda_mess"):
        os.mkdir("./build/aws_lambda_mess")

    with ZipFile('dist/package.zip', 'w') as zip:
        for file in file_paths:
            print(file)
            zip.write(file)



def run():
    import argparse

    parser = argparse.ArgumentParser(description="aws lambda mess")
    subparsers = parser.add_subparsers(dest='subparser')

    new_parser = subparsers.add_parser('new')
    new_parser.add_argument('dirname')
    build_parser = subparsers.add_parser('build')

    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)

if __name__ == "__main__":
    run()
