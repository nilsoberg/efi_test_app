"""
This ExampleReadsApp demonstrates how to use best practices for KBase App
development using the SFA base package.
"""

# This is the SFA base package which provides the Core app class.
from base import Core
import os
import uuid
import zipfile
import time

from shutil import copyfile

#from KBaseReport.KBaseReportClient import KBaseReport
#from KBaseReportClient import KBaseReport
#import KBaseReport


MODULE_DIR = "/kb/module"
TEMPLATES_DIR = os.path.join(MODULE_DIR, "lib/templates")

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))

class NameInOutApp(Core):
    def __init__(self, ctx, config, clients_class=None):
        """
        This is required to instantiate the Core App class with its defaults
        and allows you to pass in more clients as needed.
        """
        super().__init__(ctx, config, clients_class)
        # Here we adjust the instance attributes for our convenience.
        self.report = self.clients.KBaseReport
        # self.shared_folder is defined in the Core App class.
        # TODO Add a self.wsid = a conversion of self.wsname

    def copy_name(self, params: dict):
        """
        This method is where the main computation will occur.
        """
        fname = params['family_name']

        results_dir = os.path.join(self.shared_folder, str(uuid.uuid4()))
        self._mkdir_p(results_dir)
        log("RESULTS_DIR: " + results_dir + "\n")
        text_file = os.path.join(results_dir, 'output.txt')
        log(text_file)

        with open(text_file, 'w') as fh:
            fh.write('Family name: ' + fname + '\n')

        params['output_name'] = fname
        params['output_file'] = text_file
        params['output_file_name'] = 'output.txt'

        # This is the method that generates the HTML report
        return self.generate_template_report(params)

    def generate_template_report(self, params: dict):
        # This path is required to properly use the template.
        results_dir = os.path.join(self.shared_folder, 'reports')
        self._mkdir_p(results_dir)

        output_file = params['output_file']
        file_name = params['output_file_name']
        download_file = os.path.join(results_dir, file_name)

        copyfile(output_file, download_file)

        # Path to the Jinja template. The template can be adjusted to change
        # the report.
        template_path = os.path.join(TEMPLATES_DIR, 'report.html')
        # The keys in this dictionary will be available as variables in the
        # Jinja template. With the current configuration of the template
        # engine, HTML output is allowed.
        template_variables = dict(
            output_name = params['output_name'],
            download_file = download_file,
            download_file_name = file_name,
        )
        # The KBaseReport configuration dictionary
        config = dict(
            report_name=f'efi_test_app_{str(uuid.uuid4())}',
            reports_path=results_dir,
            template_variables=template_variables,
            workspace_name=params['workspace_name'],
        )
        return self.create_report_from_template(template_path, config)

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
