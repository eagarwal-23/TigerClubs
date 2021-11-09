import pandas
df = pandas.read_excel('sample.xls')

#print the column names
print df.columns

#get the values for a given column
values = df['column_name'].values

#get a data frame with selected columns
FORMAT = ['Col_1', 'Col_2', 'Col_3']
df_selected = df[FORMAT]