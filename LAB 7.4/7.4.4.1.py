def compute_ratios(values):
    results = [ ]
    for i in range(len(values)):
        for j in range(len(values)):
            if i != j and (values[j]-values[i])!=0:
                ratio=values[i] / (values[j]-values[i])
                results.append((i,j,ratio))
                return results
nums=[5,10,15,20,25]
print(compute_ratios(nums))
               