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
	def getPBS_para(self,command,name,path,source_file):
		filename = './script/'+name+".sh"
		try:
                       f = open(filename,"w")
                except IOError:
                       print "cannot open the path ",path
                       sys.exit(1)
		f.write('#!/bin/bash'+"\n")
               	PBS_PARAM='#PBS -A loni_metrics_16 '+"\n"
                PBS_PARAM+='#PBS -q workq'+"\n"
                PBS_PARAM+='#PBS -l nodes=1:ppn=20'+"\n"
                PBS_PARAM+='#PBS -l walltime=60:00:00'+"\n"
                PBS_PARAM+='#PBS -o '+'./script/'+name+".output"+"\n"
                PBS_PARAM+='#PBS -j oe '+"\n"
                f.write(PBS_PARAM)
                f.write("cd "+path+ "\n")
                f.write("source "+source_file+ "\n")
		f.write(command+"\n wait \n")
		f.close()
		os.chmod(filename,stat.S_IEXEC | os.stat(filename).st_mode)
		return filename

class SPECexcuteScript:
	def __init__(self,path,source_file,prefix,benchmark,suffix):
		self.path = path
		self.source_file = source_file
		self.prefix = prefix
		self.benchmark = ""
		self.benchmark_name = ""
		name = benchmark
		#if 1:
		for name in benchmark:
			[fastforward, bench]=name.split(':')
			self.benchmark_name += bench
			self.benchmark += name+';'
		self.benchmark = self.benchmark[0:-1]
		self.suffix = suffix
	def getScript(self,path,fastforward,inst,suffix):
		#filename = path+self.benchmark_name+suffix+".sh"
		#if not os.path.exists(path):
		#	os.makedirs(path)
		#try:
		#	f = open(filename,"w")
		#except IOError:
		#	print "cannot open the path ",path
		#	sys.exit(1)
                #build/X86/gem5.opt --stats-file mcf.txt configs/example/dram_se.py  --report './m5out/mcf.txt' --script "1:mcf" -I 100000 
		#f.write('#!/bin/bash'+"\n")
		#PBS_PARAM='#PBS -A loni_metrics_16 '+"\n"
                #PBS_PARAM+='#PBS -q checkpt'+"\n"
                #PBS_PARAM+='#PBS -l nodes=1:ppn=20'+"\n"
                #PBS_PARAM+='#PBS -l walltime=48:00:00'+"\n"
                #PBS_PARAM+='#PBS -o '+path+self.benchmark_name+suffix+".output"+"\n"
		#f.write(PBS_PARAM)
		#f.write("cd "+self.path+ "\n")
		#f.write("source "+self.source_file+ "\n")
		reportfile = self.benchmark_name+suffix+".txt"
		cmd = "build/X86/gem5.opt  --remote-gdb-port=0 --stats-file "+reportfile+" "
		cmd= cmd+"configs/example/dram_se.py   --report " + "\""+reportfile+"\" "
		cmd= cmd + "--script "+"\""+self.benchmark+"\" " + " "+self.suffix+" "
		cmd =cmd + "-I " +str(inst)+" &\n"
		#f.write(cmd)
		#f.close()
		#os.chmod(filename,stat.S_IEXEC | os.stat(filename).st_mode)
		return cmd
path = "/work/shaoming/gem5_pcm"
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
#benches = [[bench[0],bench[3],bench[14],bench[14]],
#	[bench[0],bench[3],bench[16],bench[16]],
#	[bench[0],bench[6],bench[16],bench[16]],
#	[bench[3],bench[6],bench[16],bench[16]],
#	[bench[0],bench[3],bench[16],bench[14]],
#	[bench[3],bench[6],bench[16],bench[14]],
#	[bench[14],bench[14],bench[14],bench[14]],
#	[bench[15],bench[15],bench[15],bench[15]],
#	[bench[10],bench[14],bench[16],bench[18]],
#	[bench[10],bench[14],bench[17],bench[18]],
#	[bench[10],bench[16],bench[17],bench[18]],
#	[bench[14],bench[16],bench[17],bench[18]]
benches=  [[bench[0],bench[3],bench[6],bench[1]],
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
#benches= [[bench[6],bench[13],bench[11],bench[5]],
#	 [bench[11],bench[13],bench[8],bench[5]],
#	 [bench[5],bench[8],bench[10],bench[17]],
#	 [bench[5],bench[8],bench[17],bench[16]],
#	 [bench[13],bench[8],bench[10],bench[17]],
#	 [bench[13],bench[8],bench[17],bench[16]],
#         
#	 [bench[14],bench[14],bench[15],bench[15]],
#	 [bench[14],bench[14],bench[14],bench[14]],
#	 [bench[15],bench[15],bench[15],bench[15]],
	 #]

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
bench_scripts = []
for bench in benches:
	#for j in range(len(benchs)):
		#bench = bench *2
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--checkpoint_created"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --sub_channel 3 --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 1 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 2 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 4 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 1 --sub_channel 3  --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 2 --sub_channel 3  --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 4 --sub_channel 3  --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench," --smart --conf 2 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench," --smart  --L2fetch --Degreefetch 1  --conf 2 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench," --smart  --L2fetch --Degreefetch 2  --conf 2 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench," --smart  --L2fetch --Degreefetch 4  --conf 2 --sub_channel 3  --core_freq 4GHz"))
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --interleave --core_freq 3GHz")
		bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch  --L2fetch --Degreefetch 4  --sub_channel 3 --core_freq 2.4GHz --Pschedule"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 4 --sub_channel 3  --core_freq 2.4GHz"))
		#script = bench_script.getScript("./script/",2000,2*(10**8),"SINGLE__")
script = ""
#name = "MMCHECK__"
name = "MMSM_PS_P4_C3_24G"
#name = "MMSM_PCM_P4_C3_24G"
#name = "MMSM_PCM_P4_C3_4G"
#name = "MSM_SMART_P4_C3_24G"
for bench_script in bench_scripts:
		script += bench_script.getScript("./script/",2000,2*(10**8),name)
		#script = bench_script.getScript("./script/",2,2*(10**3))
#print script
script = PBS.getPBS_para(script,name,path,"rc")
print "command line",script
#subprocess.call("echo $PBS_PARAM", shell=True)
cmd = 'qsub '+script+"  \n"
#subprocess.call(cmd, shell=True)
print cmd
