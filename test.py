
dicta = [
    {'unoaaaaaaaaaaaaaaaaaaaaaaa': 'xdcxdxd', 'dos': 'adsfasdf', 'tres': '123123312'},
    {'unoaaaaaaaaaaaaaaaaaaaaaaa': 'asdfasd', 'dos': 'adsaaaaafasdf', 'tres': '3312'}
]

lengths = []

for k in dicta[0].keys():
    allvals = [d[k] for d in dicta]
    allvals.append(k)
    lengths.append(len(max(allvals, key=len)))

print(lengths)