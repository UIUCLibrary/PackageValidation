# FURPS Requirements
**Authors:** 

* Henry Borchers
* William Schlaack

**Abstract:** The format for this document is based on the FURPS model developed by Hewlett-Packard and contains the 
list of requirements for the Python rewrite of the HathiTrust packaging script. 


## Table of Contents:
- Requirements
  * [Functional](#functional-requirements)
  * [Usability](#usability-requirements)
  * [Reliability](#usability-requirements)
  * [Performance](#performance-requirements)
  * [Supportability](#supportability-requirements)
  

## Functional Requirements

### Table 1: General Functional Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Read MD5 hashes                                 | Must     | Must be able to read MD5 hashes from sidecar hash manifest files. |
| xx   | Calculate MD5 hashes                            | Must     | Must be able to calculate MD5 hashes values from files. |
| xx   | Compare hash values                             | Must     | Must be able to compare hash values and check for matches for validation purposes.  |
| xx   | Validate base object naming scheme              | Must     | Must be able to match a base object name to a REGEX pattern.   |
| xx   | Validate the existence of files                 | Must     | Must be able to check a directory for the existence of files with predefined names.  |
| xx   | Check for subfolders                            | Must     | Must be able to check a folder for undesired subfolders. |
| xx   | Validate all files individually                 | Must     | Must be able to iterate over all files in folder. |
| xx   | Validate file naming scheme                     | Must     | Must be able to make sure that each of the file names match a specific REGEX expression |
| xx   | Create Log                                      | Must     | Must be able to generate a log of errors |
| xx   | Parse checksum list                             | Must     | Must be able to parse information in the checksum.md5 file  |
| xx   | Compare checksum inventory list to actual files | Must     | Must be able to match that every file listed in the checksum.md5 to a physical file in the same directory |
| xx   | Read and parse an XML File                      | Must     | Must be able to read an XML file  |

## Usability Requirements

### Table 2: General Usability Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   |  Installation documentation   | Must        | Must include written documentation on how to install the script.   |
| xx   |  User documentation           | Must        | Must include written documentation on how to use the script.   |
| xx   |  Command line interface       | Must        | Must include a command line user interface to run the script.   |
| xx   |  Graphical User interface     | High Want   | Script should be accessible through a graphical user interface.   |
| xx   |  Code documentation           | High Want   | Code should be documented to aid in future support and maintenance. |


## Reliability Requirements

### Table 3: General Reliability Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   |  On failure, terminate.       | Must        | If the script experience an unhandled exception/error, terminate the script and inform the user of the error. |


##Performance Requirements


### Table 4: General Performance Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   |  Unit testing                 | Must        |  Code base should include automated unit testing  |


## Supportability Requirements

### Table 5: General Supportability Requirements

| ID   | Description                   | Priority          | Details                                                  |
| ---- |:------------------------------| :---------------- | :------------------------------------------------------- |
| xx   | Run locally on workstations   | Must        | Must be able to run on Windows 7 desktops with ... [fill in this information]  |


