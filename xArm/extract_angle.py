#!/usr/bin/env python3
import re

with open('testpath.txt', 'r') as file:
    data = file.read()
    pattern = r'positions:\s*(\[.*?\])'
    matches = re.findall(pattern, data)

    result_text = '\n'.join(match.replace(']', ']') for match in matches)

    # save
    with open('testpath_R.txt', 'w') as result_file:
        result_file.write(result_text)

    print("Results saved to testpath_result.txt")
