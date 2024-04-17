import os
import sys
import shutil

sys.path.insert(0, '../bugscpp')
from command import CommandList

class BugscppInterface():
    def __init__(self, project, bug_index):
        self._commands = CommandList()
        self._project = project
        self._bug_index = bug_index
        self._path_to_repo = f'benchmark/{self._project}/buggy-{self._bug_index}'
        self._prepare_test_output_directory()
        self._output_dir
    
    def __str__(self):
        return f'{self._project}-{self._bug_index}'
        
    def _prepare_test_output_directory(self):
        # os.getcwd: current directory where the cursor is located
        self._output_dir = os.path.join(os.getcwd(), f'benchmark/{self._project}-{self._bug_index}')
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
    
    def _clear_test_output_directory(self):
        try:
            for file_name in os.listdir(self._output_dir):
                file_path = os.path.join(self._output_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"An error occurred while clearing test output: {e}")

    def checkout(self):
        checkout_args = [self._project, self._bug_index, '--buggy', '--target=benchmark']
        self._commands['checkout'](checkout_args)
    
    def build(self):
        build_args = [self._path_to_repo, '--coverage']
        self._commands['build'](build_args)

    def test(self):
        self._clear_test_output_directory()
        test_args = [self._path_to_repo, '--broken-cases', f'--output-dir={self._output_dir}', '--coverage']
        self._commands['test'](test_args)
    
    def check_sanitizer_output(self):
        if os.path.exists(self._output_dir):
            sub_dirs = os.listdir(self._output_dir)
            for sub_dir in sub_dirs:
                bugnum = sub_dir.split('-')[-1]
                output_path = os.path.join(self._output_dir, sub_dir)
                output_file = os.path.join(output_path, bugnum+'.output')

                if os.path.exists(output_file):
                    with open(output_file, 'r') as of:
                        content = of.readlines()

                        if 'AddressSanitizer' in ' '.join(content):
                            print(f"{self._project}-buggy-{self._bug_index}-{bugnum} has sanitizer results")
                        else:
                            print(f"{self._project}-buggy-{self._bug_index}-{bugnum} doesn't have sanitizer results")
                            self.remove_proj(output_path, output_file)
        else:
            print(f"{self._output_dir} doesn't exist")
    
    def remove_proj(self, output_path, output_file):
        shutil.rmtree(output_path)
        sub_dirs_output = os.listdir(self._output_dir)
        if not sub_dirs_output:
            shutil.rmtree(self._output_dir)
            shutil.rmtree(self._path_to_repo)
        sub_dirs_repo = os.listdir(f'benchmark/{self._project}')
        if len(sub_dirs_repo) == 1 and sub_dirs_repo[0] == ".repo":
            shutil.rmtree(f'benchmark/{self._project}')
    

if __name__ == "__main__":
    projects_list = './projects_with_sanitizer_option.txt'

    with open(projects_list, 'r') as lf:
        for l in lf:
            bugname, start_num, end_num = l.split()
            for i in range(int(start_num), int(end_num)+1):
                bugscpp = BugscppInterface(bugname, str(i))
                bugscpp.checkout()
                bugscpp.build()
                bugscpp.test()

                bugscpp.check_sanitizer_output()





