import os
import sys
import stat
import subprocess
class GolbalSetting:
	def __init__(self,walltime,work):
		self.PBS_PARAM='-A loni_metrics_14 -q workq -l nodes=1:ppn=8 -l walltime='+str(walltime)+':00:00  '
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
		name = benchmark
		for name in benchmark:
			[fastforward, bench]=name.split(':')
			self.benchmark_name += bench
			self.benchmark += name+';'
		self.benchmark = self.benchmark[0:-1]
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
PBS= GolbalSetting(48,path) ## 1 eight hours
#benchs = ["perlbench","mcf","bzip2","gcc","bwaves","gamess","mcf","milc","zeusmp","gromacs","cactusADM","leslie3d","namd","gobmk","dealII","soplex","povray","calculix","hmmer","sjeng","GemsFDTD","libquantum","h264ref","tonto","lbm","omnetpp","astar","wrf","sphinx3","xalancbmk"]
#benchs = ["perlbench","bzip2","gcc","mcf","milc","gromacs","gobmk","soplex","povray","hmmer","sjeng","libquantum","astar","sphinx3"]
#benchs = ["bzip2","gcc","mcf","milc","soplex","sjeng","libquantum","astar","sphinx3"]

#bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:splinx","45:soplex","226:omnetpp","142:sjeng","44:bzip2","14:gromacs","53:astar","20:hmmer","181:h264ref"]
#bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:sphinx3","45:soplex","226:omnetpp","142:sjeng","74:bzip2","14:gromacs","53:astar","101:hmmer","181:h264ref"]
#bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:sphinx3","45:soplex","11:zeusmp","63:gobmk","75:dealII","14:gromacs","53:astar","42:GemsFDTD","46:wrf","14:bzip2","20:hmmer"]
bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:sphinx3","45:soplex","11:zeusmp","63:gobmk","75:dealII","14:gromacs","53:astar","42:GemsFDTD","46:cactusADM","14:bzip2","20:hmmer","25:omnetpp","15:sjeng","41:h264ref"]
#benchs = ["25:omnetpp","15:sjeng","41:h264ref"]
#bench = "75:dealII"
#benchs = #[[bench[0]],
	 #[bench[0],bench[0]],
#benchs=	 [[bench[0],bench[0],bench[0],bench[0]]
	 #[bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0]],
	 #[bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0],bench[0]]
benchs=  [[bench[0],bench[3],bench[6],bench[1]],
	 [bench[0],bench[3],bench[2],bench[1]],
	 [bench[0],bench[3],bench[6],bench[2]],
	 [bench[0],bench[6],bench[1],bench[2]],
	 [bench[3],bench[6],bench[1],bench[2]],
         [bench[4],bench[4],bench[4],bench[4]],
         [bench[4],bench[4],bench[11],bench[11]],
	 [bench[11],bench[11],bench[11],bench[11]]#,
#benchs=	 #[[bench[6],bench[11],bench[5],bench[8]],
#benchs = [bench[8]
#benchs=	 [[bench[6],bench[5],bench[8],bench[13]],
#         [bench[6],bench[8],bench[13],bench[11]],
#benchs=	 [[bench[6],bench[13],bench[11],bench[5]],
#	 [bench[11],bench[13],bench[8],bench[5]],
#	 [bench[5],bench[8],bench[10],bench[17]],
#	 [bench[5],bench[8],bench[17],bench[16]],
#	 [bench[13],bench[8],bench[10],bench[17]],
#	 [bench[13],bench[8],bench[17],bench[16]]#,
         
#[[bench[14],bench[14],bench[15],bench[15]],
#	 [bench[14],bench[14],bench[14],bench[14]],
#	 [bench[15],bench[15],bench[15],bench[15]],
	 #]

#	[bench[10],bench[14],bench[16],bench[17]],
#	[bench[10],bench[14],bench[16],bench[18]],
#	[bench[10],bench[14],bench[17],bench[18]],
#	[bench[10],bench[16],bench[17],bench[18]],
#	[bench[14],bench[16],bench[17],bench[18]]
         ]
#for i in range(len(benchs)):
#benchs = [[bench[0],bench[3],bench[14],bench[15]],
#	[bench[4],bench[11],bench[14],bench[15]],
#	[bench[14],bench[14],bench[15],bench[15]],
#	[bench[14],bench[14],bench[14],bench[14]],
#	[bench[15],bench[15],bench[15],bench[15]]
#	]
#benchs =[[bench[0],bench[3],bench[6],bench[2]]]
#banks=[32,16,8]
#ranks=[8,4,2]
#for i in range(9):
#benches = bench
for bench in benchs:
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
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--sub_channel 3 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart --conf 2 --sub_channel 3 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart --conf 3 --sub_channel 4 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"  --bank "+str(bank)+" --rank "+str(rank)+" --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--utilSchedule --LengthHisChannel 64 --order_bias 2 --rowhit_bias 500  --memfetch --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--utilSchedule --LengthHisChannel 32 --order_bias 2 --rowhit_bias 500  --memfetch --core_freq 3.2GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--interleave  --sub_channel 3 --core_freq 4GHz")
		bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --interleave  --sub_channel 3 --core_freq 2.4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart --core_freq 4GHz")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"BASCI__")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM__")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSMART_")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"M32_C412G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_C24G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSI_C34G")
		script = bench_script.getScript("./script/",2000,2*(10**8),"MSI_C324G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_C44G")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"MSM_C4_4G")
		#script = bench_script.getScript("./script/",500,2*(10**8),"MSMC3_4GLaccess500m")
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
		subprocess.call(cmd, shell=True)
		print cmd
