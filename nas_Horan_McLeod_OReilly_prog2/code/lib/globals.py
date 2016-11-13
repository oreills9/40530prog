import numpy as np
import os

class Globals:
    '''
    Create class to hold global variables
    This allows for easier access from other classes and functions
    '''
    ## Allowable reasons for exiting process
    STOP_REASON_X_SEQ_CON = 'x Sequence Convergence'
    STOP_REASON_RES_CON = 'Residual Convergence'
    STOP_REASON_MAX_ITS = 'Max Iterations Reached'
    STOP_REASON_DIVERGENCE = 'x Sequence Divergence'
    STOP_REASON_ZERO_DIAGONAL = 'Zero On Diagonal'
    STOP_REASON_OTHER = 'Cannot Proceed'
    STOP_REASON_ZERO_MATRIX = 'Zero Matrix Size'
    STOP_REASON_INVALID_MATRIX = 'Invalid Matrix Input'
    STOP_REASON_NOT_DIAG_DOM = 'Not Diagonally Dominant'

    # Calculate Machine Epsilon
    Em = np.finfo(float).eps
    # This is the approx error used in tolerance calculation
    E = 1.0e-3

    #Set File path for files
    HOME_DIR = os.chdir("..")
    FILE_DIR = os.getcwd()+'/files'