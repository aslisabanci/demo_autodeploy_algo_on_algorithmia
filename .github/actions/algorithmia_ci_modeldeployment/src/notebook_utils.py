import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def run_notebook(notebook_path, execution_path):
    print("notebook and exec paths:", notebook_path, execution_path)
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600)
        ep.preprocess(
            nb,
            {"metadata": {"path": execution_path}},
        )
    print("done with notebook execution")


"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

class NotebookExecutor:
    def __init__(self, name, base_path, notebook_filename_in, notebook_filename_out, timeout=-1):
        self.name = name
        if base_path.endswith('/') is False:
            base_path = base_path + '/'
        self.base_path = base_path
        self.notebook_filename_in = notebook_filename_in
        self.notebook_filename_out = notebook_filename_out
        self.timeout = timeout

    def run(self):
        print("Running notebook '" + self.name + "'")
        nb = nbformat.read(open(self.base_path + self.notebook_filename_in), as_version=4)
        ep = ExecutePreprocessor(timeout=self.timeout, kernel_name='python3', allow_errors=True)
        try:
            ep.preprocess(nb, {'metadata': {'path': self.base_path}})
        except CellExecutionError:
            msg = 'Error executing the notebook "%s".\n\n' % self.notebook_filename_in
            msg += 'See notebook "%s" for the traceback.' % self.notebook_filename_out
            print(msg)
        # raise
        finally:
            nbformat.write(nb, open(self.base_path + self.notebook_filename_out, mode='wt'))

ne = NotebookExecutor('Test', '/my/path', 'MyBook.ipynb', 'MyBook_out.ipynb')
ne.run()
"""