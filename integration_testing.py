# importing libraries
import csv 
import json 
import pandas as pd
import datetime

# reading the sample csv file
my_df = pd.read_csv('sample_call_data.csv')

# converting the 'START' and 'END' column time string to datetime object
my_df['START']= pd.to_datetime(my_df['START'], format="%m/%d/%Y %H:%M")
my_df['END']= pd.to_datetime(my_df['END'], format="%m/%d/%Y %H:%M")
# finding the difference between end time and start time in seconds
my_df['duration']= (my_df['END']- my_df['START']).astype('timedelta64[s]')


# formatting the datetime values for 'START' and 'END' column 
my_df['START'] = my_df['START'].dt.strftime('%Y-%m-%dT%H:%M')
my_df['END'] = my_df['END'].dt.strftime('%Y-%m-%dT%H:%M')

# renaming the columns per specifications 
my_df = my_df.rename(columns={"ID":"id","CALL_ID":"call_id","START":"start_time","END":"end_time",\
                          "AGENT_NAME":"agent_name","CUSTOMER_NAME":"customer_name"})

# creating metadata dataframe
metadata = my_df[['USER_AGENT','ADDR','ACW']]
# converting metadata to a dictionary
my_df['metadata']= metadata.to_dict('records')
# final dataframe of all the columns and metadata dictionary
my_df = my_df[['id','call_id','start_time','customer_name','agent_name','end_time','duration','metadata']]

# writting to a text file in json format with new lime delimited
result =my_df.to_json(orient="records")
parsed = json.loads(result)
data = [json.dumps(record) for record in parsed]
with open('output.txt', 'w') as f:
    for i in data:
        f.write(i+'\n')

# printing the summary
summary_df = my_df.groupby('agent_name').sum()
total_duration = summary_df['duration'].sum()
print(f'Total duration: {total_duration}')
summary_df.index.name = None
print(f'Agent duration:\n{summary_df.to_string(header=False)}')





