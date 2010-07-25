#!/usr/bin/python
import os
import string
import sys

from optparse import OptionParser

def main():
    """
    python clean_database.py devel
    """

    usage = "usage: %prog [options] project"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=True,
                    help="make lots of noise [default]")
    parser.add_option("-s", "--site", default=1, help="Sites ID")
    parser.add_option("-p", "--path", help="File URI" )

    (options, args) = parser.parse_args()

    if len(args) != 1:
        sys.stderr.write("Type '%s --help' for usage.\n" % sys.argv[0])
        sys.exit(2)

    if not options.dsn:
        sys.stderr.write("Type '%s --help' for usage.\n" % sys.argv[0])
        sys.exit(2)
    
    # Allows us to import the models
    os.environ["DJANGO_SETTINGS_MODULE"] = "%s.settings" % args[0]

    # Import in the models
    try:
        from file_manager.models import File, FilePermission
    except ImportError, error:
        sys.stderr.write("%s\n" % error)
        sys.exit(1)

#    if options.verbose:
#        print "Options: %s" % options
#        print "Args: %s" % args

    # Walk through all listed permissions, ensure that the file still
    # exists. (Clear if it does not)
  
    
 
if __name__ == "__main__":
    main()
