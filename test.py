import os 
 
for dirpath, dirnames, filenames in os.walk("c:\\"): 
    for filename in filenames:
        if filename.endswith("Brief für Birgit und Stella.rtf"):
            # print (os.path.join(dirpath, filename))
            print(f'{dirpath}\{filename}')