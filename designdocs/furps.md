# FURPS Requirements

**Authors:** 

* Henry Borchers
* William Schlaack


## Abstract

> The format for this document is based on the FURPS model developed by Hewlett-Packard and contains the 
> list of basic requirements for a Python rewrite of the HathiTrust packaging script. 


## Table of Contents

* [Requirements](#requirements)
    * [Functional](#functional-requirements)
    * [Usability](#usability-requirements)
    * [Reliability](#reliability-requirements)
    * [Performance](#performance-requirements)
    * [Supportability](#supportability-requirements)
* [Technical Specifications](#technical-specifications)
    * [Folder Structure](#folder-structure)
    * [Included Files](#included-files)
        * [checksum.md5](#checksummd5)
        * [marc.xml](#marcxml)
        * [meta.yml](#metayml)
    * [Regular Expressions](#regular-expressions)
    * [XML Schema Documents](#xml-schema-documents)
* [Notes](#notes)
  

## Requirements

### Functional Requirements

#### Table 1: General Functional Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Read MD5 hashes                                 | Must     | Must be able to read MD5 hashes from sidecar hash manifest files. |
| xx   | Compare hash values                             | Must     | Must be able to compare hash values and check for matches for validation purposes.  |
| xx   | Validate base object naming scheme              | Must     | Must be able to match a base object name to a REGEX pattern. [See Regular Expressions section](#regular-expressions)   |
| xx   | Validate the existence of files                 | Must     | Must be able to check a directory for the existence of files with predefined names.  |
| xx   | Check for subfolders                            | Must     | Must be able to check a folder for undesired subfolders. |
| xx   | Validate all files individually                 | Must     | Must be able to iterate over all files in folder. |
| xx   | Validate file naming scheme                     | Must     | Must be able to make sure that each of the file names match a specific REGEX expression. [See Regular Expressions section](#regular-expressions) |
| xx   | Parse checksum list                             | Must     | Must be able to parse information in the checksum.md5 file  |
| xx   | Compare checksum inventory list to actual files | Must     | Must be able to match that every file listed in the checksum.md5 to a physical file in the same directory |
| xx   | Validate checksum inventory list format         | Must     | Must be able to make sure that the checksum.md5 is formatted correctly. [See technical specs](#technical-specifications)|
| xx   | Read and parse an XML file                      | Must     | Must be able to read an XML file  |
| xx   | Validate a XML file to .xsd schema file         | Must     | Must be able to validate an XML file to an XSD schema file |
| xx   | Read and parse a YAML file                      | Must     | Must be able to read an YAML file  |
| xx   | Validate fields inside a YAML file              | Must     | Must be able to validate the existence and correctness of fields within a YAML file |


### Usability Requirements

#### Table 2: General Usability Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Installation documentation    | Must        | Must include written documentation on how to install the script.   |
| xx   | User documentation            | Must        | Must include written documentation on how to use the script.   |
| xx   | User interface                | Must        | Must include some form of a user interface to run the script, either commandline or GUI   |
| xx   | Graphical User interface      | High Want   | Script should be accessible through a graphical user interface.   |
| xx   | Communicate all errors        | Must        | Inform the user of errors. |


### Reliability Requirements

#### Table 3: General Reliability Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Calculate MD5 hashes          | Must        | Must be able to reliably calculate MD5 hashes values from files. |
| xx   | Terminate on fatal error      | Must        | If the script experience an unhandled exception/error | 


### Performance Requirements

#### Table 4: General Performance Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Run locally on workstations   | Must        | Must be able to run on Windows 7 desktops with ... **TODO: fill in this information**  |


### Supportability Requirements

#### Table 5: General Supportability Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Log operations and errors     | Must        | Must be able to generate a log of operations and any errors |
| xx   | Unit testing                  | Must        |  Code base should include automated unit testing  |
| xx   | Code documentation            | High Want   | Code should be documented to aid in future support and maintenance. |


## Technical Specifications

### Folder Structure
**TODO: A very brief explanation of the file/folder structure**

#### Example
> **TODO: write an sample tree structure of a package**


### Included Files

#### checksum.md5
##### Format
The file checksum.md5 contains a list in the following format
> filename, checksum, checksum algorithm

##### Example
> **TODO: write an example of a line here**


#### marc.xml
##### Format
**TODO: explain the basic format of this file format**

##### Example
> **TODO: write an example here**

#### meta.yml
##### Format
**TODO: explain the basic format of this file format**

##### Example
> **TODO: write  an example here**

### Regular Expressions

> **Valid object id**
> ``` 
> ^\d+(p\d+(_\d+)?)?(v\d+(_\d+)?)?(i\d+(_\d+)?)?(m\d+(_\d+)?)?$
> ```

> **Valid file names**
> ```
>^([0-9]{8}|meta|marc|checksum)\.(txt|tif|jp2|xml|yml|md5)$
> ```

### XML Schema Documents
|  Name                  | URI    |
| :--------------------- | :----- |
| MARC 21 | http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd
| ALTO: Analyzed Layout and Text Object | http://www.loc.gov/standards/alto/alto.xsd |
| METS XLink | http://www.loc.gov/standards/xlink/xlink.xsd |

## Notes

> Write any additional notes here
