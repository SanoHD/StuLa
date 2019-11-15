import os, sys
from termcolor import cprint

os.system("cls")

var = {"_":" "}
func = {}
args = []
imported = []
commentsymbol = ";"
filename = sys.argv[1]
LN = 0
valid = list(abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890_)


def tv(V): # test var
    if V == "_": error("Invalid variable-name")
    for l in V:
        if not l in valid:
            error("Invalid variable-name")
    if V[0] in ["0","1","2","3","4","5","6","7","8","9"]: error("Invalid variable-name")
    return V

def error(txt):
    print("[ERROR]",LN,txt)
    print("---------------Data---------------")
    print("Vars ",var)
    print("Funcs",func)
    sys.exit()

def parser(line):
    global args, ret
    for v in var:
        if "="+str(v)+"!" in line: line = line.replace("="+str(v)+"!",str(var[v]))


    for a in range(len(args)):
        if "["+str(a)+"]" in line:
            line = line.replace("["+str(a)+"]",args[a])

    ##### STRING #####
    if "<s-" in line:
        vn, vv = line.split("<s-")
        var[tv(vn)] = str(vv)
    
    if "<+s-" in line:
        vn, vv = line.split("<+s-")
        var[tv(vn)] += str(vv)

    ##### INTEGER #####
    if "<i-" in line:
        vn, vv = line.split("<i-")
        var[tv(vn)] = int(vv)
    if "<+i-" in line:
        vn, vv = line.split("<+i-")
        var[tv(vn)] += int(vv)
    if "<-i-" in line:
        vn, vv = line.split("<-i-")
        var[tv(vn)] -= int(vv)
    if "<*i-" in line:
        vn, vv = line.split("<*i-")
        var[tv(vn)] *= int(vv)
    if "</i-" in line:
        vn, vv = line.split("</i-")
        var[tv(vn)] /= int(vv)

    ##### FLOAT #####
    if "<f-" in line:
        vn, vv = line.split("<f-")
        var[tv(vn)] = float(vv)

    ##### VARIABLE #####
    if "<v-" in line:
        vn, vv = line.split("<v-")
        var[tv(vn)] = var[vv]

    ##### INPUT #####
    if "<?-" in line:
        vn, vv = line.split("<?-")
        var[tv(vn)] = input(vv)

    ##### FUNCTION #####
    if "<!-" in line:
        vn, vv = line.split("<!-")
        tv(vn)
        vs = vv.split(" & ")
        vv = vs[0]
        args = []
        try:
            for a in vs[1:]: args.append(a)
        except: pass
        if vv in func:
            for f in func[vv]:
                parser(f)
                if ret != None: var[vn] = ret
                if ret == None: break
        else:
            error("Undefined function.")

    if line[:9] == "out:text/":
        print(line[9:],end="")
    if line[:9] == "out:line/":
        print(line[9:])        

    
    if line[:2] == "..":
        if line == "..*":
            ret = None
        else:
            ret = line[2:]
    else:
        ret = ""
    
    if line[:5] == "take ":
        if not line[5:] in ["StuTerm"]:
            getfunc(line[5:])
        imported.append(line[5:])

    if line[:9] == "destroy #":
        del(var[line[9:]])

    if "StuTerm" in imported:
        os.system("color")
        if line == "clear":
            os.system("cls")
        if line[:8] == "out:red/":
            cprint(line[8:],"red",end="")
        if line[:10] == "out:green/":
            cprint(line[10:],"green",end="")
        if line[:9] == "out:blue/":
            cprint(line[9:],"blue",end="")
        if line[:9] == "out:grey/":
            cprint(line[9:],"grey",end="")
        if line[:11] == "out:yellow/":
            cprint(line[11:],"yellow",end="")
        if line[:12] == "out:magenta/":
            cprint(line[12:],"magenta",end="")
        if line[:9] == "out:cyan/":
            cprint(line[9:],"cyan",end="")
        if line[:10] == "out:white/":
            cprint(line[10:],"white",end="")
        
    if line[1] == "|":
        pass

def getfunc(FileName):
    cfile = open(FileName)
    complete = cfile.read().split("\n")
    cfile.close()
    infunc = False
    e = []
    for c in complete:
        if c[:7] == "func/<<" and c[-2:] == ">>":
            funcname = c[7:-2]
            infunc = True
        if c == "<<>>" and infunc == True: infunc = False; func[funcname] = e[1:]; e = []
        if infunc == True:
            e.append(c)

getfunc(filename)

file = open(filename)

infunc = False
for L in file:
    LN += 1
    L = L.strip()
    if L[:7] == "func/<<" and L[-2:] == ">>": infunc = True
    if infunc == True and L == "<<>>": infunc = False
    
    if L != "" and infunc == False and L != "<<>>" and L[:len(commentsymbol)] != commentsymbol:
        parser(L)
    else:
        continue

print("\n---------------Data---------------")
print("Vars ",var)
print("Funcs",func)

