import os, sys, time

counter = 0
filename = open("/Users/arkasantra/arka/Sasha_Work/OutputFile/"+sys.argv[1])
for lines in filename.readlines():
    ##bxNumber << pdg << track_id << det_id << xx << yy << eneg << ev_weight << vtx_x << vtx_y << vtx_z << parentid << pxx << pyy << pzz
    lines    = lines.rstrip()
    if '#' in lines: continue
    
    eachWord = lines.split()
    if(int(eachWord[0]) > 1):break
    if(int(eachWord[3]) > 1001): continue
    counter += 1
    #print(eachWord)
    #if(int(eachWord[1])==-11 and int(eachWord[2])==1): counter += 1
    
print("Track multiplicity: ", counter)
