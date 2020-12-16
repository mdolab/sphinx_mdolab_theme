from importlib import import_module
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table
from docutils.statemachine import ViewList
from docutils import nodes
import yaml


class OptionsTable(Table):
    """
    This Table directive formats the defaultOptions dictionary in a nice table

    This is heavily adapted from
    https://github.com/BU-NU-CLOUD-SP16/Trusted-Platform-Module-nova/blob/master/api-ref/ext/rest_parameters.py
    """

    required_arguments = 0
    optional_arguments = 4
    has_content = True
    option_spec = {
        "optionvar": str,
        "filename": str,
        "header": str,
        "widths": directives.positive_int_list,
    }

    def get_options(self, cls):
        # extracts the dictionaries from the class instance
        class_instance = cls(raiseError=False)
        # since the name of the attribute can change, need to access via __dict__
        if "optionvar" in self.options:
            optionvar = self.options["optionvar"]
        else:
            optionvar = "defaultOptions"
        self.defaultOptions = class_instance.__dict__[optionvar]

    def get_descriptions(self):
        if "filename" in self.options:
            filename = self.options["filename"]
        else:
            filename = "options.yaml"
        with open(filename) as f:
            self.desc = yaml.load(f, Loader=yaml.FullLoader)

    def set_header(self):
        # sets the self.header and self.max_cols
        # based on options
        if "header" in self.options:
            self.header = self.options["header"].split(",")
        else:
            self.header = ["Option name", "Default value", "Description"]

        self.max_cols = len(self.header)

    def set_width(self):
        # sets the self.col_widths
        if "widths" in self.options:
            self.col_widths = self.options["widths"]
        else:
            self.col_widths = [20, 20, 40]

    def run(self):
        module_path, member_name = self.arguments[0].rsplit(".", 1)
        class_name = getattr(import_module(module_path), member_name)
        # set the self.defaultOptions attribute
        self.get_options(class_name)
        # read the descriptions
        self.get_descriptions()
        # set header option
        self.set_header()
        # set width
        self.set_width()
        table_node = self.build_table()
        return [table_node]

    def collect_rows(self):
        # Add a column for a field. In order to have the RST inside
        # these fields get rendered, we need to use the
        # ViewList. Note, ViewList expects a list of lines, so chunk
        # up our content as a list to make it happy.
        def add_col(value):
            entry = nodes.entry()
            result = ViewList(value.split("\n"))
            self.state.nested_parse(result, 0, entry)
            return entry

        rows = []
        groups = []
        # options
        for key, value in self.defaultOptions.items():
            trow = nodes.row()
            # first add the name column, with text = key
            trow += add_col("``" + key + "``")
            # default value
            trow += add_col(str(value))
            # description
            trow += add_col(self.desc[key])
            rows.append(trow)
        return rows, groups

    def build_table(self):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(self.header))
        table += tgroup

        tgroup.extend(
            nodes.colspec(colwidth=col_width, colname="c" + str(idx)) for idx, col_width in enumerate(self.col_widths)
        )

        thead = nodes.thead()
        tgroup += thead

        row_node = nodes.row()
        thead += row_node
        row_node.extend(nodes.entry(h, nodes.paragraph(text=h)) for h in self.header)

        tbody = nodes.tbody()
        tgroup += tbody

        rows, groups = self.collect_rows()
        tbody.extend(rows)
        table.extend(groups)

        return table


def setup(app):
    app.add_directive("optionstable", OptionsTable)
