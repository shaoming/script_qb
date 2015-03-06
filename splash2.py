def Cholesky(dir,num):
    dir = "cd "+dir + '/kernels/cholesky'+"\n "
    cmd = './CHOLESKY '+'-p ' +  str(num)+' <inputs/tk29.O'
    return dir+cmd
def FFT(dir,num):
    dir = "cd "+dir + '/kernels/fft'+"\n "
    cmd = './FFT '+'-p ' +  str(num)+' -m20 -n65536 -l4'
    return dir+cmd
def LU_contig(dir,num):
    dir = "cd "+dir + '/kernels/lu/contiguous_blocks'+"\n "
    cmd = './LU '+'-p ' +  str(num)+' -n1024 -b16'
    return dir+cmd

def LU_noncontig(diri,num):
    dir = "cd "+dir + '/kernels/lu/non_contiguous_blocks'+"\n "
    cmd = './LU '+'-p ' +  str(num)+' -n1024 -b16'
    return dir+cmd

def Radix(dir,num):
    dir = "cd "+dir + '/kernels/radix'+"\n "
    cmd = './RADIX '+'-p ' +  str(num)+' -r1024 -n4194304 -m8388608'
    return dir+cmd

def Barnes(dir,num):
    dir = "cd "+dir + '/apps/barnes'+"\n "
    cmd = './BARNES '+ ' <input.p'+str(num)
    return dir+cmd

def FMM(dir,num):
    dir = "cd "+dir + '/apps/fmm'+"\n "
    cmd = './FMM '+ 'inputs/input.2048.p'+str(num)
    return dir+cmd

def Ocean_contig(dir,num):
    dir = "cd "+dir + '/apps/ocean/contiguous_partitions'+"\n "
    cmd = './OCEAN '+'-p ' +  str(num)+'  -n258'
    return dir+cmd

def Ocean_noncontig(dir,num):
    dir = "cd "+dir + '/apps/ocean/non_contiguous_partitions'+"\n "
    cmd = './OCEAN '+'-p ' +  str(num)+'  -n258'
    return dir+cmd

def Raytrace(dir,num):
    dir = "cd "+dir + '/apps/raytrace'+"\n "
    cmd = './RAYTRACE '+'-p ' +  str(num)+'   -m64 balls4.env'
    return dir+cmd

def Water_nsquared(dir,num):
    dir = "cd "+dir + '/apps/water-nsquared'+"\n "
    cmd = './WATER-NSQUARED '+'<input.p'+ str(num)
    return dir+cmd

def Water_spatial(dir,num):
    dir = "cd "+dir + '/apps/water-spatial'+"\n "
    cmd = './WATER-SPATIAL '+'<input.p'+ str(num)
    return dir+cmd
print eval("FFT('../',1)")
