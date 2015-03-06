import re
class record:
   def  __init__(self,name,pattern):
            self.name=name
	    print name
	    self.pattern=re.compile(self.name+pattern)###\S*\s+(\d+)
   def matchLine(self,line):
	    value = 0
            match = self.pattern.search(line)
            if match:
                 value = float(match.group(1))
                 return True, value
	    else:
		return False, value

class header(record):
  def __init__(self):
	record.__init__(self,"---------- Begin Simulation Statistics ----------","")
  def matchLine(self,line):
        match = self.pattern.search(line)
	if match:
		return True
	else:
		return False

class records:
  def __init__(self,name,pattern,core_names):
	self.entries = []
	self.value = []
	for core in core_names:
		self.entries.append(record(core+name,pattern))
		self.value.append(0)
  def matchLine(self,line):
	i = 0
	for entry in self.entries:
		[find,value]= entry.matchLine(line)
		if find:
			self.value[i]=value
		i = i + 1 

class cumRecords(records):
  def __init__(self,name,pattern,core_names):
	records.__init__(self,name,pattern,core_names)
	self.LastValue = [0.0]*len(self.entries)
  def update(self):
	delValue = [0.0]*len(self.entries)
	for i in range(len(self.entries)):
		delValue[i] = self.value[i]-self.LastValue[i]
		self.LastValue[i]=self.value[i]
	return delValue

#if __name__ == "__main__":
mheader =  header()
mem_read = cumRecords(".bytesRead","\s+(\d+)",["system.physmem"])  
mem_written = cumRecords(".bytesWritten","\s+(\d+)",["system.physmem"])  
fetch_icache = cumRecords(".fetch.icacheStallCycles","\s+(\d+)",["system.switch_cpus"+str(i) for i in range(4)])
inst_l2_latency = cumRecords(".inst","\s+(\d+)",["system.l2.overall_miss_latency::switch_cpus"+str(i) for i in range(4)])
data_l2_latency = cumRecords(".data","\s+(\d+)",["system.l2.overall_miss_latency::switch_cpus"+str(i) for i in range(4)])
inst_l2 = cumRecords(".inst","\s+(\d+)",["system.l2.overall_accesses::switch_cpus"+str(i) for i in range(4)])
data_l2 = cumRecords(".data","\s+(\d+)",["system.l2.overall_accesses::switch_cpus"+str(i) for i in range(4)])
inst_mem = cumRecords(".inst","\s+(\d+)",["system.physmem.bytes_read::switch_cpus"+str(i) for i in range(4)])
data_mem = cumRecords(".data","\s+(\d+)",["system.physmem.bytes_read::switch_cpus"+str(i) for i in range(4)])
Instruction = cumRecords(".commit.committedInsts","\s+(\d+)",["system.switch_cpus"+str(i) for i in range(4)])
Cycle = cumRecords(".numCycles","\s+(\d+)",["system.switch_cpus"+str(i) for i in range(4)])
idleCycle = cumRecords(".idleCycles","\s+(\d+)",["system.switch_cpus"+str(i) for i in range(4)])
quiesceCycles = cumRecords(".quiesceCycles","\s+(\d+)",["system.switch_cpus"+str(i) for i in range(4)])
#for i in range(1,9):
if True:
	#file = open("/work/shaoming/gem5-mem/m5out/mem_-X1048576"+str(i)+"00GHzMEM_MC3G24.txt")
	file = open("/work/shaoming/gem5/m5out/blackscholes_4c_simlargeSTATC3G4.txt")
	#file = open("/work/shaoming/gem5/m5out/x264_1c_simlargeMSTATC3G4.txt")
	#file = open("/work/shaoming/gem5/m5out/bt_WSPLASH2_C3G4.txt")
	#file = open("/work/shaoming/gem5/m5out/vips_4c_simlargeSTATC3G4.txt")
	#file = open("/work/shaoming/gem5/m5out/Radix_4SPLASH2_MC3G24.txt")
	time =float(4*4*(10**6))
	for line in file.readlines():
		#fetch_icache.matchLine(line)
		#inst_l2_latency.matchLine(line)
		#data_l2_latency.matchLine(line)
		inst_mem.matchLine(line)
		#inst_l2.matchLine(line)
		#data_l2.matchLine(line)
		#inst_mem.matchLine(line)
		data_mem.matchLine(line)
		mem_read.matchLine(line)
		mem_written.matchLine(line)
		Instruction.matchLine(line)
		Cycle.matchLine(line)
		idleCycle.matchLine(line)
		quiesceCycles.matchLine(line)
		if mheader.matchLine(line):
			Ins = 1.0+float(sum(Instruction.update()))
			Cycles = (sum(Cycle.update())+1)
			idle = sum(idleCycle.update())+sum(quiesceCycles.update())
			output = "Inst\t"+str(float(Ins))+"\tCPI\t"+str(Cycles/Ins)
			output += "\tmem_read\t"+str(sum(mem_read.update()))
			output += "\tmem_write\t"+str(sum(mem_written.update()))
			output += "\tutilization\t"+str(Cycles/(time))
			print output
			
 	
	
