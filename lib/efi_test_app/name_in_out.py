"""
This ExampleReadsApp demonstrates how to use best practices for KBase App
development using the SFA base package.
"""

# This is the SFA base package which provides the Core app class.
from base import Core
import os
import uuid

MODULE_DIR = "/kb/module"
TEMPLATES_DIR = os.path.join(MODULE_DIR, "lib/templates")


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
        fname = params["family_name"]

        params["output_name"] = fname
        # This is the method that generates the HTML report
        return self.generate_report(params)

    def generate_report(self, params: dict):
        """
        This method is where to define the variables to pass to the report.
        """
        # This path is required to properly use the template.
        reports_path = os.path.join(self.shared_folder, "reports")
        # Path to the Jinja template. The template can be adjusted to change
        # the report.
        template_path = os.path.join(TEMPLATES_DIR, "report.html")
        # The keys in this dictionary will be available as variables in the
        # Jinja template. With the current configuration of the template
        # engine, HTML output is allowed.
        template_variables = dict(
            output_name=params["output_name"],
        )
        # The KBaseReport configuration dictionary
        config = dict(
            report_name=f"efi_test_app_{str(uuid.uuid4())}",
            reports_path=reports_path,
            template_variables=template_variables,
            workspace_name=params["workspace_name"],
        )
        return self.create_report_from_template(template_path, config)
