import time

string_list = [(str(i)+"fuck") for i in range(24)]  # List of strings "0" to "23"
int_list = list(range(24))  # List of integers 0 to 23

target_string = "23"
target_int = 23

# Measure time for string search
start_time = time.time()
if target_string in string_list:
    pass
end_time = time.time()
string_search_time = end_time - start_time

# Measure time for integer search
start_time = time.time()
if target_int in int_list:
    pass
end_time = time.time()
int_search_time = end_time - start_time

print(f"Time taken for string search: {string_search_time:.10f} seconds")
print(f"Time taken for integer search: {int_search_time:.10f} seconds")
