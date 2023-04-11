"""
This ExampleReadsApp demonstrates how to use best practices for KBase App
development using the SFA base package.
"""

# This is the SFA base package which provides the Core app class.
from base import Core
import os
import uuid
import zipfile

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
        self.ru = self.clients.ReadsUtils
        # self.shared_folder is defined in the Core App class.
        # TODO Add a self.wsid = a conversion of self.wsname

    def copy_name(self, params: dict):
        """
        This method is where the main computation will occur.
        """
        fname = params['family_name']

        results_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        text_file = os.path.join(results_dir, 'output.txt')

        log('Saving family name ' + fname)
        log(results_dir)
        log(text_file)

        with open(text_file, 'w') as fh:
            fh.write('Family name: ' + fname + '\n')

        params['output_name'] = fname
        # This is the method that generates the HTML report
        return self.generate_report(params, results_dir)

    def generate_download_file(self, params: dict, results_dir):

        output_files = list()

        output_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_dir)
        
        log('dl out dir ' + output_dir)

        result_file = os.path.join(output_dir, 'report.zip')

        with zipfile.ZipFile(result_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zip_fh:
            input_file = os.path.join(results_dir, 'output.txt')
            zip_file.write(input_file, 'results.txt')
        
        log('zip ' + result_file)

        output_files.append({'path': result_file,
                             'name': 'report.zip',
                             'label': 'report.zip',
                             'description': 'Report files'})

        log(output_files)
        log('end dl')

        return output_files

    def generate_report_file(self, params: dict, results_dir):

        html_report = list()

        output_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_dir)

        log('html')
        log(output_dir)

        report_file = os.path.join(output_dir, 'report.html')
        log(report_file)
        template_file = os.path.join(TEMPLATES_DIR, 'report_template.html')
        log(template_file)

        with open(report_file, 'w') as out_fh:
            with open(template_file, 'r') as template_fh:
                text = template_fh.read()
                log('TEXT: ' + text)
                text.replace('{{output_name}}', 'HTML report family name: ' + params['output_name'])
                out_fh.write(text)

        report_shock_id = self.dfu.file_to_shock({'file_path': output_dir, 'pack': 'zip'})['shock_id']
        log(report_shock_id)

        #html_report.append({
        html_report.append({'shock_id': report_shock_id,
                            'name': 'report.html',
                            'label': 'report.html',
                            'description': 'HTML summary report'})

        log('end html')

        return html_report

    def generate_report(self, params: dict, results_dir):
       
        log('start report')
        output_files = self.generate_download_file(params, results_dir)

        html_report_file = self.generate_report_file(params, results_dir)
        log('end report')

        report_params = {'message': '',
                         'workspace_name': params.get('workspace_name'),
                         'objects_created': [],
                         'file_links': output_files,
                         'html_links': html_report_file,
                         'direct_html_link_index': 0,
                         'html_window_height': 200,
                         'report_object_name': 'efi_test_app_report_' + str(uuid.uuid4())}

        log('report params')
        log(report_params)

        report_client = KBaseReport(self.callback_url)
        output = report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref', output['ref']}

        log('report_name:' + output['name'])
        log('report_ref:' + output['ref'])

        return report_output


        ## This path is required to properly use the template.
        #reports_path = os.path.join(self.shared_folder, 'reports')
        ## Path to the Jinja template. The template can be adjusted to change
        ## the report.
        #template_path = os.path.join(TEMPLATES_DIR, 'report.html')
        ## The keys in this dictionary will be available as variables in the
        ## Jinja template. With the current configuration of the template
        ## engine, HTML output is allowed.
        #template_variables = dict(
        #    output_name=params['output_name'],
        #)
        ## The KBaseReport configuration dictionary
        #config = dict(
        #    report_name=f'efi_test_app_{str(uuid.uuid4())}',
        #    reports_path=reports_path,
        #    template_variables=template_variables,
        #    workspace_name=params['workspace_name'],
        #)
        #return self.create_report_from_template(template_path, config)
