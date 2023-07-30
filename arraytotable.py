def itemdisplay(array):
        arr = [[array[j][i] for i in range(len(array[0]))] for j in range(len(array))]  #inspired a lot from stackoverflow.
        #arr = array behaves as a pointer and so arr is edited and applies that data to array, 
        # thereby editing the original array, messing up the format and text. 
        # this line is a double for loop that copies the original array into arr, without impacting the original array.
        titles = ['Code','Description','Category','Unit','Price','Quantity','Minimum']
        arr.insert(0,titles)
        maximums = []
        #step 1
        for col in range(7):
            max = 0
            for row in arr:
                if len(row[col]) > max:
                    max = len(row[col])
            maximums.append(max)
        # print(maximums)
        # step 2
        for col in range(7):
            for row in arr:
                if len(row[col]) < maximums[col]:
                    # print("found less")
                    remainder = maximums[col] - len(row[col])
                    # print(f"it needs {remainder} spaces")
                    for i in range(remainder):
                        row[col] += " "
        # step 3
        liner = "\n"
        for i in range(sum(maximums)+7):
            liner += "_"
        print(liner,end='')
        for record in arr:
            for cell in record:
                if arr.index(record) == 1 and record.index(cell) == 0:
                    print(liner)
                    print(f"{cell}",end="|")
                else:
                    if record.index(cell) == 0:
                        print(f"\n{cell}",end="|")
                    else:
                        print(cell,end="|")
        print("\n")
        del arr