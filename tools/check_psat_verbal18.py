from fractions import Fraction
from psat_batch_tools import validate

# Own reconstruction, before comparing the official final key:
# 1 roles/timeline; 2 two performance metrics; 3 structure and social meaning;
# 4 transport vs knowledge cost; 5 multiple codewords for the same letter;
# 6 same criticism reused; 7 internal feeling projected outward;
# 8 necessary but not sufficient; 9 equal space does not guarantee truth;
# 10 equipment's direct and organizational consequences.
proof={
'1':{'answer':2,'chain':['administrative head','some appointed chancellors','senior chancellor chaired'],'wrong':['decision/execution reversed','531 office moved to early period','collective ruling replaced by king alone','later functioning meeting ignored']},
'2':{'answer':4,'shotsPerMinute':{'nonmechanical':6,'crossbow':1},'accuracy':'crossbow higher','unprovided':'crossbow vs hornbow training cost;other units excluded'},
'3':{'answer':3,'evidence':'stage and audience each have dual authority;hierarchy equal','notStated':['natural vs artificial stability ranking','absence in all mixed terrains']},
'4':{'answer':4,'third':['transport cheap','knowledge expensive','geographical separation rises'],'fourth':['knowledge cheap','remote management','offshoring']},
'5':{'answer':3,'letter':'A','alternativeCodes':['tse-nill','wol-la-chee','be-la-sana'],'scope':'encoded spelling length can differ;original English spelling does not change'},
'6':{'answer':5,'sameCriticism':['Catholic icons and rosaries','West African fetish objects'],'scope':'semantic expansion is not replacement;term circulation not adoption of belief'},
'7':{'answer':3,'projection':['internal: I dislike them','external attribution: they dislike me'],'otherTerms':['insufficient ego strength','repression differs from forgetting','reaction formation covers opposite impulse','prevent irreparable damage not immediate recovery']},
'8':{'answer':2,'truthRows':[],'scope':'ritual execution needs wealth but wealth alone can fail;Confucian virtue supports public participation'},
'9':{'answer':5,'counterexample':'equal weight to consensus and skepticism produces confusion','notClaimed':['abandon objectivity','silence until unanimity','withhold all factual judgment']},
'10':{'answer':1,'chain':['heavy plough raises productivity','eight oxen and equipment too costly alone','communal cultivation and animal rearing'],'cultivatedFractions':['1/2','2/3']},
}
codes=proof['5']['alternativeCodes']
assert len({len(s.replace('-','')) for s in codes})>1
for wealth in [False,True]:
 for ritual in [False,True]:
  if ritual and not wealth:continue
  proof['8']['truthRows'].append(dict(wealth=wealth,ritual=ritual))
assert dict(wealth=True,ritual=False) in proof['8']['truthRows']
assert dict(wealth=False,ritual=True) not in proof['8']['truthRows']
assert Fraction(1,2)<Fraction(2,3)
validate('verbal18',proof,[('2026-03-07',n) for n in range(1,11)])
