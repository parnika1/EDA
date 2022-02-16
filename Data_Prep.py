def data_prep(src="", wrk="", oup="", cop="", tnp="", indsn="", vardsn="", resp="", lm=1):
    """
    :param src: Path to input folder
    :param wrk: Path to Work folder
    :param oup: Path to Output folder
    :param cop: Path to Outcopy folder
    :param tnp: Path to Temporary folder
    :param indsn: Name of the Input Data frame
    :param vardsn: Name of the dataset containing the top variables - output from Top_Variables
    :param resp: Name of the target variable
    :param lm: Unique identifier of output datasets for each run with various top variable combinations. <=3 characters
    :return: Binned and Raw dataframes with selected Top features
    """
    # Check if all the input parameters are properly specified
    if src == "" or wrk == "" or oup == "" or cop == "" or tnp == "" or indsn == "" or vardsn == "" or resp == "" or lm == "":
        print("INPUT PARAMETERS ARE NOT SPECIFIED PROPERLY IN FUNCTION CALL!")
        return False

    # import sys library for searching the below location for USD package(s)
    import numpy as np
    import pandas as pd
    import os.path
    from os import path
    import sys
    sys.path.insert(1, r'..\.')
    from Libraries.check_path import check_path
    from Libraries.check_file import check_file
    from Libraries.load_file import load_pickle, load_excel
    print("CHECK: IF SPECIFIED PATHS ARE VALID")
    if check_path(src, wrk, oup, cop, tnp):
        print("---------------------------------------------------")
        print("")

        # Creating references for required dataframes
        topiv = str(vardsn) + ".pkl"

        inpdsn = str(indsn) + ".pkl"
        tr3dsn = str(indsn) + "_tr3.pkl"
        tr6dsn = str(indsn) + "_tr6.pkl"

        bindsn = str(indsn) + "_bin.pkl"
        tr3bindsn = str(indsn) + "_tr3_bin.pkl"
        tr6bindsn = str(indsn) + "_tr6_bin.pkl"

        if check_file(oup, topiv) and check_file(src, inpdsn) and check_file(wrk, tr3dsn) and check_file(wrk,
                                                                                                         tr6dsn) and check_file(
                wrk, bindsn) and check_file(wrk, tr3bindsn) and check_file(wrk, tr6bindsn):
            # Check on target variable
            input_df = load_pickle(src, inpdsn)
            if len(input_df[resp].unique()) != 2:
                print("TARGET VARIABLE DOES NOT BELONG TO BINARY CLASS!")
                return False

            # read dataframes
            topiv_df = load_pickle(oup, topiv)
            tr3_df = load_pickle(wrk, tr3dsn)
            tr6_df = load_pickle(wrk, tr6dsn)

            input_bin_df = load_pickle(wrk, bindsn)
            tr3_bin_df = load_pickle(wrk, tr3bindsn)
            tr6_bin_df = load_pickle(wrk, tr6bindsn)

            # Creating buckted variable lists

            base_list = {'KNID', 'OBSERVATION_DATE'}
            inp_list_buc = set(topiv_df.KEEP_VARNAME).intersection(input_df.columns)
            tr3_list_buc = set(topiv_df.KEEP_VARNAME).intersection(tr3_df.columns)
            tr6_list_buc = set(topiv_df.KEEP_VARNAME).intersection(tr6_df.columns)
            inp_bin_list_buc = set(topiv_df.KEEP_VARNAME).intersection(input_bin_df.columns)
            tr3_bin_list_buc = set(topiv_df.KEEP_VARNAME).intersection(tr3_bin_df.columns)
            tr6_bin_list_buc = set(topiv_df.KEEP_VARNAME).intersection(tr6_bin_df.columns)

            fin_bin_list = base_list.union(inp_list_buc, tr3_list_buc, tr6_list_buc, inp_bin_list_buc, tr3_bin_list_buc,
                                           tr6_bin_list_buc)
            if len(fin_bin_list) - 2 == len(topiv_df.KEEP_VARNAME):
                # Prepare TOP VARS  MCT_BIN dataset
                df1 = input_df[list(base_list) + list(inp_list_buc) + [resp]]
                df1 = pd.merge(df1, tr3_df[list(base_list) + list(tr3_list_buc)], on=['KNID', 'OBSERVATION_DATE'],
                               how='inner')
                df1 = pd.merge(df1, tr6_df[list(base_list) + list(tr6_list_buc)], on=['KNID', 'OBSERVATION_DATE'],
                               how='inner')
                df1 = pd.merge(df1, input_bin_df[list(base_list) + list(inp_bin_list_buc)],
                               on=['KNID', 'OBSERVATION_DATE'], how='inner')
                df1 = pd.merge(df1, tr3_bin_df[list(base_list) + list(tr3_bin_list_buc)],
                               on=['KNID', 'OBSERVATION_DATE'], how='inner')
                mct_bin = pd.merge(df1, tr6_bin_df[list(base_list) + list(tr6_bin_list_buc)],
                                   on=['KNID', 'OBSERVATION_DATE'], how='inner')
                mct_bin.sort_values(by=['KNID', 'OBSERVATION_DATE'], inplace=True)
                mct_bin.reset_index(drop=True, inplace=True)
                
                # release memory
                del inp_list_buc
                del tr3_list_buc
                del tr6_list_buc
                del inp_bin_list_buc
                del tr3_bin_list_buc
                del tr6_bin_list_buc
                del input_bin_df
                del tr3_bin_df
                del tr6_bin_df
                del fin_bin_list
                del df1

            else:
                print(
                "TOP IV VARIABLE COUNT NOT MATCHES WITH FINAL KEEP_VARNAME LIST COUNT!Check TOP IV KEEP_VARNAMES!")
                return False

            # Creating raw variable lists
            inp_list_raw = set(topiv_df.VAR_NAME).intersection(input_df.columns)
            tr3_list_raw = set(topiv_df.VAR_NAME).intersection(tr3_df.columns)
            tr6_list_raw = set(topiv_df.VAR_NAME).intersection(tr6_df.columns)

            fin_raw_list = base_list.union(inp_list_raw, tr3_list_raw, tr6_list_raw)

            if len(fin_raw_list) - 2 == len(topiv_df.VAR_NAME):
                # Prepare TOP VARS MCT_RAW dataset
                df1 = input_df[list(base_list) + list(inp_list_raw) + [resp]]
                df1 = pd.merge(df1, tr3_df[list(base_list) + list(tr3_list_raw)], on=['KNID', 'OBSERVATION_DATE'],
                               how='inner')
                mct_raw = pd.merge(df1, tr6_df[list(base_list) + list(tr6_list_raw)], on=['KNID', 'OBSERVATION_DATE'],
                                   how='inner')
                mct_raw.sort_values(by=['KNID', 'OBSERVATION_DATE'], inplace=True)
                mct_raw.reset_index(drop=True, inplace=True)
                # release memory
                del inp_list_raw
                del tr3_list_raw
                del tr6_list_raw
                del input_df
                del tr3_df
                del tr6_df
                del df1

            else:
                print("TOP IV VARIABLE COUNT NOT MATCHES WITH FINAL VAR_NAME LIST COUNT!Check TOP IV KEEP_VARNAMES!")
                return False

            # Print Results
            print("VARS_TOP_DTST")
            print(topiv_df.VAR_NAME.nunique())
            print("--------------------------------------------------")
            print("")
            print("VARS_BIN_DTST")
            print(len(mct_bin.columns))
            print("--------------------------------------------------")
            print("")
            print("VARS_RAW_DTST")
            print(len(mct_raw.columns))

            # Saving output in SRCDRC
            try:
                mct_bin.to_pickle(r"{}\{}_{}_mct_bin.pkl".format(str(src), str(indsn), str(lm)))
                mct_raw.to_pickle(r"{}\{}_{}_mct_raw.pkl".format(str(src), str(indsn), str(lm)))
                print("Following output files successfully saved in Input folder")
                print("{}_{}_mct_bin".format(str(indsn), str(lm)))
                print("{}_{}_mct_raw".format(str(indsn), str(lm)))
            except:
                print("Failed to save the output. Please check your Input path!")
                return False
    else:
        return False
