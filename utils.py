########### Python 3.2 #############
import sys, getopt

COMMANDLINE_SHORT_OPTIONS = 'hq:f:t:p:s:j:d:' # help, string, from, to, prefix, suffix 
COMMANDLINE_LONG_OPTIONS = ['help', 'query', 'from', 'to', 'prefix', 'suffix', 'jobId', 'docId']
HELP_TEXT = '\t-h/--help for help\n\t-f/--from <from which language>\n\t-t/--to <to which language> \
    \n\t-q/--query <string to translate for text> \
    \n\t-p/--prefix <prefix of container, i.e. all docs in this subfolder, e.g. -p myDocsFolder> \
    \n\t-s/--suffix <suffix of all documents to translate, e.g. -s pdf to translate all file names ending with pdf> \
    \n\t-j/--jobId <job Id of the doucment translation job> \
    \n\t-d/--docId <document Id of a specific doucment in a Document Translation request> \
    \n'

def getThisRunningFileName():
    return sys.argv[0]

# For the command 
# expectedShortOptions has the arg list you expect
#   example expectedShortOptions = "hi:o:"
#   where h is a short option that does not need a value
#   i: and o: are short options that need a value (as they are with a :)
# expectedLongOptions has the long arg list you expect
#   example expectedLongOptions = ["input=", "output=", "help"]
#   where help is the long option that does not need a value
#   'input' and 'output' are long options that need a value (as they are suffixed with '=')
def getCommandLineArgs(expectedShortOptions, expectedLongOptions):
    justArgs = sys.argv[1:]
    return getopt.getopt(justArgs, expectedShortOptions, expectedLongOptions)

def needHelp(forceHelp):
    try:
        if (forceHelp == True):
            print("{}\n{}".format(getThisRunningFileName(), HELP_TEXT))
            return True
        opts, args = getCommandLineArgs(COMMANDLINE_SHORT_OPTIONS, COMMANDLINE_LONG_OPTIONS)
        # If help was an argument, process help
        for opt, val in opts:
            if opt == "-h" or opt == "--help":
                print("{}\n{}".format(getThisRunningFileName(), HELP_TEXT))
                return True
        return False
    except getopt.GetoptError:
        print("Failed to parse arguments")
        print("{}\n{}".format(getThisRunningFileName(), HELP_TEXT))
        return True

# Returns True/False, ValueOfArgument
def getArgumentValue(shortName, longName):
    try:
        opts, args = getCommandLineArgs(COMMANDLINE_SHORT_OPTIONS, COMMANDLINE_LONG_OPTIONS)
        for opt, val in opts:
            if opt in (shortName, longName):
                return True, val
        return False, ''
    except getopt.GetoptError:
        print("Failed to parse argument {}/{}\n".format(shortName, longName))
        return False, ''

# Returns True/False, ValueOfStringAfterAllKnownArgumentsWereParsed
def getNonArgumentTailString():
    try:
        opts, args = getCommandLineArgs(COMMANDLINE_SHORT_OPTIONS, COMMANDLINE_LONG_OPTIONS)
        return True, args
    except getopt.GetoptError:
        print("Failed to parse")
        return False, ''

######### Below is an example code on how to get command line arguments #########
# First check if arguments are passed correctly
# if not, print help text
#########
# if needHelp() == True:
#    print("{} - Help information above".format(getThisRunningFileName()))
#    exit()
#########
#########
# Now get the value for a given argument
# Pass either or both short and long name of argument
# If you do not pass short name, and user passes short name
# you will not get the value. Same with long name.
# So it is better to pass both short and long names
# to catch the value for the argument passed in short or long form by user
#########
# iShort = ''
# iLong = '--resource-name'
# status, optionVal = getArgumentValue(iShort, iLong)
# if (status == True):
#    print("Found {}".format(optionVal))
# else:
#    print("Not found")
#########
# If anything was passed after all the options 
# defined in the commanline options in the top of this file
# that is returned by this call
# status, input = getNonArgumentTailString()
# if (status):
#    print("True {}".format(input))
# else:
#    print("False {}".format(input))
