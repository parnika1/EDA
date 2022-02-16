def checks_cons_bi(src="", wrk="", oup="", cop="", tnp="", indsn="", resp="", maxmisslmt=75):
    """
    :param src: Path to input folder
    :param wrk: Path to Work folder
    :param oup: Path to Output folder
    :param cop: Path to Outcopy folder
    :param tnp: Path to Temporary folder
    :param indsn: Name of the Input Data frame
    :param resp: Name of the target variable
    :param maxmisslmt: Missing percentage limit. Keep same value from the previous code.(1-100 Scale , Default:75)
    :return: Checks to be validated in the results
    """

    # Check if all the input parameters are properly specified
    if src == "" or wrk == "" or oup == "" or cop == "" or tnp == "" or indsn == "" or resp == "" or maxmisslmt == "":
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
        print('---------------------------------------------------')
        print("")

        # Creating refrences for required dataframes
        allclmndsn = str(indsn) + "_all_clmn_dtls.pkl"
        allunimissdsn = str(indsn) + "_all_uni_miss.pkl"
        allunifreqdsn = str(indsn) + "_all_uni_freq.pkl"
        allunipercdsn = str(indsn) + "_all_uni_perc.pkl"

        ivdsn = str(indsn) + "_all_bi_iv.pkl"
        woedsn = str(indsn) + "_all_bi_woe.pkl"
        chidsn = str(indsn) + "_all_bi_chisq.pkl"
        bindsn = str(indsn) + "_bin.pkl"
        tr3bindsn = str(indsn) + "_tr3_bin.pkl"
        tr6bindsn = str(indsn) + "_tr6_bin.pkl"

        if check_file(oup, ivdsn) and check_file(oup, woedsn) and check_file(oup, chidsn):  # Outcopy checks
            if check_file(wrk, bindsn) and check_file(wrk, tr3bindsn) and check_file(wrk, tr6bindsn):  # work checks
                if check_file(oup, allclmndsn) and check_file(oup, allunimissdsn) and check_file(oup,allunifreqdsn) and check_file(oup, allunipercdsn):  # Output folder

                    # read all column details and all univariate dataframe
                    all_clmn_dtls = load_pickle(oup, allclmndsn)
                    all_uni_miss = load_pickle(oup, allunimissdsn)
                    all_uni_perc = load_pickle(oup, allunipercdsn)
                    all_uni_freq = load_pickle(oup, allunifreqdsn)

                    # pick Variables where missing_per < maxmisslmt and
                    set1 = set(all_clmn_dtls[all_clmn_dtls.BIVAR_TYPE.isin(["CHAR", "CHAR - BINARY", "CHAR - OTHER"])].VAR_NAME)
                    set2 = set(all_uni_miss[all_uni_miss.MISSING_PERC <= maxmisslmt].VAR_NAME)
                    req_set = set1.intersection(set2)

                    # read all bin dataframes and append its variable o required list
                    bin_df = load_pickle(wrk, bindsn)
                    tr3bin_df = load_pickle(wrk, tr3bindsn)
                    tr6bin_df = load_pickle(wrk, tr6bindsn)

                    req_set = req_set.union(set(bin_df.columns), set(tr3bin_df.columns), set(tr6bin_df.columns))

                    # read all IV,WOE,CHISQ dataframes
                    all_iv_df = load_pickle(oup, ivdsn)
                    all_woe_df = load_pickle(oup, woedsn)
                    all_chisq_df = load_pickle(oup, chidsn)

                    # Print Results:
                    print("ALL_VARS")
                    print(len(req_set))
                    print("")
                    print("-----------------------------------------------")
                    print("IV_VARS")
                    print(all_iv_df.VAR_NAME.nunique())
                    print("")
                    print("-----------------------------------------------")
                    print("WOE_VARS")
                    print(all_woe_df.VAR_NAME.nunique())
                    print("")
                    print("-----------------------------------------------")
                    print("CHISQ_VARS")
                    print(all_chisq_df.VAR_NAME.nunique())
                    print("")
                    #Check if all the features required for Bi-variate analysis is presentin results
                    a = len(req_set)
                    b = max(all_iv_df.VAR_NAME.nunique(), all_woe_df.VAR_NAME.nunique(),
                            all_chisq_df.VAR_NAME.nunique())

                    if a == b:
                        print("ALL VARIABLE COUNTS MATCH.")
                        return True
                    elif a < b:
                        print(
                        "VARIABLE COUNTS DONT MATCH. TOTAL VARIABLES ACROSS DATASETS LESS THAN VARIABLES WITH BIVARIATE RESULTS. VERIFY STEPS 7 & 8.")
                        return False
                    else:
                        mismatch = list(req_set.difference(set().union(set(all_iv_df.VAR_NAME), set(all_woe_df.VAR_NAME), set(all_chisq_df.VAR_NAME))))
                        mismatch.remove(resp)

                        excl_df = pd.DataFrame(columns=['VAR_NAME'])
                        oth_df = pd.DataFrame(columns=['VAR_NAME'])
                        freq_df = pd.DataFrame(columns=['VAR_NAME'])
                        perc_df = pd.DataFrame(columns=['VAR_NAME'])
                        l = ['CUSTOMER_ZIPCODE']
                        c = list(all_clmn_dtls[all_clmn_dtls.UNIVAR_TYPE.isin(["DATE", "ID VAR", "NA."])].VAR_NAME)
                        d = list(all_uni_freq.VAR_NAME)
                        e = list(all_uni_perc.VAR_NAME)

                        for x in mismatch:
                            if x in l:
                                excl_df = df.append({'VAR_NAME': x}, ignore_index=True)

                            if x in c:
                                oth_df = oth_df.append({'VAR_NAME': x}, ignore_index=True)

                            if x in d:
                                freq_df = freq_df.append({'VAR_NAME': x}, ignore_index=True)

                            if x in e:
                                perc_df = perc_df.append({'VAR_NAME': x}, ignore_index=True)

                        # Print results
                        print("")
                        print("-----------------------------------------------")
                        print(
                        "ALL_VARS = MAX(IV_VARS,CHISQ_VARS)+EXCL_VARS+OTH_VARS+FREQ_VARS+1(FOR RESPONSE VARIABLE)")
                        print("EXCL_VARS")
                        print(excl_df.VAR_NAME.nunique())
                        print("")
                        print("-----------------------------------------------")
                        print("OTHR_VARS")
                        print(oth_df.VAR_NAME.nunique())
                        print("")
                        print("-----------------------------------------------")
                        print("FREQ_VARS")
                        print(freq_df.VAR_NAME.nunique())
                        print("")
                        print("-----------------------------------------------")
                        print("NUM_VARS")
                        print(perc_df.VAR_NAME.nunique())
                        print("")
                        print("-----------------------------------------------")

                        print("THE MAX PERC. OF A SINGLE LEVEL OF A VARIABLE IN FREQ_VARS SHOULD BE GREATER THAN THE LIMIT SPECIFIED IN Bi-Variate Analysis")
                        df1 = all_uni_freq[all_uni_freq.VAR_NAME.isin([freq_df.VAR_NAME])].groupby(['VAR_NAME'])[
                            'PERCENT'].max()
                        df1.reset_index(drop=True, inplace=True)
                        print(df1.head(freq_df.VAR_NAME.nunique()))

    else:
        return False
