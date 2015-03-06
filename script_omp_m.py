import os
import sys
import stat
import subprocess
class GolbalSetting:
	def __init__(self,walltime,work):
		self.PBS_PARAM='-A loni_metrics_16 -q workq -l nodes=1:ppn=20 -l walltime='+str(walltime)+':00:00  '
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
		#for name in benchmark:
		#	[fastforward, bench]=benchmark.split(':')
		#	self.benchmark_name += bench
		#	self.benchmark += name+';'
		self.benchmark = benchmark
		self.suffix = suffix
	def getScript(self,path,fastforward,inst,suffix):
		reportfile = self.benchmark+suffix+".txt"
		cmd = "build/X86/gem5.opt  --remote-gdb-port=0 --stats-file "+reportfile+" "
		cmd= cmd+"configs/example/dram_se.py --NPB --report " + "\""+reportfile+"\" "
		cmd= cmd + "--script "+"\""+self.benchmark+"\" " + " "+self.suffix+" "
		cmd =cmd + "-I " +str(inst)+" &\n"
		#f.write(cmd)
		#f.close()
		#os.chmod(filename,stat.S_IEXEC | os.stat(filename).st_mode)
		return cmd
path = "/work/shaoming/gem5"
PBS= GolbalSetting(48,path) ## 1 eight hours
#benchs = ["perlbench","mcf","bzip2","gcc","bwaves","gamess","mcf","milc","zeusmp","gromacs","cactusADM","leslie3d","namd","gobmk","dealII","soplex","povray","calculix","hmmer","sjeng","GemsFDTD","libquantum","h264ref","tonto","lbm","omnetpp","astar","wrf","sphinx3","xalancbmk"]
#benchs = ["perlbench","bzip2","gcc","mcf","milc","gromacs","gobmk","soplex","povray","hmmer","sjeng","libquantum","astar","sphinx3"]
#benchs = ["bzip2","gcc","mcf","milc","soplex","sjeng","libquantum","astar","sphinx3"]

#bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:splinx","45:soplex","226:omnetpp","142:sjeng","44:bzip2","14:gromacs","53:astar","20:hmmer","181:h264ref"]
#bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:sphinx3","45:soplex","226:omnetpp","142:sjeng","74:bzip2","14:gromacs","53:astar","101:hmmer","181:h264ref"]
#bench = ["13:lbm","23:libquantum","6:leslie3d","52:milc","50:mcf","65:sphinx3","45:soplex","11:zeusmp","63:gobmk","75:dealII","14:gromacs","53:astar","42:GemsFDTD","46:wrf","14:bzip2","20:hmmer"]
#benches = ["bt.A","bt.W","cg.A","cg.W","dc.A","dc.W","ep.A","ep.W","ft.A","ft.W","is.A","is.W","lu.A","mg.A","mg.W","sp.A","sp.W","ua.A","ua.W"]
#benches = ["bt.W","cg.W","dc.W","ep.W","ft.W","is.W","lu.W","mg.W","sp.W","ua.W"]
#benches = ["ammp_m.m","applu_m.m","apsi_m.m","art_m.m","equake_m.m","fma3d_m.m","gafort_m.m","mgrid_m.m","swim_m.m","wupwise_m.m"]
#benches = ["ammp_m.m","applu_m.m","apsi_m.m","art_m.m","equake_m.m","gafort_m.m","mgrid_m.m","wupwise_m.m"]
#benches = ["art_m.590","ammp_m.3529","equake_m.2757"]### time 10**7 instructions num for core 0
#benches = ["backprop.0","bfs.0","canneal.0","heartwall.0","hotspot.0","nw.0","ocean.0","particlefilter.0","streamcluster.0"]
#benches = ["art_m.685","lbm_omp.140","srad.1972"]
benches = ["equake_m.3386"]
#benches = ["hop.7","backprop.317"]
#benches = ["art_m.830","lbm_omp.140","ammp_m.3555","equake_m.4983","backprop.313"]
#benches = ["art_m.830","equake_m.4983","ocean.14"]
#benches = ["lud.0","nn.0","kmean.0","srad.0"]
#benches = ["lud.1232","srad.1972","stencil_omp.374"]
#benches = ["dc.0","Sphinx3.0"]
#benches = ["apr.0","hop.0","plas.0","scalparc.0"]
#benches = ["equake_m.0","stencil_omp.0"]
#benches = ["hop.0"]
#benches = ["imghisto_omp.0","cutcp_omp.0","bfs_omp.0","stencil_omp.0"]

#benches = ["art_m.590","canneal.73","hotspot.498"]
#benches = ["ammp_m.3529","equake_m.2757","backprop.318","bfs.1020","heartwall.416","nw.565"]
#benches = ["lbm_omp.0","sgemm_omp.0","spmv_omp.0"]
#benches = ["backprop.318","bfs.1020","canneal.73","heartwall.416","hotspot.498","nw.565","ocean.6"]
bench_scripts = []
for bench in benches:
	#for j in range(len(benchs)):
		#bench = bench *2
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--checkpoint_created"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--smart --memfetch --conf 2 --sub_channel 3 --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--NPBTEST --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --sub_channel 3 --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench," --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench," --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 1 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 2 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--L2fetch --Degreefetch 4 --sub_channel 3  --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --sub_channel 3 --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 1 --sub_channel 3  --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 2 --sub_channel 3  --core_freq 2.4GHz"))
		bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--memfetch --L2fetch --Degreefetch 4 --sub_channel 3  --core_freq 2.4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--smart --memfetch --conf 2 --sub_channel 3 --core_freq 4GHz"))
		#bench_scripts.append(SPECexcuteScript(path,"rc","",bench,"--smart --memfetch --L2fetch --Degreefetch 4` --conf 2 --sub_channel 3 --core_freq 4GHz"))
		#bench_script = SPECexcuteScript(path,"rc","",bench," --smart  --L2fetch --Degreefetch 4 --conf 2 --sub_channel 3 --core_freq 4GHz")
		#bench_script = SPECexcuteScript(path,"rc","",bench,"--memfetch --interleave --core_freq 3GHz")
		#script = bench_script.getScript("./script/",2000,2*(10**8),"SINGLE__")
script = ""
#name = "MMCHECK__"
#name = "P4_MSMART"
#name = "P4_M4G"
name = "P4_MM24G"
#name = "MNPB_TESTNN"
#name = "MCHECK"
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
