from newf import vf2
from find_q_functions import get_qs,get_embeddings
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
    tmp = vf2(source, target, δ)
    for item in tmp:
        if item not in result_set:
            result_set.add(item)
            result.append(item)
            inc += 1
            if len(result) >= k:
                break
    δ += 2
    # if inc <= k/10:
    #     δ += 2
    #     time += 1   
    #     if time > 2:
    #         δ += 2
    # else:
    #     δ += 1
    #     time = 0

print(result)
qs = get_qs(source,result)
emb = get_embeddings(qs,target)
print(emb)
