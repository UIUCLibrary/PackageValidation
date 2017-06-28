This is a command line script so you will need a terminal window open to use it.

Validate a package
------------------
To run validation on a package, type "qcpkg" followed by the type of package and path to the package. If the path has spaces in it, you must
surround the path by quotes.

Checking a HathiTrust package ready to be submitted to Hathi
------------------------------------------------------------

Example:

    :command:`qcpkg hathisubmit "Y:\\DCC Unprocessed Files\\20170523_CavagnaCollectionRBML_rj"`


See the list of a HathiTrust package from the lab
-------------------------------------------------
Use the --list-profiles argument to list available profiles to check.

For example:

    :command:`qcpkg --list-profiles"`

.. code-block:: console

    C:\Users\hborcher.UOFI>qcpkg --list-profiles

    hathilab
    hathisubmit



The Help Screen
---------------
This documentation should be up to date. However, you can always type :command:`makejp2 -h` or
:command:`makejp2 --help` into a command prompt to display the script usage instructions along with any
additional the options.


:command:`qcpkg -h`

.. code-block:: console

    C:\Users\hborcher.UOFI>qcpkg -h

    usage: qcpkg [-h] [--list-profiles | --version] [--save-report REPORT_NAME]
                 [--debug] [--log-debug LOG_DEBUG]
                 [profile] [path]

    optional arguments:
      -h, --help       show this help message and exit
      --list-profiles  List available package profiles
      --version        show program's version number and exit



It's that simple!