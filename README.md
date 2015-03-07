JSON2Mantle
========================

Generate [Mantle](https://github.com/Mantle/Mantle) models using JSON files.

##Quick start

### Install 

```
pip3 install JSON2Mantle
```

### Usage

```
json2mantle [-h] [--prefix PREFIX] [--author AUTHOR]
                   json_file output_dir

```

### Example

```
json2mantle api_model.json class --prefix XYZ --author "John Smith"
```

will generate Mantle models according to your `api_model.json` structure. The output files will be created under `output_dir` directory, the author name will be `John Smith`, and the Objective-C classes have the prefix `XYZ`.

## Features

* Supports nested JSON data, which means JSON2Mantle can generate the correct number of classes that the JSON file contains.
* Convert field name like `var_name` to `varName` automatically.
* Python 3.

## Note

* When reserved words in Objective-C appear, it will replace the original name with a prefix `model`. For instance, if you have a field with the name `id`, the generated one would be `modelId`.
* Only supports generating Objective-C files.
* If the input JSON file is an array, it will ask you to give a name for the array items.

## TODO
- [ ] reserved words
- [ ] URL type
- [ ] Python 2 compatible

## License
The MIT License (MIT)
