import os
import sys
import stat
import subprocess
class GolbalSetting:
	def __init__(self,walltime,work):
		self.PBS_PARAM='-A loni_metrics_15 -q workq -l nodes=1:ppn=20 -l walltime='+str(walltime)+':00:00  '
		if not os.path.exists(work):
			print "the path do not exists : ",work
			sys.exit(1)
		self.work= work
	def getPBS_para(self,log):
		path,name = os.path.split(log)
		if not os.path.exists(path):
			print "the path do not exists : ",path
			sys.exit(1)
		if os.path.exists(log) and os.path.isdir(log):
			print "there is a directory with name : ",log
			sys.exit(1)
		var = self.PBS_PARAM + '-o '+log+' -j oe'
		os.environ["PBS_PARAM"] = var
		return var
class ParsecScript:
	def __init__(self,path,bench,size,num_core):
		self.path = path
		self.bench = bench
		self.size = size
		self.num_core = num_core
	def getScript(self,path,fastforward, inst,script_path,suffix,input):
		filename = path+self.bench+"_"+str(self.num_core)+"c_"+self.size+"_"+suffix+".sh"
		if not os.path.exists(path):
			os.makedirs(path)
		try:
			f = open(filename,"w")
		except IOError:
			print "cannot open the path ",path
			sys.exit(1)
                #build/X86/gem5.opt --stats-file mcf.txt configs/example/dram_se.py  --report './m5out/mcf.txt' --script "1:mcf" -I 100000 
		f.write('#!/bin/bash'+"\n")
		f.write("cd "+self.path+ "\n")
		f.write("source rc "+"\n")
		reportfile = self.bench+"_"+str(self.num_core)+"c_"+self.size+suffix+".txt"
		cmd = "build/X86/gem5.opt --stats-file "+reportfile+" "
		cmd= cmd+"configs/example/dram_fs.py --fullsys  --report " +reportfile+" "
		#cmd= cmd + "--script "+"\""+str(fastforward)+":"+self.benchmark+";"+str(fastforward)+":"+self.subbench+"\" "
		script_name = self.bench+"_"+str(self.num_core)+"c_"+self.size+".rcS" 
		cmd= cmd + "--exescript "+script_path+"/"+script_name+" "
		#cmd =cmd + "-I " +str(inst)+"  \n"
		cmd =cmd + input+"  \n"
		f.write(cmd)
		f.close()
		os.chmod(filename,stat.S_IEXEC | os.stat(filename).st_mode)
		return filename
path = "/work/shaoming/gem5"
script_path = path + "/disk/scripts"
PBS= GolbalSetting(6,path) ## 1 eight hours
#benchs = ["bzip2","gcc","mcf","milc","soplex","sjeng","libquantum","astar","sphinx3"]
#benchs = ["blackscholes", "bodytrack", "canneal", "dedup", "facesim", "ferret", "fluidanimate", "freqmine", "streamcluster","swaptions", "vips", "x264", "rtview"]
benchs = ["blackscholes"]
#benchs = ["blackscholes","canneal", "dedup", "freqmine","rtview"]
#benchs = ["x264"]
#benchs = ["blackscholes", "bodytrack", "canneal", "dedup", "facesim", "streamcluster", "vips", "rtview"]
#benchs = ["blackscholes"]
#benchs = ["x264"]
sizes =  ["test", "simdev", "simsmall", "simmedium","simlarge"]
num_size = 4
num_core = 4 
if True:
	for bench in benchs:
		subprocess.call("rm -Rf "+bench+"*", shell=True,cwd=script_path)
		subprocess.call("./writescripts.pl "+bench+" "+str(num_core), shell=True,cwd=script_path)
		bench_script = ParsecScript(path,bench,sizes[num_size],num_core)
		script = bench_script.getScript("./script/",2000,2*(10**8),script_path,"STATC3G4"," --conf 2 --sub_channel 3 --core_freq 4GHz")
		#script = bench_script.getScript("./script/",2000,2*(10**8),script_path,"MSTATC3G4","--memfetch  --conf 2 --sub_channel 3 --core_freq 2.4GHz")
		#script = bench_script.getScript("./script/",2000,2*(10**8),script_path,"MSTATC3G24"," --checkpoint_created ")
		#script = bench_script.getScript("./script/",2,2*(10**3))
		pbs = PBS.getPBS_para(os.getcwd()+"/script"+"/"+bench)
       		#print "command line",pbs
		subprocess.call("echo $PBS_PARAM", shell=True)
		cmd = 'qsub -V $PBS_PARAM '+script+"  \n"
		subprocess.call(cmd, shell=True)
		print cmd
