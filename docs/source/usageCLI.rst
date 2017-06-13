This is a command line script so you will need a terminal window open to use it.

Checking a HathiTrust package from the lab
------------------------------------------
To run validation on a package, type "qcpkg" followed by the path to the package. If the path has spaces in it, you must
surround the path by quotes.

For example:

    :command:`qcpkg "Y:\\DCC Unprocessed Files\\20170523_CavagnaCollectionRBML_rj"`



The Help Screen
---------------
This documentation should be up to date. However, you can always type :command:`makejp2 -h` into
a command prompt to display the script usage instructions along with any additional the options.

:command:`qcpkg -h`

.. code-block:: console

    usage: qcpkg [-h] [--debug] [--log-debug LOG_DEBUG] path

    positional arguments:
      path                  Directory of packages to be validated

    optional arguments:
      -h, --help            show this help message and exit
      --debug               Run script in debug mode
      --log-debug LOG_DEBUG
                            Save debug information to a file



It's that simple!