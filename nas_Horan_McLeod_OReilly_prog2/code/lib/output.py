from lib.globals import Globals
import sys

class Output:

        def output_results(self, output_file, stopReason, maxIts, xSeqTol, residualSeqTol, \
                           numIts=None, result=None, epsilon=None):
            """
            Outputs the results (or reasons for failure) for the Sparse SOR function
            to both the output_file() location and the prompt, before exiting the
            SOR function
            Arguments:  stopReason - The reason for exiting the algorithm.
                        maxIts - The number of iterations cycled through.
                        xSeqTol - The tolerance between sucsessive x estimations
                        residualSeqTol - The error tolerance
                        numIts - The number of iterations cycled through. ('None' if error)
                        result - The matrix generated by the SOR formula. ('None' if error)
                        epsilon - The machine epsilon number ('None' if error)
            Returns: None
            """

            ## Open writable file
            file = open(output_file, 'w')
            print(result)

            ##Generate headings line
            headings = '     Stopping Reason     | Max. Iterations |' \
                       ' No. Iterations |      Epsilon      |' \
                       ' X Seq. Tolerance | Res. Seq. Tolerance |'
            print(headings)

            ##Generate formatted stastical data
            stats = "{:^25}|{:^17}|{:^16}|{:^19}|{:^18}|{:^21}|" \
                .format(stopReason, str(maxIts), str(numIts), str(epsilon), str(xSeqTol), str(residualSeqTol))
            print(stats)
            file.write(headings + '\n')
            file.write(stats + '\n')

            if stopReason in (Globals.STOP_REASON_X_SEQ_CON, Globals.STOP_REASON_RES_CON, Globals.STOP_REASON_MAX_ITS):
                ## Only print results when appropriate to do so
                file.write('Results: %s' % result)
            file.close()
            sys.exit(0)