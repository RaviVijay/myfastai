import pandas as pd
import re

def worker_lef(file):
    name = re.compile(r'MACRO (.*) ')
    size = re.compile(r'.*SIZE (.*) BY (.*) .*')

    """Make a dict out of the parsed, supplied lines"""
    with open(file) as f:
        for line in f:
            match = name.match(line)
            if match:
                cname = match.group(1)
                continue
            match2 = size.match(line)
            if match2:
                size0 = float(match2.group(1))
                size1 = float(match2.group(2))
                return [cname,float("{0:.4f}".format(size0*size1))]
    

def process_devices(devline):
    nfin_patt = re.compile('.*nfin=([0-9]*) .*')
    match = nfin_patt.match(devline)
    if match:
        nfin = match.group(1)
    else:
        nfin = 0
    capfil_patt = re.compile(r'capfil=1')
    match = capfil_patt.match(devline)
    if match:
        capfil = match.group(1)
    else:
        capfil = 0
    esd = re.compile(r'esd=1')
    x = re.compile('.*\$X=([0-9]*) .*')
    y = re.compile('.*\$Y=([0-9]*) .*')
    return [nfin, capfil, esd, x, y]


    
def worker_spice(file):
    fname = re.compile(r'.*/(.*).spice')
    name = re.compile(r'.SUBCKT(.*)')
    device = re.compile('^M[0-9]* (.*)')
    pode = re.compile('^X[0-9]* (.*)')
    pode2 = re.compile('^M[0-9]* (.*_mpode).*')

    match = fname.match(file)
    if match:
        fname = match.group(1)
        name = re.compile('.SUBCKT '+fname+' (.*)')

    with open(file) as f:
        flg = 0
        devicecnt = 0
        podecnt = 0
        fincnt = 0
        capfcnt = 0
        for line in f:
            match = name.match(line)
            if match:
                pincount = len(match.group(1).split())-4
                flg = 1
                continue
            if flg == 1:
                match2 = device.match(line)
                if match2:
                    dev = match2.group(1)
                    devicecnt = devicecnt+1
                    dev_details = process_devices(dev)
                    fincnt = fincnt  + int(dev_details[0])
                    capfcnt = capfcnt  + int(dev_details[1])
                match3 = pode.match(line)
                if match3:
                    dev = match3.group(1)
                    podecnt = podecnt+1
                match4 = pode2.match(line)
                if match4:
                    dev = match4.group(1)
                    podecnt = podecnt+1
                    devicecnt = devicecnt-1
        return [fname,pincount,devicecnt,podecnt,fincnt, capfcnt]

def lef_files(direc):
    n = 0
    while True:
        n += 1
        yield open(f'{direc}lef/%d.part' % n, 'w')

def split_lef(inp_lef_file,direc):
    pat = 'MACRO'
    fs = lef_files(direc)
    outfile = next(fs) 

    with open(inp_lef_file) as infile:
        for line in infile:
            if pat not in line:
                outfile.write(line)
            else:
                items = line.split(pat)
                outfile.write(items[0])
                for item in items[1:]:
                    outfile = next(fs)
                    outfile.write(pat + item)


def add_stdcell_details(df, fldname, drop=True):
    """add_datepart converts a column of df from a datetime64 to many columns containing
    the information from the date. This applies changes inplace.

    Parameters:
    -----------
    df: A pandas data frame. df gain several new columns.
    fldname: A string that is the name of the date column you wish to expand.
        If it is not a datetime64 series, it will be converted to one with pd.to_datetime.
    drop: If true then the original date column will be removed.

    Examples:
    ---------

    >>> df = pd.DataFrame({ 'A' : pd.to_datetime(['3/11/2000', '3/12/2000', '3/13/2000'], infer_datetime_format=False) })
    >>> df

        A
    0   2000-03-11
    1   2000-03-12
    2   2000-03-13

    >>> add_stdcell_details(df, 'A')
    >>> df

        AYear AMonth AWeek ADay ADayofweek ADayofyear AIs_month_end AIs_month_start AIs_quarter_end AIs_quarter_start AIs_year_end AIs_year_start AElapsed
    0   2000  3      10    11   5          71         False         False           False           False             False        False          952732800
    1   2000  3      10    12   6          72         False         False           False           False             False        False          952819200
    2   2000  3      11    13   0          73         False         False           False           False             False        False          952905600
    """
    fld = df[fldname]
    df['tech'] = fld.apply(lambda x:parse_std_cell(x)) 
    df[['tech','track','vt','func','drive']] = pd.DataFrame(df.tech.values.tolist(), index= df.index)

    if drop: df.drop(fldname, axis=1, inplace=True)

def parse_std_cell(stdc_name):
    split_std = re.compile('(^C|^P)([0-9]*)(...)._(.*)X([0-9]*)')
    m = split_std.match(stdc_name)
    if m:
        return list(m.groups(0))
    else:
        return [0,0,0,0,0]
        
def parse_std_cell(stdc_name):
    split_std = re.compile('(^C|^P)([0-9]*)(...)._(.*)X([0-9]*)')
    m = split_std.match(stdc_name)
    if m:
        return list(m.groups(0))
    else:
        return [0,0,0,0,0]
        


#def parse_std_cell(stdc_name,var):
#    if var == "tech":
#        ffc = re.compile('^C')
#        ffp = re.compile('^P')
#        if ffc.match(stdc_name):
#            return "16ffc"
#        elif ffp.match(stdc_name):
#            return "16ffp"
#        else:
#            return "NA"
#    elif var == "track":
#        track = re.compile('^.([0-9]*).*')
#        match = track.match(stdc_name)
#        if match:
#            return match.group(1)
#        else:
#            return "NA"
#    elif var == "vt":
#        track = re.compile('^.([0-9]*).*')
#        match = track.match(stdc_name)
#        if match:
#            return match.group(1)
#        else:
#            return "NA"
#
#
#def copy(x,n):
#    return "None"
