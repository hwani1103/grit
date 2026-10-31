from psat_batch_tools import validate
proof={
'2':{'evidence':'varying document sizes -> registrationBooks efficient','notInferred':['originalWritingPurpose','onlyCopyTypeUsed','manualsMadeFromRegisters','mandatoryOriginalRetention']},
'3':{'victory':'betterWeapons+strongerArmor+trainedFormation','false':'inferiorWeapons','rightFlank':'ownLeft+neighborLeftPersonsRight'},
'4':{'privateDebt':'owner owes manager','businessProfit':'half still paid owner','unprovided':['lossSharing','jointCapital','abilityBasedDuration']},
'5':{'agreements':'subjectToChildWelfareJudicialRestriction','maintenance':'notPrerequisiteToVisitation','postDivorceJointCustody':'possible'},
'6':{'attributedClaims':[1,2],'authorFacts':[3,4],'unprovided':5},
'7':{'corrected':2,'bridge':'fixedWiredComputer -> immobility -> mobileAccess','otherErrors':['reversedImpact','unintroducedCampaign','mistakeTreatedAsTruth','reversedCriticism']},
'8':{'blanks':['핵심 역량 강화','사회적 책임 이행','통합'],'twoPrograms':'premiumPurchase vs skill+finance+quality+sales'},
'9':{'core':'citizenParticipation democratizes authority societywide to solve inequality','workplace':'exampleNotMandatoryFirst'},
'10':{'name':'eyeTrajectoryNotContentLayout','use':'frequentEvenThoughIneffective','origin':'printBeforeDigital'},
'11':{'truth':[True,False,True],'counterexample':{'T':1,'I':3,'E':1,'R':1},'directMeasurement':'RcannotBeDirectlyMeasured'}}
T,I,E,R=1,3,1,1
assert E+R<T+I and T+I+E+R>T+I+E
validate('verbal20',proof,[('2025-03-08',i) for i in range(2,12)])
