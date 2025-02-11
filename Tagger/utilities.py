import csv
from typing import Dict, List, Callable

def generateDefaultKey(keyIndices: List[int], row) -> str:
            key = ""
            separator = "_"
            for i in keyIndices:
                key += f"{row[i].lower().strip()}{separator}"
            return key.rstrip(separator)

def createMapFromCsv(filePath: str, keyIndices: List[int], valueIndex: int, rowLength: int, getKey: Callable = generateDefaultKey):
    """
    Reads a CSV file and creates a dictionary where the key is composed
    of col indicated by keyIndices, and the value is the column indicated by valueIndex.
    """


    result_map = {}
    with open(filePath, mode='r') as file:
        csvReader = csv.reader(file)
        
        # Skip the header
        next(csvReader, None)
        
        # basic sanity
        for row in csvReader:
            if len(row) != rowLength:
                print(row)
                continue

            key = getKey(keyIndices, row)
            value = row[valueIndex].lower().strip()
            result_map[key] = value
    
    return result_map
    
    
def createCsvFromList(data: List[Dict], outputFilePath: str, fieldNames: List[str]):
    with open(outputFilePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldNames)
        writer.writerows(data)
    print(f"CSV file '{outputFilePath}' has been created.")
    


def createCsvFromMap(data: Dict, outputFilePath: str, fieldNames: List[str]):
    fieldnames = data.keys()

    with open(outputFilePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldNames)
        for key, value in data.items():
            writer.writerow([key, value])

    print(f"CSV file '{outputFilePath}' has been created.")

def getProtocolToNumberMap():
     return createMapFromCsv("./data/protocol_numbers.csv", [1], 0, 5)

def getNumberToProtocolMap():
     return createMapFromCsv("./data/protocol_numbers.csv", [0], 1, 5)
