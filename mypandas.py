import pandas as pd
import re


"""
Convert a list of html files into a dictionary of dataframes with key extracted from html files
# Example use :
#           pattern_for_key = ".*power_analysis\/local_(.*)?\/.*"
#           list_of_htmls   = power_htmls[:track_till]
#           index_col       = 'Vector'
#           
#           frames = html_paths_to_dataframe_dictionary(pattern_for_key, list_of_htmls, index_col)
#           frames.keys()
"""
def html_paths_to_dataframe_dictionary(pattern_for_key, list_of_htmls, index_col):
    frames = {}
    #extract_tag = re.compile(".*power_analysis\/local_(.*)?\/.*")
    extract_tag = re.compile(pattern_for_key)
    #for i,p in enumerate(power_htmls[:track_till]):
    for i,p in enumerate(list_of_htmls):
        match = re.match(extract_tag,p)
        if match:
            df = pd.read_html(p, header=0, index_col=index_col)
            frames[match[1]]= df 
    return frames

"""
Concat a dictionary containing similar DataFrames to one single DataFrame 
"""
def concat_dict_of_dfs_to_single_df(dfdict):
    dflist = [dfdict[list(dfdict.keys())[i]][0] for i in range(len(dfdict))]
    df = pd.concat(dflist,axis=1);
    return df
    
"""
Transpose Dataframe, replicate Tags to create a column, add it as first
"""
def create_col_from_dict_to_add_as_first(df,dfdict,repetitions,col_name):
    duplicated_keys =  [[i]*repetitions for i in list(dfdict.keys())] 
    flatten_keys = [item for sublist in duplicated_keys for item in sublist]
    df['Tag'] = pd.Series(flatten_keys).values; 
    cols = df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    return df[cols]
