
# Handle the case when the ticket is a subtask of of another ticket i.e. BAC-182 is a subtask of BAC-170
# In this case the application should create the following branch tree:
#     dev/sprintXX
#        BAC-182___________________________
#             BAC-170____________________________________