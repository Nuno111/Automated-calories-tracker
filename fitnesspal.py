import myfitnesspal
import functions
import sys

arguments = sys.argv

auth = functions.googleAuth()

client = myfitnesspal.Client('nuno_c11')

# Check for input errors

functions.validateInput(arguments)

# Run queries depending on number of arguments
if len(arguments) == 3:

    sheet = auth.open(sys.argv[1]).worksheet("Fitnesspal")

    functions.getSingle(sys.argv[1], sys.argv[2], client, sheet)

else:

    sheet = auth.open(sys.argv[1]).worksheet("Fitnesspal")

    functions.getRange(sys.argv[1], sys.argv[2], sys.argv[3], client, sheet)
