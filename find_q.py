from newf import vf2_emb

source = 'graphdata/pubchem_no_H.txt'
target = 'graphdata/demoquery.txt'
δ = 1
k = 10


result = []
result_set = set()
time = 0

while len(result) < k:
    inc = 0
    print(δ, inc,time)
    tmp = vf2_emb(source, target, δ)
    for item in tmp[1]:
        if item not in result_set:
            result_set.add(item)
            result.append(item)
            inc += 1
            if len(result) >= k:
                break
    if inc <= k/10:
        δ += 2
        time += 1   
        if time >= 2:
            δ += 2
    else:
        δ += 1
        time = 0

print(result)
