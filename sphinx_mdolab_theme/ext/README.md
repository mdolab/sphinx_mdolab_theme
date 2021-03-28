# Custom Sphinx directives
## Options Table
This is a custom Sphinx extension for parsing a default options dictionary and generating an RST table.

### Usage
The extension is included by default in `conf.py` and does not need to be configured there.
To use, simply write the directive
```
.. optionstable:: <class name>
```
and make sure the class is on the path, which is usually achieved with
```
sys.path.insert(0, os.path.abspath("../"))
```
If the package has autodoc API documentation, then the above line is already there.

There are two optional arguments for the extension
- `filename` to specify the YAML file containing the description of the options. The default value is `options.yaml` under the current (i.e. `doc`) directory.
- `widths`, a list of four numbers specifying the relative width of the table columns. The default value is `[15, 10, 15, 40]`.

For this extension to work, two things must be in place in the code repo:
- a static method called `_getDefaultOptions` in the class that returns the default options dictionary
- a YAML file corresponding to the `filename` option above that contains the descriptions of the options

The capitalization of the option names **must match** between the default options dictionary, and the keys of the YAML file.
For readability, we recommend the options to be capitalized according to camelCase, since this will be the display name via this extension.

### Informs Table
There is in fact another optional argument which allows this directive to typeset a dictionary of informs of the format `Dict[str, str]`.
This will be rendered as a two-column table, using `cls()._getInforms()` as the function to extract the informs dictionary.
## Options List
This is an alternative to the table where each entry is typeset using the `py:data` directive.
We parse the YAML file and the options as normal, but generate a new temporary file and write each option as a `.. data::` directive.
The directive automatically includes this temporary file (but excludes it elsewhere in Sphinx to avoid duplication).
Unlike the Options Table, this directive only accepts one optional argument `filename`.
Typesetting informs is not possible with this directive.

# YAML File Format
The YAML file containing the descriptions must be of the following format:
```
<option>:
  desc: <description>
```
for simple options.
For options with multiple choices, the format is
```
<option>:
  desc: <general description>
  <choice 1>: <description of choice 1>
  <choice 2>: <description of choice 2>
```

If the description is long, it should be split into multiple lines.
In that case, the YAML operator `>` can be used:
```
<option>:
  desc: >
  <this can now be multiple lines>
```

Text written in the `desc` field will be parsed appropriately, therefore any RST/Sphinx markup can be used, such as italics, bold, or bullet points.
