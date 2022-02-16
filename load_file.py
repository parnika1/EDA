def load_pickle(folder="",file=""):
    
    #import necessary libraries
    import pandas as pd
    
    try:
        return pd.read_pickle(r"{}\{}".format(str(folder),str(file)))         
    except:
        print(r"Unable to load {} from {}!".format(str(file),str(folder)))
        return False
    
    
def load_excel(folder="",file=""):
    
    #import necessary libraries
    import pandas as pd
    
    try:
        return pd.read_pickle(r"{}\{}".format(str(folder),str(file)))         
    except:
        print(r"Unable to load {} from {}!".format(str(file),str(folder)))
        return False
