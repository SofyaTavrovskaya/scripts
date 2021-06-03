import json
import pandas as pd
import sys

with open(sys.argv[1]) as file_open:
    previous_result = json.load(file_open)
with open(sys.argv[2]) as file_open:
    current_result = json.load(file_open)

# diff = {}
# for current_image, current_package in current_result.items():
#     for previous_image, previous_package in previous_result.items():
#         if current_image in previous_result:
#             for packages in current_package:
#                 if packages in previous_result[previous_image]:
#                     for vuln in previous_result[previous_image][packages]:
#                         if vuln not in previous_result[previous_image][packages]:
#                             print(vuln)

previous = pd.DataFrame.from_dict(previous_result, orient='index') \
    .apply(pd.Series).stack().apply(pd.Series).stack().apply(pd.Series).reset_index()
previous = previous.drop([6, 'level_2'], 1)

current = pd.DataFrame.from_dict(current_result, orient='index') \
    .apply(pd.Series).stack().apply(pd.Series).stack().apply(pd.Series).reset_index()
current = current.drop([6, 'level_2'], 1)

difference = pd.concat([previous, current]).drop_duplicates(keep=False).reset_index()
diff = pd.DataFrame.to_csv(difference, index=False)
print(diff)
