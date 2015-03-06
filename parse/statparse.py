import os
import sys
import stat
import subprocess
import tempfile
sys.path.append("../")
import parse
def getFilelist(rdir,names,perfix,suffix):
	files= []
	wholename=  []
	for name in names:
		fullname = ""
		names = ""
		for s_name in name:
			[num,single_name]=s_name.split(":")
			fullname += single_name 
			names += single_name+"\t"
		files.append(rdir+'/'+fullname+suffix)
		wholename.append(names)
	return files, wholename

def getTimelist(files,names,suffix):
	times= []
	for (file,name) in zip(files,names):
		file = file+suffix
		try:
			reader = open(file,'r')
		except IOError:
			print "cannot open a flie"
			print file
			sys.exit(1)
		#print file
		time = []
		import re
		for i in range(4):
			line = reader.readline()
			m = re.search("(\d+\.\d+)",line)
			time.append(m.group(0))
		#print name
		times.append('\t'.join(time))
	return times
def getStatlist(files,items):
	valueList=[]
	for file in files:			 
		file = file
		try:
			reader = open(file,'r')
		except IOError:
			print "cannot open a flie"
			print file
			sys.exit(1)
		for line in reader.readlines():
			for item in items:
				item.matchLine(line)
		values =""
		for item in items:
			for value in item.value:
				values+="\t"+str(value)
		valueList.append(values)
	return valueList
path = "/work/shaoming/gem5_pcm"
bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:sphinx3","45:soplex","11:zeusmp","63:gobmk","75:dealII","14:gromacs","53:astar","42:GemsFDTD","46:cactusADM","14:bzip2","20:hmmer","25:omnetpp","15:sjeng","41:h264ref"]
#benchs = ["25:omnetpp","15:sjeng","41:h264ref"]
#bench = "75:dealII"
#benchs = #[[bench[0]],
	 #[bench[0],bench[0]],
#benchs=	 [[bench[0],bench[0],bench[0],bench[0]]
	 #[bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0]],
	 #[bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0]]
benches=  [[bench[0],bench[3],bench[6],bench[1]],
	 [bench[0],bench[3],bench[2],bench[1]],
	 [bench[0],bench[3],bench[6],bench[2]],
	 [bench[0],bench[6],bench[1],bench[2]],
	 [bench[3],bench[6],bench[1],bench[2]],
         [bench[4],bench[4],bench[4],bench[4]],
         [bench[4],bench[4],bench[11],bench[11]],
	 [bench[11],bench[11],bench[11],bench[11]]]
dir = "/work/shaoming/gem5_pcm/m5out"
class Bench_process:
    def __init__(self,dir,benches,suffix):
	files, self.names = getFilelist(dir,benches,"",suffix)
	self.times = getTimelist(files,self.names,".stat")
	items = []
        items.append(parse.records(".avgRdBW","\s+(\d+\.\d+)",["system.physmem"]))
        items.append(parse.records(".avgWrBW","\s+(\d+\.\d+)",["system.physmem"]))
	self.valueList = getStatlist(files,items)
    def getName(self):
	return self.names
    def getData(self,i):
	return self.times[i]+self.valueList[i]
	#files, names = getFilelist(dir,benches,"","MMSM_PCM_P1_C3_4G.txt")
if __name__ =="__main__":
	benchp = []
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_C3_4G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_C3_24G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_P1_C3_4G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_P2_C3_4G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_P4_C3_4G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_P1_C3_24G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_P2_C3_24G.txt"))
	benchp.append(Bench_process(dir,benches,"MMSM_PCM_P4_C3_24G.txt"))
	names = benchp[0].getName()
	num = len(names)
	for i in range(num):
		print names[i] 
		for bench in benchp:
			print bench.getData(i)
		print "\n"
