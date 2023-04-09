import os
from time import gmtime, strftime
import subprocess
from Common import *
import json

studentsIds = dict()

def loadData():
    os.system("pwd")
    print(os.path.exists("./data"))
    with open("./data/students.json", 'r') as f:
        global studentsIds
        studentsIds = json.loads(f.read())

def saveData():
    with open("./data/students.json") as f:
        f.write(json.dumps(studentsIds))

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def auth(studentId: str, password: str):
    try:
        return studentsIds[studentId][PASSWORD] == password
    except:
        return False
    
def runTest(inputStr: str, expectedOut: str, executableFilename: str) -> bool:
    process = subprocess.Popen([executableFilename], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = process.communicate(input=inputStr.encode())
    return output == expectedOut.encode()


def handle(request: dict[str, str]): 
    requestType = request[REQUEST_TYPE]
    if(requestType == CODE_SUBMISSION):
        return _handleCodeSubmission(request)
    if requestType == CHANGE_PASSWORD:
        return _handleChangePassword(request)
    



def _handleChangePassword(request: dict[str, str]):
    newPassword = request[NEW_PASSWORD]
    oldPassword = request[PASSWORD]
    studentId = request[STUDENT_ID]
    if(auth(studentId, oldPassword)):
        studentsIds[studentId][PASSWORD] == newPassword
        saveData()
        return {"outcome": True, "report": f"new password now set to {newPassword}"}
    else:
        return {"outcome": False, "report": "wrong password or st-id"}



def _handleCodeSubmission(request: dict[str, str]) -> dict:
    """
    {
        STUDENT_ID: ...
        "code": ....
        "problem name": ....

    }
    """
    # save it to archives (./data/archive/studentId/{problem}-{data}.asm)
    studentId = request[STUDENT_ID]
    code = request[CODE]
    problemName = request[PROBLEM_NAME]
    if(studentId not in studentsIds):
        return {"outcome": False, "report": "Invalid student number"}




    time = strftime("-%Y-%m-%d_%H:%M:%S", gmtime())

    archiveDir = f"./data/archive/{studentId}/"
    if(not os.path.exists(archiveDir)):
        os.mkdir(archiveDir)

    archiveFilePath = archiveDir + f"{problemName}-{time}.asm"
    with open(archiveFilePath, 'w') as f:
        f.write(code)

    # sourcePath = make_dir(f"./data/archive/{studentId}")
    # savePath = os.path.join(sourcePath, f"{archiveFilePath[:-4]}{time}.asm")

    # with open(code, 'r') as f:
    #     codeContents = f.read()

    # with open(savePath, 'w') as f:
    #     f.write(codeContents)
        


    # save code to a file (./data/runFolder/{studentId}/code.asm)
    # if the file is available replace it 
    # sourcePath = make_dir(f"./data/runFolder/{studentId}")
    # savePath = os.path.join(sourcePath, archiveFilePath)

    # with open(code, 'r') as f:
    #     codeContents = f.read()

    # with open(savePath, 'w') as f:
    #     f.write(codeContents)

    runPath = f"./data/runFolder/{studentId}"
    if(not os.path.exists(runPath)):
        os.mkdir(runPath)

    runFilePath = f"{runPath}/code.asm"
    with open(runFilePath, 'w') as f:   
        f.write(code)

     
    

    # compile the code (./data/runFolder/{studentId}/code.asm)
    os.system(f"nasm -f elf64 {runFilePath} -o {runPath}/code.o ")
    os.system(f"ld {runPath}/code.o -e _start -o {runPath}/a.out")
    

    # run the code for each test case in ./data/testCases/{problem}/in/test{*}.txt
    # compare with expected result in ./data/testCases/{problem}/out/test{*}.txt
    testCasesPath = f'./data/testCases/{problemName}'
    if(not os.path.exists(testCasesPath)):
        return {
            'outcome': False,
            'report': "problem name invalid or not available at the moment"
        }

    inputsFilenames =  os.listdir(f'{testCasesPath}/in')
    # outputsFilenames = os.listdir(f'{testCasesPath}/out')
    correctAnswers = 0
    for testnum in range(len(inputsFilenames)):
        with open(f'{testCasesPath}/in/input{testnum+1}.txt') as f:
            inTest = f.read()
        
        with open(f'{testCasesPath}/out/output{testnum+1}.txt') as f:
            outTest = f.read()
        
        if runTest(inTest, outTest, f"{runPath}/a.out"):
            correctAnswers += 1
    
    return {'submission result': f"{correctAnswers}/{len(inputsFilenames)}"}
    

    # return a list of booleans: [True, False, False]

