def cons_uni(src="", wrk="", oup="", cop="", tnp="", indsn=""):
    """
    :param src: Path to input folder
    :param wrk: Path to Work folder
    :param oup: Path to Output folder
    :param cop: Path to Outcopy folder
    :param tnp: Path to Temporary folder
    :param indsn: Name of the Input Data frame
    :return: Dataframes containing all univariate analysis of all the variables(Base + TR3 +TR6 variables)
    """
    # Check if all the input parameters are properly specified
    if src == "" or wrk == "" or oup == "" or cop == "" or tnp == "" or indsn == "":
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
    print("CHECK: IF SPECIFIED PATHS ARE VALID")
    check1 = check_path(src, wrk, oup, cop, tnp)
    if check1:
        print("---------------------------------------------------")
        print("")
        # Consolidate all columns details dataframes
        if path.exists(r"{}\{}_clmn_dtls.pkl".format(str(cop), str(indsn))):
            if path.exists(r"{}\{}_tr3_clmn_dtls.pkl".format(str(cop), str(indsn))):
                if path.exists(r"{}\{}_tr6_clmn_dtls.pkl".format(str(cop), str(indsn))):
                    #read base variables & derrived variables data dictionary
                    df = pd.read_pickle(r"{}\{}_clmn_dtls.pkl".format(str(cop), str(indsn)))
                    #read derived features pickle file
                    tr3_df = pd.read_pickle(r"{}\{}_tr3_clmn_dtls.pkl".format(str(cop), str(indsn)))
                    tr6_df = pd.read_pickle(r"{}\{}_tr6_clmn_dtls.pkl".format(str(cop), str(indsn)))
                    temp = df.append(tr3_df, ignore_index=True)
                    temp2 = temp.append(tr6_df, ignore_index=True)
                    temp2.drop_duplicates(keep='first', inplace=True)
                    temp2.reset_index(drop=True, inplace=True)
                    # Saving output files in output folder
                    try:
                        temp2.to_pickle(r"{}\{}_all_clmn_dtls.pkl".format(str(oup), str(indsn)))
                        temp2.to_excel(r"{}\{}_all_clmn_dtls.xlsx".format(str(oup), str(indsn)))
                        print("All columns details file has been successfully saved in Output folder")
                        print("{}_all_clmn_dtls".format(str(indsn)))
                    except:
                        print("Failed to save the output. Please check your output path!")
                        return False
                else:
                    print ("TR6 column details dataset does not exists!.Check the outcopy folder")
                    return False
            else:
                print ("TR3 column details dataset does not exists!.Check the outcopy folder")
                return False
        else:
            print ("Input column details dataset does not exists!.Check the outcopy folder")
            return False

        # Consolidate all missing details dataframes
        if path.exists(r"{}\{}_uni_miss.pkl".format(str(cop), str(indsn))):
            if path.exists(r"{}\{}_tr3_uni_miss.pkl".format(str(cop), str(indsn))):
                if path.exists(r"{}\{}_tr6_uni_miss.pkl".format(str(cop), str(indsn))):
                    df = pd.read_pickle(r"{}\{}_uni_miss.pkl".format(str(cop), str(indsn)))
                    tr3_df = pd.read_pickle(r"{}\{}_tr3_uni_miss.pkl".format(str(cop), str(indsn)))
                    tr6_df = pd.read_pickle(r"{}\{}_tr6_uni_miss.pkl".format(str(cop), str(indsn)))
                    temp = df.append(tr3_df, ignore_index=True)
                    temp2 = temp.append(tr6_df, ignore_index=True)
                    temp2.drop_duplicates(keep='first', inplace=True)
                    temp2.reset_index(drop=True, inplace=True)
                    # Saving output files in output folder
                    try:
                        temp2.to_pickle(r"{}\{}_all_uni_miss.pkl".format(str(oup), str(indsn)))
                        temp2.to_excel(r"{}\{}_all_uni_miss.xlsx".format(str(oup), str(indsn)))
                        print("---------------------------------------------------")
                        print("")
                        print("All Missing values details file has been successfully saved in Output folder")
                        print("{}_all_uni_miss".format(str(indsn)))
                    except:
                        print("Failed to save the output. Please check your output path!")
                        return False
                else:
                    print ("TR6 missing details dataset does not exists!.Check the outcopy folder")
                    return False
            else:
                print ("TR3 missing details dataset does not exists!.Check the outcopy folder")
                return False
        else:
            print ("Input missing details dataset does not exists!.Check the outcopy folder")
            return False

        # Consolidate all character details dataframes
        if path.exists(r"{}\{}_uni_freq.pkl".format(str(cop), str(indsn))):
            if path.exists(r"{}\{}_tr3_uni_freq.pkl".format(str(cop), str(indsn))):
                if path.exists(r"{}\{}_tr6_uni_freq.pkl".format(str(cop), str(indsn))):
                    df = pd.read_pickle(r"{}\{}_uni_freq.pkl".format(str(cop), str(indsn)))
                    tr3_df = pd.read_pickle(r"{}\{}_tr3_uni_freq.pkl".format(str(cop), str(indsn)))
                    tr6_df = pd.read_pickle(r"{}\{}_tr6_uni_freq.pkl".format(str(cop), str(indsn)))
                    temp = df.append(tr3_df, ignore_index=True)
                    temp2 = temp.append(tr6_df, ignore_index=True)
                    temp2.drop_duplicates(keep='first', inplace=True)
                    temp2.reset_index(drop=True, inplace=True)
                    # Saving output files in output folder
                    try:
                        temp2.to_pickle(r"{}\{}_all_uni_freq.pkl".format(str(oup), str(indsn)))
                        temp2.to_excel(r"{}\{}_all_uni_freq.xlsx".format(str(oup), str(indsn)))
                        print("---------------------------------------------------")
                        print("")
                        print("All character values detail file has been successfully saved in Output folder")
                        print("{}_all_uni_freq".format(str(indsn)))
                    except:
                        print("Failed to save the output. Please check your output path!")
                        return False
                else:
                    print ("TR6 character details dataset does not exists!.Check the outcopy folder")
                    return False
            else:
                print ("TR3 character details dataset does not exists!.Check the outcopy folder")
                return False
        else:
            print ("Input character details dataset does not exists!.Check the outcopy folder")
            return False

        # Consolidate all numeric details dataframes
        if path.exists(r"{}\{}_uni_perc.pkl".format(str(cop), str(indsn))):
            if path.exists(r"{}\{}_tr3_uni_perc.pkl".format(str(cop), str(indsn))):
                if path.exists(r"{}\{}_tr6_uni_perc.pkl".format(str(cop), str(indsn))):
                    df = pd.read_pickle(r"{}\{}_uni_perc.pkl".format(str(cop), str(indsn)))
                    tr3_df = pd.read_pickle(r"{}\{}_tr3_uni_perc.pkl".format(str(cop), str(indsn)))
                    tr6_df = pd.read_pickle(r"{}\{}_tr6_uni_perc.pkl".format(str(cop), str(indsn)))
                    temp = df.append(tr3_df, ignore_index=True)
                    temp2 = temp.append(tr6_df, ignore_index=True)
                    temp2.drop_duplicates(keep='first', inplace=True)
                    temp2.reset_index(drop=True, inplace=True)
                    # Saving output files in output folder
                    try:
                        temp2.to_pickle(r"{}\{}_all_uni_perc.pkl".format(str(oup), str(indsn)))
                        temp2.to_excel(r"{}\{}_all_uni_perc.xlsx".format(str(oup), str(indsn)))
                        print("---------------------------------------------------")
                        print("")
                        print("All numeric values details  has been successfully saved in Output folder")
                        print("{}_all_uni_perc".format(str(indsn)))
                    except:
                        print("Failed to save the output. Please check your output path!")
                        return False
                else:
                    print ("TR6 numeric details dataset does not exists!.Check the outcopy folder")
                    return False
            else:
                print ("TR3 numeric details dataset does not exists!.Check the outcopy folder")
                return False
        else:
            print ("Input numeric details dataset does not exists!.Check the outcopy folder")
            return False
    else:
        return False
