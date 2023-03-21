/*
A KBase module: efi_test_app
*/

module efi_test_app {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_efi_test_app(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
