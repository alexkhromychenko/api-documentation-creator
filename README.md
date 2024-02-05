# API Documentation Creator

Creates documentation for a Spring Boot application REST API method in confluence format.

`OPENAI_KEY` env variable needs to be set

## Application command line parameters:

`-m`, `--method` - application method to document in a format `Class::method`.
`-p`, `--path` - list of paths to search files in.

### Example

`python api_documentation_creator.py -m Class::method -p /some/path/ /another/path/`