import os
import logging
from code.util import register
from code.util.db import Submission, Problem
import time
import shutil
import re
from uuid import uuid4

def addSubmission(probId, lang, code, user, type, custominput):
    sub = Submission()
    sub.problem = Problem.get(probId)
    sub.language = lang
    sub.code = code
    sub.result = "pending"
    sub.user = user
    sub.timestamp = time.time() * 1000
    sub.type = type

    if type == "submit":
        sub.save()
    elif type == "custom":
        sub.custominput = custominput
        sub.id = str(uuid4())
    else:
        sub.id = str(uuid4())
    return sub

exts = {
    "c": "c",
    "cpp": "cpp",
    "cs": "cs",
    "java": "java",
    "python2": "py",
    "python3": "py",
    "ruby": "rb",
    "vb": "vb"
}

def readFile(path):
    try:
        with open(path, "rb") as f:
            return f.read(1000000).decode("utf-8")
    except:
        return None

def strip(text):
    return re.sub("[ \t\r]*\n", "\n", text)

# Checks if <incomplete> contains only lines from <full> in order
# Can be missing some lines in the middle or at the end
def compareStrings(incomplete, full):
    lineNumOfFull = 0
    for line in incomplete.split('\n'):
        while lineNumOfFull < len(full.split('\n')):
            if line == full.split('\n')[lineNumOfFull]:
                break
            lineNumOfFull += 1
        else:
            return False
        lineNumOfFull += 1
    return True

def runCode(sub):
    # Copy the code over to the runner /tmp folder
    extension = exts[sub.language]
    os.mkdir(f"/tmp/{sub.id}")
    with open(f"/tmp/{sub.id}/code.{extension}", "wb") as f:
        f.write(sub.code.encode("utf-8"))
    
    prob = sub.problem
    
    if sub.type == "test":
        tests = prob.samples 
    elif sub.type == "custom":
        tests = 1
    else:
        tests = prob.tests     
    # Copy the input over to the tmp folder for the runner
    
    
   
    if sub.type != "custom":
        for i in range(tests):
            shutil.copyfile(f"/db/problems/{prob.id}/input/in{i}.txt", f"/tmp/{sub.id}/in{i}.txt") 
    else:
        with open(f"/tmp/{sub.id}/in0.txt", "w") as text_file:
            if(sub.custominput == None):
                sub.custominput = ""
            text_file.write(sub.custominput)    


    # Output files will go here
    os.mkdir(f"/tmp/{sub.id}/out")

    # Run the runner
    if os.system(f"docker run --rm --network=none -m 256MB -v /tmp/{sub.id}/:/source nathantheinventor/open-contest-dev-{sub.language}-runner {tests} 5 > /tmp/{sub.id}/result.txt") != 0:
        raise Exception("Something went wrong")

    inputs = []
    outputs = []
    answers = []
    errors = []
    results = []
    result = "ok"

    if sub.type != "custom":
        for i in range(tests):
            inputs.append(sub.problem.testData[i].input)
            errors.append(readFile(f"/tmp/{sub.id}/out/err{i}.txt"))
            outputs.append(readFile(f"/tmp/{sub.id}/out/out{i}.txt"))
            answers.append(sub.problem.testData[i].output)

            anstrip = strip((answers[-1] or "").rstrip()).splitlines()
            outstrip = strip((outputs[-1] or "").rstrip()).splitlines()

            res = readFile(f"/tmp/{sub.id}/out/result{i}.txt")
            if res == "ok" and strip((answers[-1] or "").rstrip()) != strip((outputs[-1] or "").rstrip()):
                if compareStrings(strip((outputs[-1] or "").rstrip()), strip((answers[-1] or "").rstrip())):
                    res = "incomplete_output"
                elif compareStrings(strip((answers[-1] or "").rstrip()), strip((outputs[-1] or "").rstrip())):
                    res = "extra_output"
                else:
                    res = "wrong_answer"
            if res == None:
                res = "tle"
            
            results.append(res)

            # Make result the first incorrect result
            if res != "ok" and result == "ok":
                result = res
    else:
        inputs.append(sub.custominput)
        outputs.append(readFile(f"/tmp/{sub.id}/out/out0.txt"))
        errors.append(readFile(f"/tmp/{sub.id}/out/err0.txt"))
        if(inputs[0]  != None): inputs[0] =  inputs[0].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if(outputs[0] != None):outputs[0] = outputs[0].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if(errors[0]  != None): errors[0] =  errors[0].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        answers.append("")
        res = readFile(f"/tmp/{sub.id}/out/result0.txt")
        if res == None:
            res = "tle"
        if res != "ok" and result == "ok":
            result = res
        results.append(res)

            
            
    sub.result = result    
    
    if readFile(f"/tmp/{sub.id}/result.txt") == "compile_error\n":
        sub.results = "compile_error"
        sub.delete()
        sub.compile = readFile(f"/tmp/{sub.id}/out/compile_error.txt")
        shutil.rmtree(f"/tmp/{sub.id}", ignore_errors=True)
        return

    sub.results = results
    sub.inputs  = inputs
    sub.outputs = outputs
    sub.answers = answers
    sub.errors  = errors
    
    if sub.type == "submit":
        sub.save()
    shutil.rmtree(f"/tmp/{sub.id}", ignore_errors=True)

def submit(params, setHeader, user):
    probId = params["problem"]
    lang   = params["language"]
    code   = params["code"]
    type   = params["type"]
    custominput = params.get("input")
    submission = addSubmission(probId, lang, code, user, type, custominput)
    runCode(submission)
    return submission.toJSON()

def changeResult(params, setHeader, user):
    id = params["id"]
    sub = Submission.get(id)
    if not sub:
        return "Error: incorrect id"
    sub.result = params["result"]
    sub.save()
    return "ok"

def rejudge(params, setHeader, user):
    id = params["id"]
    submission = Submission.get(id)
    if os.path.exists(f"/tmp/{id}"):
        shutil.rmtree(f"/tmp/{id}")
    runCode(submission)
    return submission.result

register.post("/submit", "loggedin", submit)
register.post("/changeResult", "admin", changeResult)
register.post("/rejudge", "admin", rejudge)
