import os
import glob

def displayFileLocation(pathToFile):
    print(f"File located! Access it here: {pathToFile}")
    os.startfile(os.path.dirname(pathToFile))

def locateFileByName(docName):
    docName += '.txt'
    txtFiles = glob.glob("Documents/*.txt")
    for path in txtFiles:
        if os.path.basename(path) == docName:
            displayFileLocation(path)
            return
    print("Document not found.")

def stripPunctuation(word):
    return ''.join(character for character in word if character.isalnum())

def buildIndex():
    # Load stop words from a file
    stopWordsFile = "StopWords.txt"
    stopWordsSet = loadStopWords(stopWordsFile)
    folderPath = "Documents/"
    txtFiles = glob.glob(folderPath + "*.txt")
    indexData = {}

    for path in txtFiles:
        docName = os.path.basename(path).replace('.txt', '')
        with open(path, 'r') as doc:
            lines = doc.readlines()

            for lineNumber, line in enumerate(lines, start=1):
                words = line.split()

                for word in words:
                    cleanedWord = stripPunctuation(word).lower()

                    if cleanedWord in stopWordsSet or not cleanedWord:
                        continue

                    if cleanedWord not in indexData:
                        indexData[cleanedWord] = {docName: {'frequency': 1, 'lineNumbers': [lineNumber]}}
                    else:
                        if docName not in indexData[cleanedWord]:
                            indexData[cleanedWord][docName] = {'frequency': 1, 'lineNumbers': [lineNumber]}
                        else:
                            indexData[cleanedWord][docName]['frequency'] += 1
                            if lineNumber not in indexData[cleanedWord][docName]['lineNumbers']:
                                indexData[cleanedWord][docName]['lineNumbers'].append(lineNumber)

    return [f.replace('.txt', '') for f in os.listdir(folderPath) if f.endswith('.txt')], indexData

def loadStopWords(filePath):
    stopWords = set()
    try:
        with open(filePath, 'r') as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    stopWords.add(word)
    except FileNotFoundError:
        print("Stop words file not found. Proceeding without stop words.")
    return stopWords

def searchContent(indexData):
    query = input('Enter a word or phrase to search in documents: ').lower()
    searchTerms = query.split()

    matchedFiles = []
    lineNumbers = []

    for term in searchTerms:
        if term in indexData:
            for docName, details in indexData[term].items():
                if docName in matchedFiles:
                    docIndex = matchedFiles.index(docName)
                    lineNumbers[docIndex].extend(details['lineNumbers'])
                else:
                    matchedFiles.append(docName)
                    lineNumbers.append(details['lineNumbers'])

    if matchedFiles:
        print('\nDocuments and Lines matching your query:\n')
        for i in range(len(matchedFiles)):
            print(f'{matchedFiles[i]} - Lines: {sorted(set(lineNumbers[i]))}')
    else:
        print('No matches found!')

def searchDocumentByName(docNames):
    # Take input from user and remove spaces
    query = input('Enter the document name or keyword (e.g., D1, Design): ').replace(" ", "").lower()
    
    # Check for exact match or partial match in document names
    matchingDocs = [doc for doc in docNames if query in doc.lower()]
    
    if matchingDocs:
        print("\nDocuments matching your input:")
        for doc in matchingDocs:
            print(f"- {doc}")
            locateFileByName(doc)
    else:
        print("No document found matching the input.")

def header():
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("*               Search Engine                 *")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")

def showMenu():
    header()
    print('Document Search Engine Menu------>')
    print('1. Refresh Index')
    print('2. Search by Document Name')
    print('3. Search by Document Content')
    print('4. Exit')
    selection = 0

    while selection not in [1, 2, 3, 4]:
        try:
            selection = int(input('Select an option (1-4): '))
        except ValueError:
            print("Invalid input. Please enter a valid option.")

    return selection

def mainProgram():
    docNames, indexData = buildIndex()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        selection = showMenu()

        if selection == 1:
            docNames, indexData = buildIndex()
            print('Index rebuilt successfully!')
        elif selection == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            header()
            print("Search by Document Name------->")
            searchDocumentByName(docNames)
        elif selection == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            header()
            print("Search by Document Content------->")
            searchContent(indexData)
        else:
            break

        input('\nPress Enter to continue.')

    os.system('cls' if os.name == 'nt' else 'clear')
    header()
    print('\nThank you for using this Document Search Tool!')

if __name__ == "__main__":
    mainProgram()

