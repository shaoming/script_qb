import os
import sys
import stat
import subprocess
class GolbalSetting:
	def __init__(self,walltime,work):
		self.PBS_PARAM='-A loni_metrics_15 -q workq -l nodes=1:ppn=20 -l walltime='+str(walltime)+':00:00  '
		#self.PBS_PARAM='-A loni_metrics_13 -q single -l nodes=1:ppn=4 -l walltime='+str(walltime)+':00:00  '
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
class SPECexcuteScript:
	def __init__(self,path,source_file,prefix,benchmark,suffix):
		self.path = path
		self.source_file = source_file
		self.prefix = prefix
		self.benchmark = ""
		self.benchmark_name = ""
		self.benchmark = benchmark
		self.suffix = suffix
	def getScript(self,path,fastforward,inst,suffix):
		filename = path+self.benchmark_name+suffix+".sh"
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
		f.write("source "+self.source_file+ "\n")
		reportfile = self.benchmark_name+suffix+".txt"
		cmd = "build/X86/gem5.opt --stats-file "+reportfile+" "
		cmd= cmd+"configs/example/dram_se.py   --report " + "\""+reportfile+"\" "
		cmd= cmd + "--script "+"\""+self.benchmark+"\" " + " "+self.suffix+" "
		cmd =cmd + "-I " +str(inst)+"  \n"
		f.write(cmd)
		f.close()
		os.chmod(filename,stat.S_IEXEC | os.stat(filename).st_mode)
		return filename
path = "/work/shaoming/gem5"
PBS= GolbalSetting(4,path) ## 1 eight hours
benches = ["bt:W"]
for bench in benches:
	#for j in range(len(benchs)):
		#bench = bench *2
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--checkpoint_created")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --interleave --core_freq 3GHz")
		#bank = banks[i/3]
		#rank = ranks[i%3]
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch "+"  --bank "+str(bank)+" --rank "+str(rank)+"  --interleave --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch "+"  --bank "+str(bank)+" --rank "+str(rank)+" --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --sub_channel 3  --core_freq 2.4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 1 --sub_channel 3  --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 1 --sub_channel 3  --core_freq 2.4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--sub_channel 3  --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --sub_channel 3 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--smart --memfetch --sub_channel 3 --core_freq 2.4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --sub_channel 3 --core_freq 2.4GHz")
		bench_script = SPECexcuteScript(path,"rc","",bench,"--NPB --memfetch --sub_channel 3 --core_freq 2.4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--sub_channel 3 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart --conf 2 --sub_channel 3 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart --conf 3 --sub_channel 4 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"  --bank "+str(bank)+" --rank "+str(rank)+" --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--utilSchedule --LengthHisChannel 64 --order_bias 2 --rowhit_bias 500  --memfetch --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--utilSchedule --LengthHisChannel 32 --order_bias 2 --rowhit_bias 500  --memfetch --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --interleave  --sub_channel 3 --core_freq 2.4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart --core_freq 4GHz")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"BASCI__")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM__")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSMART_")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"M32_C412G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_C24G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_C44G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_C4_4G")
		#script = bench_script.getScript("./script/",500,2*(10**8),"MSMC3_24G")
		script = bench_script.getScript("./script/",500,2*(10**8),"MSMC3_24Gtest")
		#script = bench_script.getScript("./script/",500,2*(10**8),"MSMC3_24GLaccess500m")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"F2D1MSM_C4G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"_CHECK_LBM_4")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSMART_C3")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSMART_C4")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"M32")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_TRACE")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"NEW_TEST")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_"+str(bank)+"_"+str(rank))
		#script = bench_script.getScript("./script/",2000,2*(10**8),"M32_"+str(bank)+"_"+str(rank))
		#script = bench_script.getScript("./script/",2000,2*(10**8),"M32_INT"+str(bank)+"_"+str(rank))
		#script = bench_script.getScript("./script/",2000,2*(10**8),"M32_DYN")
		#script = bench_script.getScript("./script/",2000,2*(10**5),"M32NEW_TEST")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"SINGLE__")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"CHECK__")
		#script = bench_script.getScript("./script/",2,2*(10**3))
		pbs = PBS.getPBS_para(os.getcwd()+"/script"+"/"+('_'.join(bench)))
       		print "command line",pbs
		subprocess.call("echo $PBS_PARAM", shell=True)
		cmd = 'qsub -V $PBS_PARAM '+script+"  \n"
		#subprocess.call(cmd, shell=True)
		print cmd
