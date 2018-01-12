
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ColorPrint:
    @staticmethod
    def print_message(Type, Tag, Message):
        if Type == "Error":
            print(bcolors.FAIL + "[ERROR]" + " " + Tag + ":" + bcolors.ENDC + Message)
        elif Type == "Ok":
            print(bcolors.OKGREEN + "[OK]"+ " " + Tag + ":" + bcolors.ENDC + Message)
        elif Type == "Warning":
            print(bcolors.WARNING + "[WARNING]" + " " + Tag + ":" + bcolors.ENDC + Message)
        elif Type == "FAIL":
            print(bcolors.FAIL + "[FAIL]" + " " + Tag + ":" + bcolors.ENDC + Message)
        elif Type == "Debug":
            print(bcolors.OKBLUE + "[DEBUG]" + " " + Tag + ":" + bcolors.ENDC + Message)

    @staticmethod
    def print(Message):
       ColorPrint.print_message("Debug", "Debugging", Message)