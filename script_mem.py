import os
import sys
import stat
import subprocess
import splash2
parameters= {"-B":[],
	 "-w":[str(10**x)+"k" for x in range(1,9)],
         "-X":[str(2**x) for x in range(10,22,3)],
         "-U":[],
	 "-P":[str(10**x)+"k" for x in range(7,10)],
	 "-c":[str(2**x) for x in range(2,9)],
	 "--drive_freq":[str(2**x)+"GHz" for x in range(9)]}
class GolbalSetting:
	def __init__(self,walltime,work):
		self.PBS_PARAM='-A loni_metrics_14 -q workq -l nodes=1:ppn=8 -l walltime='+str(walltime)+':00:00  '
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
	def __init__(self,path,bench,num_core,num):
		self.path = path
		self.bench = bench
		#self.size = size
		self.num_core = num_core
		self.num = num
	def CreateClientScript(self,path,filename,param):
		filename = filename.replace(" ", "")
		filename = filename.replace("_", "")
		filename = filename.replace("-", "")
		client = filename +"client.rcS"
		server = filename +"server.rcS"
		#SERVER=10.0.0.1
		#CLIENT=10.0.0.2
		subprocess.call("echo '#!/bin/sh' >"+server, shell=True,cwd=path)
		subprocess.call("echo 'SERVER=10.0.0."+str(self.num)+"' >>"+server, shell=True,cwd=path)
		subprocess.call("echo 'CLIENT=10.0.0."+str(self.num+1)+"' >>"+server, shell=True,cwd=path)
		subprocess.call("tail -n +4 memcached-server.rcS >>"+server, shell=True,cwd=path)

		subprocess.call("echo '#!/bin/sh' >"+client, shell=True,cwd=path)
		subprocess.call("echo 'XARGS=\" "+param+" \"' >>"+client, shell=True,cwd=path)
		subprocess.call("echo 'SERVER=10.0.0."+str(self.num)+"' >>"+client, shell=True,cwd=path)
		subprocess.call("echo 'CLIENT=10.0.0."+str(self.num+1)+"' >>"+client, shell=True,cwd=path)
		subprocess.call("tail -n +4 memcached-client.rcS >>"+client, shell=True,cwd=path)
		client = "./disk/"+client
		server = "./disk/"+server
		return client,server
	def getScript(self,params,path,fastforward, inst,script_path,suffix,input):
		client,server=self.CreateClientScript("/work/shaoming/gem5-mem/disk/",self.bench+"_"+params+suffix,params)
		params = params.replace(" ","")
		filename = path+self.bench+"_"+str(self.num_core)+params+suffix+".sh"
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
		reportfile = self.bench+"_"+params+suffix+".txt"
		cmd = "build/ARM/gem5.opt --stats-file "+reportfile+" "
		cmd= cmd+"configs/example/dram_fs.py --kernel=vmlinux-3.3-arm-vexpress-emm-pcie --machine-type=VExpress_EMM --disk arm-ubuntu-natty-headless_newdisk.img --fullsys --memcached -m 1024  --report " +reportfile+"  --clientscript "+client+" --serverscript "+server+" "
		#cmd= cmd + "--script "+"\""+str(fastforward)+":"+self.benchmark+";"+str(fastforward)+":"+self.subbench+"\" "
		#script_name = self.bench+"_"+suffix+str(self.num_core)+".rcS" 
		#cmd= cmd + "--exescript "+script_path+"/"+script_name+" "
		#cmd =cmd + "-I " +str(inst)+"  \n"
		cmd =cmd + input+"  \n"
		f.write(cmd)
		f.close()
		os.chmod(filename,stat.S_IEXEC | os.stat(filename).st_mode)
		return filename
path = "/work/shaoming/gem5-mem"
script_path = path + "/disk/scripts"
PBS= GolbalSetting(48,path) ## 1 eight hours
#benchs = ["bzip2","gcc","mcf","milc","soplex","sjeng","libquantum","astar","sphinx3"]
#benchs=["Cholesky","FFT","LU_contig","LU_noncontig","Radix","Barnes","FMM","Ocean_contig","Ocean_noncontig","Raytrace"]
#benchs=["Cholesky"]
#benchs = ["blackscholes", "bodytrack", "canneal", "dedup", "facesim", "ferret", "fluidanimate", "freqmine", "streamcluster","swaptions", "vips", "x264", "rtview"]
#benchs = ["x264"]
#sizes =  ["test", "simdev", "simsmall", "simmedium","simlarge"]
num_size = 4
num_core =4
n = 2
command = ""
freq="" 
param = ""
if True:
	#for param in parameters["-X"]:
	#	param = " -X "+param
	#for param in parameters["-w"]:
		#param = "-U -w "+param
	#	param = "-"+param
	#param = "-U "
	#for param in parameters["--drive_freq"]:
	#	param = "--drive_freq "+param
	#for param in parameters["-c"]:
	#	param = "-c "+param
	#for param in parameters["-P"]:
	#	param = "-P "+param
	#for param in parameters["-w"]:
	for freq in [str(100+100*x)+"GHz" for x in range(8)]:
	#for L1 in [str(2**x)+"kB" for x in range(5,11)]+[str(2**x)+"MB" for x in range(1,2)]:
		param = "-X "+str(2**20)+" "
		#command = " --drive_freq "+freq+" --L1I "+L1+"  "
		#freq = L1
		#param = "-w "+param
		#subprocess.call("rm -Rf "+bench+"*", shell=True,cwd=script_path)
		#subprocess.call("./splash2.py "+bench+" "+str(num_core), shell=True,cwd=script_path)
		bench_script = ParsecScript(path,"mem",num_core,n)
		#script = bench_script.getScript("./script/",2000,2*(10**8),script_path,"STATC3G4"," --conf 2 --sub_channel 3 --core_freq 4GHz")
		#script = bench_script.getScript("./script/",2000,2*(10**8),script_path,"MSTATC3G24","--memfetch  --conf 2 --sub_channel 3 --core_freq 2.4GHz")
		#script = bench_script.getScript(param,"./script/",2000,2*(10**8),script_path,freq+"MEM_MC3G24","--interleave --memfetch "+command+" --conf 2 --sub_channel 3 --core_freq 2.4GHz")
		script = bench_script.getScript(param,"./script/",2000,2*(10**8),script_path,freq+"MEM_MC3G4"," "+command+"--interleave --conf 2 --sub_channel 3 --core_freq 4GHz")
		#script = bench_script.getScript(param,"./script/",2000,2*(10**8),script_path,"MEM_C3G4"," --conf 2 --sub_channel 3 --core_freq 4GHz")
		#script = bench_script.getScript("./script/",2,2*(10**3))
		pbs = PBS.getPBS_para(os.getcwd()+"/script"+"/"+"mem")
       		#print "command line",pbs
		subprocess.call("echo $PBS_PARAM", shell=True)
		cmd = 'qsub -V $PBS_PARAM '+script+"  \n"
		subprocess.call(cmd, shell=True)
		n = n + 2
		print cmd
