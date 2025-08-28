data = open(r"C:\Users\ABHI\OneDrive\Documents\Desktop\AIAC\LAB 7.4\file.txt","r").readlines()
output = open(r"C:\Users\ABHI\OneDrive\Documents\Desktop\AIAC\LAB 7.4\file.txt","w")

for line in data:
    output.write(line.upper())

print("Processing done")