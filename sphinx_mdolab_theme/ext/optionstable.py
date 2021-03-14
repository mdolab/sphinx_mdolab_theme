from importlib import import_module
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table
from docutils.statemachine import ViewList
from docutils import nodes
import yaml
import os


class OptionsTable(Table):
    """
    This Table directive formats the defaultOptions dictionary in a nice table

    This is heavily adapted from
    https://github.com/BU-NU-CLOUD-SP16/Trusted-Platform-Module-nova/blob/master/api-ref/ext/rest_parameters.py
    """

    required_arguments = 0
    optional_arguments = 3
    has_content = True
    option_spec = {
        "filename": str,
        "widths": directives.positive_int_list,
        "type": directives.uri,
    }

    # default options
    filename = "options.yaml"

    def set_header(self):
        """
        sets the header and columns based on options
        """
        # default type is options
        if "type" not in self.options:
            self.options["type"] = "options"
        if self.options["type"] == "options":
            self.N_COLS = 4
            self.header = ["Name", "Type", "Default value", "Description"]
            self.col_widths = [1, 1, 1, 97]
        elif self.options["type"] == "informs":
            self.N_COLS = 2
            self.header = ["Code", "Description"]
            self.col_widths = [1, 99]
        else:
            raise NotImplementedError("type must be either 'options' or 'informs'.")

    def get_options_informs(self):
        # access the class name
        self.module_path, self.member_name = self.arguments[0].rsplit(".", 1)
        # import the class
        cls = getattr(import_module(self.module_path), self.member_name)
        # call the private function to get the default options or informs
        if self.options["type"] == "options":
            self.defaultOptions = cls._getDefaultOptions()
        elif self.options["type"] == "informs":
            self.informs = cls._getInforms()

    def get_descriptions(self):
        if "filename" in self.options:
            self.filename = self.options["filename"]
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"The file {self.filename} must exist! Failed module is {self.member_name}.")

        with open(self.filename) as f:
            self.yaml = yaml.load(f, Loader=yaml.FullLoader)

    def set_width(self):
        # sets the self.col_widths
        if "widths" in self.options:
            widths = self.options["widths"]
            assert len(widths) == self.N_COLS
            self.col_widths = widths

    def make_title(self):
        """
        This is taken directly from the Sphinx Table directive
        but simplified and modified so the title, i.e. caption is just the class name
        """
        if self.options["type"] == "options":
            title_text = f"{self.member_name} Default Options"  # this is the class name
        elif self.options["type"] == "informs":
            title_text = f"{self.member_name} Informs"  # this is the class name
        text_nodes, messages = self.state.inline_text(title_text, self.lineno)
        title = nodes.title(title_text, "", *text_nodes)
        return title, messages

    def run(self):
        # set the header based on type
        self.set_header()
        # set the self.defaultOptions or self.informs attribute
        self.get_options_informs()
        # read the descriptions if parsing options
        if self.options["type"] == "options":
            self.get_descriptions()
        # set width
        self.set_width()
        # get caption
        title, messages = self.make_title()
        # build table
        table_node = self.build_table()
        table_node.insert(0, title)
        return [table_node] + messages

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
        if self.options["type"] == "options":
            for key, value in self.defaultOptions.items():
                trow = nodes.row()
                # first add the name column, with text = key
                # this is the name of the option, wrapped in double backticks
                trow += add_col("``" + key + "``")
                # this is the type of the option
                # __name__ extracts the name of the datatype (e.g. str, float etc.)
                # otherwise this will display <class 'str'> etc
                defaultType = value[0]
                if isinstance(defaultType, tuple):
                    types = [str(t.__name__) for t in defaultType]
                    trow += add_col(" or ".join(types))
                else:
                    trow += add_col(str(defaultType.__name__))
                # this is the default value
                # here we do some type checking if we get a list of possible choices
                # TODO: could potentially import baseclasses and use existing code there
                defaultValue = value[1]
                if isinstance(defaultValue, list) and defaultType != list:
                    defaultValue = value[1][0]
                    choices = True  # we have a choice
                else:
                    choices = False
                # wrap default value in verbatim if str
                if defaultType == str:
                    defaultValue = f"``{defaultValue}``"
                trow += add_col(str(defaultValue))
                # this is the description from the yaml file
                # for choices, we expect a field called desc containing general description
                # plus one field for each possible choice
                # TODO: can add better error message when yaml file does not match
                desc = self.yaml[key]["desc"]
                if choices:
                    for choice in value[1]:
                        desc += f"\n\n-  ``{choice}``: \t{self.yaml[key][choice]}"
                # if there are no choices, we just pick out the entry from yaml
                trow += add_col(desc)
                rows.append(trow)
        # informs
        elif self.options["type"] == "informs":
            for key, value in self.informs.items():
                trow = nodes.row()
                # first add the name column, with text = key
                trow += add_col("``" + str(key) + "``")
                # add inform description
                trow += add_col(value)
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
