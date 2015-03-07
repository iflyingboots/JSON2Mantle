JSON2Mantle
========================

Generate [Mantle](https://github.com/Mantle/Mantle) models using JSON files.

##Quick start
### Usage

`$ python3 JSON2Mantle.py [-h] [--prefix PREFIX] json_file output_dir`

### Example
`$ python3 JSON2Mantle.py api_model.json class --prefix XYZ`

will generate Mantle models according to your `api_model.json` structure. The output files will be created under `output_dir` directory, and the Objective-C classes have the prefix `XYZ`.

## Features
* Supports nested JSON data, which means JSON2Mantle can generate the correct number of classes that the JSON file contains.
* Convert field name like `var_name` to `varName` automatically.
* Written in Python 3.

## Notice
* `setup` is under construction.
* Only supports generating Objective-C files.

## TODO
- [ ] import necessary header files
- [ ] reserved words
- [ ] URL type

## License
The MIT License (MIT)
