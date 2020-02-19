#!/usr/bin/python
# Modified version of textgrid2csv to textgrid2stm 
# Zin
# Usage: ./textgrid2stm.py <file.TextGrid> [file.stm]

#textgrid2csv.py
# D. Gibbon
# 2016-03-15
# 2016-03-15 (V02, includes filename in CSV records)

#-------------------------------------------------
# Import modules

import sys, re
import os
import subprocess
import shlex
#-------------------------------------------------
# Text file input / output

def inputtextlines(filename):
    handle = open(filename,'r')
    linelist = handle.readlines()
    handle.close()
    return linelist

def outputtext(filename, text):
    handle = open(filename,'w')
    handle.write(str(text))
    handle.close()

def batch_replace(infile, outfile, columnid, text=''):
    inlinelist = inputtextlines(infile)
    
#-------------------------------------------------
# Conversion routines

def converttextgrid2stm(textgridlines,textgridname,fileid):

    stmtext = ''
    stmlist = []
    newtier = False
    for line in textgridlines[9:]:
        line = re.sub('\n','',line)
        line = re.sub('^ *','',line)
        linepair = line.split(' = ')
        if len(linepair) == 2:
            if linepair[0] == 'class':
                classname = linepair[1]
            if linepair[0] == 'name':
                tiername = linepair[1]
            if linepair[0] == 'xmin':
                xmin = "%.2f" % float(linepair[1].strip())
            if linepair[0] == 'xmax':
                xmax = "%.2f" % float(linepair[1].strip())
            if linepair[0] == 'text':
                if linepair[1].strip().startswith('"') and linepair[1].strip().endswith('"'):
                    text = linepair[1].strip()[1:-1]
                else:
                    text = str(linepair[1][1:-2].strip())
                diff = float(xmax)-float(xmin)

                #print text, len(text)
                #print text, len(text.split())
                if ( text != '' and len(text.split()) > 1 ):
                    if (text !='--Empty--' and diff >= 1):
                        stmtext += fileid + ' ' + '1' + ' ' + tiername.strip()[1:-1] + ' ' + xmin.strip() + ' ' + xmax.strip() + ' ' + '<0,f0,male>' + ' ' + text.strip() +'\n'

    return stmtext

#-------------------------------------------------
# Main caller

if __name__ == '__main__':    

    if len(sys.argv) < 2:
        print("Usage: textgrid2stm.py <textgridfilename> [stmfilename]")
        exit()
    textgridname = sys.argv[1]
    if not textgridname.endswith('.TextGrid'):
        exit()
    file_path=os.path.dirname(textgridname)
    fileid=os.path.basename(os.path.splitext(textgridname)[0])

    ctmname = os.path.join( file_path, fileid + '.ctm')
    
    if not os.path.exists(ctmname):
        exit()

    stmname = os.path.join( file_path, fileid + '.stm')
    stm_sorted_name = os.path.join( file_path, fileid + '_sorted.stm')
    

    textgrid = inputtextlines(textgridname)
    textstm = converttextgrid2stm(textgrid,textgridname,fileid)
    print (stmname)
    #print (textstm)
    outputtext(stmname,str(textstm))
    
    # sort the stm by start-time
    command = 'sort -k4 -n ' + stmname
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    outputtext(stm_sorted_name,output.decode("utf-8"))
    print("Output file: " + stm_sorted_name)
    
    #replace fileid in ctm file to be matched with stm fileid
    ctm_sorted_name = os.path.join(file_path, fileid + '_sorted.ctm')
    args = ["awk", r'{$1="'+fileid +'\" ; print ; }', ctmname]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if not error:
        outputtext(ctm_sorted_name, output.decode("utf-8"))
    else:
        ctm_sorted_name = ctmname
    # scoring with sclite
    command = 'sclite -r ' + stm_sorted_name + ' stm -h ' + ctm_sorted_name + ' ctm -o sum pra dtl prf '
    print(command)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
       print (error)

#-----------------------------------------------
#main()

#--- EOF -----------------------------------------
