import pyactr as actr

model = actr.ACTRModel()
actr.chunktype("type", ("type", "term"))
actr.chunktype("expressiontype", ("term1type", "term2type","term3type","expressiontype"))
actr.chunktype("expression", ("term1", "term2","term3","type1","type2","type3"))
actr.chunktype("evaluation",("evaluate"))
dm = model.decmem

for i in range(999):
	dm.add(actr.chunkstring(string="""
    isa type
    type natural_number
    term {}
    """.format(i)))

dm.add(actr.chunkstring(string="""
    isa type
    type operator
    term minus
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type operator
    term plus
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type operator
    term divided
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type operator
    term times
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type boolean
    term true
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type boolean
    term false
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type booloperator
    term greateq
    """))
dm.add(actr.chunkstring(string="""
    isa type
    type booloperator
    term lesseq
    """))
dm.add(actr.chunkstring(string="""
    isa expressiontype
    term1type natural_number
    term2type operator
    term3type natural_number
    expressiontype natural_number
    """))
dm.add(actr.chunkstring(string="""
    isa expressiontype
    term1type int
    term2type booloperator
    term3type natural_number
    expressiontype boolean
    """))
g = model.goal
imaginal = model.set_goal(name="imaginal", delay=0.2)
imaginal.add(actr.chunkstring(string="""
    isa expression
    term1 5
    term2 plus
    term3 2
"""))


g.add(actr.chunkstring(string="""
    isa evaluation
    evaluate term1
"""))
model.productionstring(name="evaluate term1", string="""
    =g>
    isa evaluation
    evaluate term1
    =imaginal>
    isa expression
    term1 = t1
    ==>
    =g>
    isa evaluation
    evaluate term2
    +retrieval>
    isa type
    term = t1
    """)

model.productionstring(name="evaluate term2", string="""
    =g>
    isa evaluation
    evaluate term2
    =imaginal>
    isa expression
    term2 = t2
    =retrieval>
    isa type
    term = t1
    type = ty1
    ==>
    =g>
    isa     evaluation
    evaluate term3
    =imaginal>
    isa expression
    type1 = ty1
    +retrieval>
    isa     type
    term      = t2 """)
model.productionstring(name="evaluate term3", string="""
    =g>
    isa evaluation
    evaluate term3
    =imaginal>
    isa expression
    term3 = t3
    =retrieval>
    isa type
    term = t2
    type = ty2
    ==>
    =g>
    isa evaluation
    evaluate expression
    =imaginal>
    isa expression
    type2 = ty2
    +retrieval>
    isa     type
    term      = t3
  """)
model.productionstring(name="evaluate expression", string="""
    =g>
    isa evaluation
    evaluate expression
    =retrieval>
    isa type
    term = t3
    type =ty3
    =imaginal>
    isa expression
    term1 =t1
    term2 = t2
    type1 = ty1
	type2 = ty2
    ==>
    =g>
    isa  evaluation
    evaluate type
    =imaginal>
    isa expression
    type3 = ty3
    """)
model.productionstring(name="evaluate type", string="""
    =g>
    isa evaluation
    evaluate type
    =imaginal>
    isa expression
    type1 = ty1
	type2 = ty2
	type3 = ty3
    ==>
    +retrieval>
    isa  expressiontype
    term1type = ty1
    term2type = ty3
    term3type = ty2
    ~imaginal>
    ~g>
    """)
# The values of ty3 and ty2 alternate at the end
if __name__ == "__main__":
    x = model.simulation()
    x.run()
