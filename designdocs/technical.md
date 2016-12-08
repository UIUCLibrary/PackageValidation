# Technical Specifications

**Authors:** 
* Henry Borchers

## Table of Contents
* [Technical Specifications](#technical-specifications)
    * [Folder Structure](#folder-structure)
    * [Included Files](#included-files)
        * [checksum.md5](#checksummd5)
        * [marc.xml](#marcxml)
        * [meta.yml](#metayml)
    * [Regular Expressions](#regular-expressions)
    * [XML Schema Documents](#xml-schema-documents)




## Folder Structure
**TODO: A very brief explanation of the file/folder structure**

### Example
> **TODO: write an sample tree structure of a package**


## Included Files

### checksum.md5
#### Format
The file checksum.md5 contains a list in the following format
> filename, checksum, checksum algorithm

#### Example
> **TODO: write an example of a line here**


### marc.xml
#### Format
**TODO: explain the basic format of this file format**

#### Example
> **TODO: write an example here**

### meta.yml
##### Format
**TODO: explain the basic format of this file format**

#### Example
> **TODO: write  an example here**

## Regular Expressions

### Valid object id

``` 
^\d+(p\d+(_\d+)?)?(v\d+(_\d+)?)?(i\d+(_\d+)?)?(m\d+(_\d+)?)?$
```


### Valid file names

```
^([0-9]{8}|meta|marc|checksum)\.(txt|tif|jp2|xml|yml|md5)$
```

## XML Schema Documents
|  Name                                 | URI                                                                          |
| :------------------------------------ | :--------------------------------------------------------------------------- |
| MARC 21                               | http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd                   |
| ALTO: Analyzed Layout and Text Object | http://www.loc.gov/standards/alto/alto.xsd                                   |
| METS XLink                            | http://www.loc.gov/standards/xlink/xlink.xsd                                 |
