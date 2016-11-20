class OutputObject(object):
    '''
    Simple object to return when needed during or at end of iteration
    It will contain the state i.e. whether it is an exit call or not
    And it will contain relevant data to write in case of exit call
    or completion of iteration loop
    '''
    output_file = ""
    stopReason = ""
    maxIts = 0
    xSeqTol = 0
    residualSeqTol = 0
    numIts = 0
    x_zero = None
    epsilon = None
    exit_state = True
    csr = {}
    prev_diff = 0