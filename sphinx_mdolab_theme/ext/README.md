# Options Table
This is a custom Sphinx extension for parsing a default options dictionary and generating an RST table.

## Usage
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

There are two options for the extension
- `filename` to specify the YAML file containing the description of the options. The default value is `options.yaml` under the current (i.e. `doc`) directory.
- `widths`, a list of four numbers specifying the relative width of the table columns. The default value is `[15, 10, 15, 40]`.


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
