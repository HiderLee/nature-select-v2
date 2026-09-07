"""
스탯제한 관련 Gene
speed 움직이는 속도
cold_resit 추우면 움직임이 둔해짐
hot_resist 더운데 있으면 에너지
poi_resist  독저항
sight  시야
poi  독
제한없는 Gene
size 크기 하고 생명개수
Child_num 한번에 얼마나 자식을생성할지 1~ 
child_energy 얼마나 많은 에너지를 넘겨줄지 1~ 
child_caution 어느정도 에너지를 남길수있어야 자식을 생성할지 0~
child_rel 성장할떄까지 어느정도로 부모를 따라다닐지
shape 모양결정
partiton 스탯제한되있는 능력치의 정도
"""
from setting import MUTE_PER, MUTE_CHANGE
from making_shape import make_shape
from random import randrange, sample, choice
from collections import namedtuple


a_gene = namedtuple("a_gene", ["speed", "cold_res", "hot_res", "poison_res",
                           "sight", "poison", "child_num", "child_energy", "child_caution",
                           "child_rel", "shape"])
a_gene_len = len(a_gene._fields)

class Animal_Gene():
    total = 50 #총스탯
    partition_num = 5  #스탯이 한정된 능력치 의 개수 -1
    def __init__(self, parent=None):
        if parent == None:
            #새로운 유전자 생성
            self.partition = sorted(sample(range(1, self.total), self.partition_num))
            self.gene = a_gene( self.partition[0], *(self.partition[i+1] - self.partition[i] for i in range(self.partition_num-1)), (self.total-self.partition[-1]),
                               child_num=1, child_energy=randrange(100,500), child_caution=randrange(20,50),
                               child_rel=5, shape=((0,0),))
        else:
            #변이확률
            self.partition = parent.partition.copy()
            if randrange(10) >= MUTE_PER:
                #변이안하면 부모랑같음
                self.gene = parent.gene
            else:
                #변이할시 스탯한정 능력치와 그외의 능력치가 하나씩 바뀐다
                #스탯한정능력치변경
                random_num = randrange(0,self.partition_num)
                self.partition[random_num] += choice([-MUTE_CHANGE, MUTE_CHANGE])
                if self.partition[random_num] < 0:
                    self.partition[random_num] = 0
                self.partition.sort()

                #일반 능력치 변경
                new_state_num = randrange(self.partition_num+1, a_gene_len)
                new_state_name = a_gene._fields[new_state_num] 
                #shape경우엔 +1, -1하면안돼므로 따로제외 
                if new_state_name == "shape":
                    new_state = make_shape(parent.gene.shape)
                else: 
                    new_state = parent.gene[new_state_num] + choice([-MUTE_CHANGE, MUTE_CHANGE])
                    if new_state < 0:
                        new_state = 0

            
                new_states = [self.partition[0], *(self.partition[i+1] - self.partition[i] for i in range(self.partition_num-1)), 
                                   (self.total-self.partition[-1])]
                for num in range(self.partition_num+1, a_gene_len):
                    if num == new_state_num:
                        new_states.append(new_state)
                    else:
                        new_states.append(parent.gene[num])
                self.gene = a_gene(*new_states)


    def __getattr__(self, name):
        return getattr(self.gene, name)
    def __repr__(self):
        return repr(self.gene)




p_gene = namedtuple("p_gene", [])
class Plant_Gene:
    pass