print('{"type":"FeatureCollection","features":[')
debut = '{"type":"Feature","id":"'
debut2 = '","properties":{"name":"1"},"geometry":{"type":"Polygon","coordinates":[['
nb=1
with open("dis.txt") as file_in:
    lines = ""
    for line in file_in:
        if line.__contains__("#Polygon_0"):
            nb=0
        elif line.__contains__("#Polygon_"):
            nb=line.replace("#Polygon_","").replace("\n","")
            lines=lines[:-1]
            lines+="]]}},"
            print(debut+nb+debut2+lines)
            lines=""
        else:
            [lat, lon] = line.replace("\n","").split(", ")
            lines += "["+lon[0:13]+","+lat[0:13]+"],"
    lines=lines[:-1]
    lines+="]]}}"
    print(debut+str(int(nb)+1)+debut2+lines)
print(']}')