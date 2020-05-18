import csv


def fix(inputFileName, outputFileName):
    # read headers
    try:
        with open(inputFileName, "r") as csvInput:
            reader = csv.reader(csvInput)
            headers = next(reader)
    except IOError:
        print("File not found: " + inputFileName)
        return 1

    # read contents
    try:
        with open(inputFileName, "r") as csvInput:
            rawList = list(csv.DictReader(csvInput))
    except IOError:
        print("File not found: " + inputFileName)
        return 1

    # write
    with open(outputFileName, "w") as csvOutput:
        writer = csv.DictWriter(csvOutput, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()

        for row in rawList:
            rowData = {}
            for field in headers:
                if (field == "Text"):
                    text = row["Text"]
                    text = text.replace(" lessee ", "**LESSEE**").replace(" lessee.", "**LESSEE**")
                    rowData["Text"] = text
                else:
                    rowData[field] = row[field]
            writer.writerow(rowData)
        print("Output: " + outputFileName)

def getRegex(text):
    # start part of the regex
    regex = "(?i)^[/\s?.*-:]*"
    lastCharacterWasNotSpaceOrPunctuation = False
    inWildcard = False

    for i in range(len(text)):
        currentCharacter = text[i]
        # print(currentCharacter, lastCharacterWasNotSpaceOrPunctuation, inw)
        # if in wildcard, check if it is the end of the wildcard. if it is, add the wildcard regex, else do nothing
        if inWildcard:
            if currentCharacter == '*' and ((i + 1) < len(text)) and text[i + 1] == '*':
                regex += "[A-Z0-9/\-]+"
                lastCharacterWasNotSpaceOrPunctuation = True
                inWildcard = False
                # skip the last character of the wildcard
                i += 1
        else:
            # check if start of wildcard
            if currentCharacter == '*' and ((i+1) < len(text)) and text[i+1] == '*':
                inWildcard = True
                lastCharacterWasNotSpaceOrPunctuation = True
                # skip start of wildcard
                i += 1
            # check if character is alphanumeric, if so add it to the regex
            elif currentCharacter.isalnum():
                lastCharacterWasNotSpaceOrPunctuation = True
                regex += currentCharacter
            else:
                # add whitespace or punctuation regex in between words, but not at the end of the string
                if lastCharacterWasNotSpaceOrPunctuation and i < len(text) - 1:
                    # regex += "[\s?.\*\-:\/()'" + '\\"' + "\\\\" + "]+"
                    regex += "[^A-Z0-9]+"
                    lastCharacterWasNotSpaceOrPunctuation = False
    # end part of regex
    regex += "[\s?.*-:]*$"
    return regex

def generateRegex(inputFileName, outputFileName):
    # read headers
    try:
        with open(inputFileName, "r") as csvInput:
            reader = csv.reader(csvInput)
            headers = next(reader)
    except IOError:
        print("File not found: " + inputFileName)
        return 1

    # add regex column if it doesn't exist
    if ("Regex" not in headers):
        headers.append("Regex")

    # read contents
    try:
        with open(inputFileName, "r") as csvInput:
            rawList = list(csv.DictReader(csvInput))
    except IOError:
        print("File not found: " + inputFileName)
        return 1

    # write
    with open(outputFileName, "w") as csvOutput:
        writer = csv.DictWriter(csvOutput, fieldnames=headers, quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()

        for row in rawList:
            rowData = {}
            for field in headers:
                if (field == "Regex"):
                    rowData["Regex"] = getRegex(row["Text"])
                else:
                    rowData[field] = row[field]
            writer.writerow(rowData)
        print("Output: " + outputFileName)
