import review_remaining605 as r
b=r.folder(49)
rows=[(5,'직은내가점유한직장자리에서담당하는대체가능한일이고업은평생삶과떼지못하는가치있는일이다.먼저자기적성과가치를탐색하고업을파악해야좋은직도보람있다는흐름이므로끝의직이해도부족을업파악못함으로바꾸는⑤가맞다.㉠직탐색으로바꾸면순서역전,㉡영향력범위는직정의아님,㉢경쟁역량은업가치왜곡,㉣자리우선은본문의일우선에반대다.', ['자기적성과원하는일을찾는대목을직자리탐색으로바꾸면업우선논지를거스른다.','직은직장내자리에서맡는일이지영향력과그범위라는정의가아니다.','업은평생추구하는가치있는일이며타인경쟁에서이길역량이아니다.','자리보다먼저추구할일을찾아야한다는주장을자리우선으로바꾸므로틀리다.','마지막직이해를업파악으로고치면자신의가치있는일을먼저찾으라는논지와일치한다.']),
(1,'첫실험은−11에서온도를높이는도중양전하로바뀌고더올라간−8에서A만결빙한다.따라서온도가올라가는상황에서도결빙가능하다.음→양전환기준T는−11보다높고−8보다낮으므로두번째실험−7에서는양전하이다.A는−7에서,B는−12.5에서얼어양전하A가덜냉각해도얼므로양전하가촉진한다.올라감/양/양①.실내최종−5와부품결빙−8을구별한다.', ['가열중결빙반례로올라감도가능하고−7은전환온도보다높아양전하이며더높은결빙온도로촉진이다.','양전하A가중성B보다높은온도에서얼었으므로촉진전하를음으로쓸수없다.','−8에서이미양전하이므로더높은−7에서음전하일수없고촉진도양전하다.','온도를올리는첫실험에서도결빙했으므로내려가는상황에서만이라는말은틀리다.','가열중결빙을부정하는가와−7의음전하인나가모두실험과어긋난다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print(q.get('underlines'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
