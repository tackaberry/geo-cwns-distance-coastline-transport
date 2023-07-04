SEG_DIST_1 = "1. <5km"
SEG_DIST_2 = "2. <10km"
SEG_DIST_3 = "3. <100km"
SEG_DIST_4 = "4. <1000km"
SEG_DIST_5 = "5. >1000km"

SEG_FLOW_1 = "1. <1lps"
SEG_FLOW_2 = "2. <5lps"
SEG_FLOW_3 = "3. <10lps"
SEG_FLOW_4 = "4. >10lps"

SEG_POP_1 = "1. <1000"
SEG_POP_2 = "2. <10000"
SEG_POP_3 = "3. <100000"
SEG_POP_4 = "4. >100000"

SEG_POWER_1 = "1. <10MW"
SEG_POWER_2 = "2. <100MW"
SEG_POWER_3 = "3. <1000MW"
SEG_POWER_4 = "4. >1000MW"



def seg_flow(x):
    if x.flow_lps < 1:
        return SEG_FLOW_1
    elif x.flow_lps < 5:
        return SEG_FLOW_2
    elif x.flow_lps < 10:
        return SEG_FLOW_3
    elif x.flow_lps >= 10:
        return SEG_FLOW_4
    else:
        return None
    

def seg_pop(x):
    if x.population < 1000:
        return SEG_POP_1
    elif x.population < 10000:
        return SEG_POP_2
    elif x.population < 100000:
        return SEG_POP_3
    elif x.population >= 100000:
        return SEG_POP_4
    else:
        return None
    
def seg_power(x):
    if x.capacity_mw < 10:
        return SEG_POWER_1
    elif x.capacity_mw < 100:
        return SEG_POWER_2
    elif x.capacity_mw < 1000:
        return SEG_POWER_3
    elif x.capacity_mw >= 1000:
        return SEG_POWER_4
    else:
        return None
    

MGD_TO_LPS = 3785411.8 / 86400