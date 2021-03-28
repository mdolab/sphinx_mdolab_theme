from importlib import import_module
from docutils.parsers.rst.directives.misc import Include
import yaml
import os

TEMP_FILE = "tmp.rst"


class OptionsList(Include):
    """
    This is an include directive, but with an extra step of generating a temporary options file
    which gets included.
    """

    optional_arguments = 1
    option_spec = {
        "filename": str,
    }

    # default file name
    filename = "options.yaml"
    # const strings
    TYPE_PREFIX = "   :type: "
    VALUE_PREFIX = "   :value: "
    INDENT = "   "

    def run(self):
        # set the self.defaultOptions attribute
        self.get_options_from_yaml()
        # read the descriptions
        self.get_descriptions()
        self.generate_temp_file()
        # reset the self.arguments to just the temp file name
        self.arguments = [TEMP_FILE]
        return super().run()

    def generate_temp_file(self):
        with open(TEMP_FILE, "w") as f:
            for key, value in self.defaultOptions.items():
                txt = []
                # first add the name column, with text = key
                # this is the name of the option, wrapped in double backticks
                txt.append(f".. data:: {key}")
                # this is the type of the option
                # __name__ extracts the name of the datatype (e.g. str, float etc.)
                # otherwise this will display <class 'str'> etc
                defaultType = value[0]
                if isinstance(defaultType, tuple):
                    types = [str(t.__name__) for t in defaultType]
                    txt.append(self.TYPE_PREFIX + " or ".join(types))
                else:
                    txt.append(self.TYPE_PREFIX + str(defaultType.__name__))
                # this is the default value
                # here we do some type checking if we get a list of possible choices
                # TODO: could potentially import baseclasses and use existing code there
                defaultValue = value[1]
                if isinstance(defaultValue, list) and defaultType != list:
                    defaultValue = value[1][0]
                    choices = True  # we have a choice
                else:
                    choices = False
                txt.append(self.VALUE_PREFIX + str(defaultValue))
                # this is the description from the yaml file
                # for choices, we expect a field called desc containing general description
                # plus one field for each possible choice
                # TODO: can add better error message when yaml file does not match
                desc = self.yaml[key]["desc"]
                # because this part needs to be indented in the RST file, we have to split it first
                if "\n" in desc:
                    desc = desc.splitlines()
                else:
                    desc = [desc]
                if choices:
                    for choice in value[1]:
                        desc.append(f"-  ``{choice}``: {self.yaml[key][choice]}")
                # we now insert the indent for each line
                desc = f"\n{self.INDENT}".join(desc)
                # we add the initial newline + indent
                desc = f"\n{self.INDENT}" + desc
                txt.append(desc)
                f.writelines("\n".join(txt))
                f.write("\n\n")

    def get_options_from_yaml(self):
        # access the class name
        self.module_path, self.member_name = self.arguments[0].rsplit(".", 1)
        # import the class
        cls = getattr(import_module(self.module_path), self.member_name)
        # call the private function to get the default options
        self.defaultOptions = cls._getDefaultOptions()

    def get_descriptions(self):
        if "filename" in self.options:
            self.filename = self.options["filename"]
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"The file {self.filename} must exist! Failed module is {self.member_name}.")

        with open(self.filename) as f:
            self.yaml = yaml.load(f, Loader=yaml.FullLoader)


def setup(app):
    app.add_directive("optionslist", OptionsList)
