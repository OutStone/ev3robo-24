angles = [[],[]]

out = []

l = len(angles)

for i in range(l):
    if i+1 <l:
        if angles[i][1] == angles[i+1][1]:
            # bacha tady to urcite bude trosku ztracet kvuli tolerancim a pruzeni
            continue # veskere hodnoty jsou koncove souradnice uhlu, tudiz nemusim nic pricitat, jen vynecham tenhle zapis
    out.append(angles[i])

print(out)