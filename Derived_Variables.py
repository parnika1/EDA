def dervar_exec(src="", wrk="", oup="", cop="", tnp="", indsn="", resp=""):
    """
    :param src: Path to input folder
    :param wrk: Path to Work folder
    :param oup: Path to Output folder
    :param cop: Path to Outcopy folder
    :param tnp: Path to Temporary folder
    :param indsn: Name of the Input Data frame
    :param resp: Name of the target variable
    :return: Dataframes containing trend variables based on last 3 and 6 month values
    """

    # Check if all the input parameters are properly specified
    if src == "" or wrk == "" or oup == "" or cop == "" or tnp == "" or indsn == "" or resp == "":
        print("INPUT PARAMETERS ARE NOT SPECIFIED PROPERLY IN FUNCTION CALL!")
        return False

    # import sys library for searching the below location for USD package(s)
    import numpy as np
    import pandas as pd
    import sys
    sys.path.insert(1, r'..\.')
    from Libraries.check_path import check_path
    print("CHECK: IF SPECIFIED PATHS ARE VALID")
    check1 = check_path(src, wrk, oup, cop, tnp)
    if check1:
        try:
            # import data dictionary for base variables
            col_dtls = pd.read_pickle(r"{}\{}_clmn_dtls.pkl".format(str(cop), str(indsn)))
            # read input pickle file
            input_df = pd.read_pickle(r"{}\{}.pkl".format(str(src), str(indsn)))
            print(r"{} and {}_clmn_dtls successfully read.".format(str(indsn), str(indsn)))
            print("---------------------------------------------------")
            print("")
        except:
            print(r"Unable to read {} or {}_clmn_dtls Dataframe!".format(str(indsn), str(indsn)))
            return False
    else:
        return False
    #Check if Target is Binary or not
    if len(input_df[resp].unique()) != 2:
        print("TARGET VARIABLE DOES NOT BELONG TO BINARY CLASS!")
        return False

    # Creating 3 months trend variables
    # Preparing list Derived columns from existing columns
    var_list = input_df.filter(regex=r'w*_[0-9]$').columns
    var_list = var_list.str[:-1]
    var_list = var_list.unique()

    input_tr3_df_col = col_dtls[(col_dtls['TREND_3M'] == 'YES') & (col_dtls['BIVAR_TYPE'] == 'NUM')]['BASE_VARNAME'].unique()
    input_tr3_df = pd.DataFrame()
    #Copying KNID and OBSERVATION_DATE and Target as it is
    input_tr3_df['OBSERVATION_DATE'] = input_df['OBSERVATION_DATE']
    input_tr3_df['KNID'] = input_df['KNID']
    input_tr3_df[resp] = input_df[resp]
    #Logic for creating TR3 features
    for x in input_tr3_df_col:
        if x in var_list:
            conditions_notnulland = [
                (input_df[x + '0'].notnull() & input_df[x + '1'].notnull() & input_df[x + '2'].notnull())]
            choices_up = [((input_df[x + '0'] > input_df[x + '1']) & (input_df[x + '1'] > input_df[x + '2']))]
            choices_do = [((input_df[x + '0'] < input_df[x + '1']) & (input_df[x + '1'] < input_df[x + '2']))]
            input_tr3_df['TUP3_' + x[:-1]] = np.select(conditions_notnulland, choices_up, default=np.nan)
            input_tr3_df['TDO3_' + x[:-1]] = np.select(conditions_notnulland, choices_do, default=np.nan)
            input_tr3_df['TMAX3_' + x[:-1]] = np.select(conditions_notnulland, [
                (input_df[[x + '0', x + '1', x + '2']].max(axis=1, skipna=True))], default=np.nan)
            input_tr3_df['TMIN3_' + x[:-1]] = np.select(conditions_notnulland, [
                (input_df[[x + '0', x + '1', x + '2']].min(axis=1, skipna=True))], default=np.nan)
            input_tr3_df['TAVG3_' + x[:-1]] = np.select(conditions_notnulland, [
                (input_df[[x + '0', x + '1', x + '2']].mean(axis=1, skipna=True))], default=np.nan)
            input_tr3_df['TSTD3_' + x[:-1]] = np.select(conditions_notnulland, [
                (input_df[[x + '0', x + '1', x + '2']].std(axis=1, skipna=True))], default=np.nan)

            condition_nonzero = [(input_tr3_df['TAVG3_' + x[:-1]] != 0) & (input_tr3_df['TAVG3_' + x[:-1]].notnull())]
            input_tr3_df['TCFV3_' + x[:-1]] = np.select(condition_nonzero, [
                (input_tr3_df['TSTD3_' + x[:-1]] / input_tr3_df['TAVG3_' + x[:-1]]).abs()], default=np.nan)
            input_tr3_df['TVOL3_' + x[:-1]] = np.select(condition_nonzero, [((input_tr3_df['TMAX3_' + x[:-1]] -
                                                                              input_tr3_df['TMIN3_' + x[:-1]]) /
                                                                             input_tr3_df['TAVG3_' + x[:-1]]).abs()],
                                                        default=np.nan)

            condition_nonzero1 = [(input_df[x + '1'].notnull() & input_df[x + '1'] != 0)]
            condition_nonzero2 = [(input_df[x + '2'].notnull() & input_df[x + '2'] != 0)]
            condition_nonzero3 = [(input_df[x + '3'].notnull() & input_df[x + '3'] != 0)]
            input_tr3_df['TR1_' + x[:-1]] = np.select(condition_nonzero1, [
                ((input_df[x + '0'] - input_df[x + '1']) / input_df[x + '1'].abs())], default=np.nan)
            input_tr3_df['TR2_' + x[:-1]] = np.select(condition_nonzero2, [
                ((input_df[x + '0'] - input_df[x + '2']) / input_df[x + '2'].abs())], default=np.nan)
            input_tr3_df['TR3_' + x[:-1]] = np.select(condition_nonzero3, [
                ((input_df[x + '0'] - input_df[x + '3']) / input_df[x + '3'].abs())], default=np.nan)
    
    #Checking if all of expected derived features are present
    # "3" is specified for KNID,OBSERVATION_DATE and Target variable
    if len(input_tr3_df.columns) - 3 == len(set(list(var_list)).intersection(set(list(input_tr3_df_col)))) * 11:
        print("Number of base vars for which 3M trend variables are created: ",
              str(len(set(list(var_list)).intersection(set(list(input_tr3_df_col))))))
        print("Number of 3M trend variables are created: ", str(len(input_tr3_df.columns) - 3))
        print("")
    else:
        print("Error in creating 3M lag variables. Please check the above code ")
        return False

    # Creating 6 months trend variables
    input_tr6_df_col = col_dtls[(col_dtls['TREND_6M'] == 'YES') & (col_dtls['BIVAR_TYPE'] == 'NUM')][
        'BASE_VARNAME'].unique()
    #Copying KNID and OBSERVATION_DATE and Target as it is
    input_tr6_df = pd.DataFrame()
    input_tr6_df['OBSERVATION_DATE'] = input_df['OBSERVATION_DATE']
    input_tr6_df['KNID'] = input_df['KNID']
    input_tr6_df[resp] = input_df[resp]
    #Logic for creating TR3 features
    for x in input_tr6_df_col:
        if x in var_list:
            conditions_notnulland = [(input_df[x + '0'].notnull() & input_df[x + '1'].notnull() & input_df[
                x + '2'].notnull() & input_df[x + '3'].notnull() & input_df[x + '4'].notnull() & input_df[
                                          x + '5'].notnull())]
            choices_up = [((input_df[x + '0'] > input_df[x + '1']) & (input_df[x + '1'] > input_df[x + '2']) & (
            input_df[x + '2'] > input_df[x + '3']) & (input_df[x + '3'] > input_df[x + '4']) & (
                           input_df[x + '4'] > input_df[x + '5']))]
            choices_do = [((input_df[x + '0'] < input_df[x + '1']) & (input_df[x + '1'] < input_df[x + '2']) & (
            input_df[x + '2'] < input_df[x + '3']) & (input_df[x + '3'] < input_df[x + '4']) & (
                           input_df[x + '4'] < input_df[x + '5']))]
            input_tr6_df['TUP6_' + x[:-1]] = np.select(conditions_notnulland, choices_up, default=np.nan)
            input_tr6_df['TDO6_' + x[:-1]] = np.select(conditions_notnulland, choices_do, default=np.nan)
            input_tr6_df['TMAX6_' + x[:-1]] = np.select(conditions_notnulland, [
                input_df[[x + '0', x + '1', x + '2', x + '3', x + '4', x + '5']].max(axis=1, skipna=True)],
                                                        default=np.nan)
            input_tr6_df['TMIN6_' + x[:-1]] = np.select(conditions_notnulland, [
                input_df[[x + '0', x + '1', x + '2', x + '3', x + '4', x + '5']].min(axis=1, skipna=True)],
                                                        default=np.nan)
            input_tr6_df['TAVG6_' + x[:-1]] = np.select(conditions_notnulland, [
                input_df[[x + '0', x + '1', x + '2', x + '3', x + '4', x + '5']].mean(axis=1, skipna=True)],
                                                        default=np.nan)
            input_tr6_df['TSTD6_' + x[:-1]] = np.select(conditions_notnulland, [
                input_df[[x + '0', x + '1', x + '2', x + '3', x + '4', x + '5']].std(axis=1, skipna=True)],
                                                        default=np.nan)

            condition_nonzero = [(input_tr6_df['TAVG6_' + x[:-1]] != 0) & (input_tr6_df['TAVG6_' + x[:-1]].notnull())]
            input_tr6_df['TCFV6_' + x[:-1]] = np.select(condition_nonzero, [
                (input_tr6_df['TSTD6_' + x[:-1]] / input_tr6_df['TAVG6_' + x[:-1]]).abs()], default=np.nan)
            input_tr6_df['TVOL6_' + x[:-1]] = np.select(condition_nonzero, [((input_tr6_df['TMAX6_' + x[:-1]] -
                                                                              input_tr6_df['TMIN6_' + x[:-1]]) /
                                                                             input_tr6_df['TAVG6_' + x[:-1]]).abs()],
                                                        default=np.nan)

            condition_nonzero1 = [(input_df[x + '4'].notnull() & input_df[x + '4'] != 0)]
            condition_nonzero2 = [(input_df[x + '5'].notnull() & input_df[x + '5'] != 0)]
            condition_nonzero3 = [(input_df[x + '6'].notnull() & input_df[x + '6'] != 0)]
            input_tr6_df['TR4_' + x[:-1]] = np.select(condition_nonzero1, [
                ((input_df[x + '0'] - input_df[x + '4']) / input_df[x + '4'].abs())], default=np.nan)
            input_tr6_df['TR5_' + x[:-1]] = np.select(condition_nonzero2, [
                ((input_df[x + '0'] - input_df[x + '5']) / input_df[x + '5'].abs())], default=np.nan)
            input_tr6_df['TR6_' + x[:-1]] = np.select(condition_nonzero3, [
                ((input_df[x + '0'] - input_df[x + '6']) / input_df[x + '6'].abs())], default=np.nan)
    #Checking if all of expected derived features are present
    # "3" is specified for KNID,OBSERVATION_DATE and Target variable
    if len(input_tr6_df.columns) - 3 == len(set(list(var_list)).intersection(set(list(input_tr6_df_col)))) * 11:
        print("Number of base vars for which 6M trend variables are created: ",
              str(len(set(list(var_list)).intersection(set(list(input_tr6_df_col))))))
        print("Number of 6M trend variables are created: ", str(len(input_tr6_df.columns) - 3))
        print("")
    else:
        print("Error in creating 6M lag variables. Please check the above code ")
        return False

    # Saving Output
    try:
        input_tr3_df.to_pickle(r"{}\{}_tr3.pkl".format(str(wrk), str(indsn)))
        input_tr6_df.to_pickle(r"{}\{}_tr6.pkl".format(str(wrk), str(indsn)))
        print("Following output files successfully saved in Work folder")
        print("{}_tr3".format(str(indsn)))
        print("{}_tr6".format(str(indsn)))
    except:
        print("Failed to save the output. Please check your output path!")
        return False
