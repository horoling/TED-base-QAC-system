from newf import vf2

source = 'graphdata/pubchem_no_H.txt'
target = 'graphdata/demoquery.txt'
δ = 1
k = 10


result = []
result_set = set()

while len(result) < k:
    tmp = vf2(source, target, δ)
    for item in tmp:
        if item not in result_set:
            result_set.add(item)
            result.append(item)
            if len(result) >= k:
                break
    δ += 1

print(result)