Move_log = [[],[]]

out = []

l = len(Move_log)

for i in range(l):
    if i+1 <l:
        if Move_log[i][1] == Move_log[i+1][1]:
            # bacha tady to urcite bude trosku ztracet kvuli tolerancim a pruzeni
            continue # veskere hodnoty jsou koncove souradnice uhlu, tudiz nemusim nic pricitat, jen vynecham tenhle zapis
    out.append(Move_log[i])

print(out)