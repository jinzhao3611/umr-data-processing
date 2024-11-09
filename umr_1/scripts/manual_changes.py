import re
def manual_fix_english(text):
    edge_cases = ["""(s16c :same-entity s17v2)
            """, """
  :temporal ((s16d :overlap s17h))""", """:temporal (())
    ""","""
            (AUTH :FullAff )""",  """
          (AUTH :FullAff s17h)""", """
  :coref ((s28e3 :same-event s30c))""", """
  :temporal ((s40c :before s40l))"""]
    for e in edge_cases:
        text = text.replace(e, "")

    edge_cases_replace = [("""(s17s0 / sentence
  :temporal ((s16d :overlap s17h))
  :modal ((ROOT :MODAL AUTH)
          (AUTH :FullAff s17h))
  :coref ((s16b :same-entity s17b)
	  (s16p2 :same-entity s17t))""", """(s17s0 / sentence
  :temporal ((s16d :overlap s17h))
  :modal ((ROOT :MODAL AUTH)
          (AUTH :FullAff s17h))
  :coref ((s16b :same-entity s17b)
	  (s16p2 :same-entity s17t)))"""),("""(s22s0 / sentence
  :temporal ((s21w :after s22p)
          (s22p :overlap s22f))
  :modal ((ROOT :MODAL AUTH)
          (AUTH :FullAff s22f)
          (AUTH :FullAff s22p))
  :coref ((s21p :same-entity s22p2)
          (s21t :same-entity s22t)
          (s17b :same-entity s22b)
	  (s18p2 :same-entity s22t2))""", """(s22s0 / sentence
  :temporal ((s21w :after s22p)
          (s22p :overlap s22f))
  :modal ((ROOT :MODAL AUTH)
          (AUTH :FullAff s22f)
          (AUTH :FullAff s22p))
  :coref ((s21p :same-entity s22p2)
          (s21t :same-entity s22t)
          (s17b :same-entity s22b)
	  (s18p2 :same-entity s22t2)))"""), ("""((39k""", """((s39k"""), ("""(s39p :same-event :s40d)))""", """(s39p :same-event s40d)))"""), ("""(s32s0 / sentence
  :temporal ((s30c :overlap s32l))
  :modal ((ROOT :MODAL AUTH)
          (AUTH :PrtAff s32t)
	  (AUTH :FullNeg s32l)
  :coref ((s31p :same-entity s32p)
          (s31p2 :same-entity s32p2)
	  (s14p :same-entity s32p3))""", """(s32s0 / sentence
  :temporal ((s30c :overlap s32l))
  :modal ((ROOT :MODAL AUTH)
          (AUTH :PrtAff s32t)
	  (AUTH :FullNeg s32l))
  :coref ((s31p :same-entity s32p)
          (s31p2 :same-entity s32p2)
	  (s14p :same-entity s32p3)))
"""), (""":: snt2  TACLOBAN , Philippines , Feb 17 , 2006 .""", """:: snt2\t  TACLOBAN , Philippines , Feb 17 , 2006 ."""), ("""(s9s0/ sentence""", """(s9s0 / sentence"""), ("""(s8s0/ sentence""", """(s8s0 / sentence"""), ("""(s16p2 :same-entity s17t))""", """(s16p2 :same-entity s17t)))"""), ("""s95w: 4,7""", """s95w: 4-7"""), ("""s96p: 2,4""", """s96p: 2-4"""), ("""s98g: 5,8""", """s98g: 5-8"""), ("""s4b: 7,9""", """s4b: 7-9"""), ("""s8o: 21""", """s8o: 21-21"""), ("""s16d: 12,15""", """s16d: 12-15"""), ("""s16u: 27,31""", """s16u: 27-31""")]
    for old, new in edge_cases_replace:
        text = text.replace(old, new)
    return text
def manual_fix_arapaho(text):
    edge_cases = ["""(s99 / sentence
    :coref ()
    :temporal ((DCT)
               (PAST_REF)
               (PRESENT_REF)
               (FUTURE_REF))
    :modal ())""", """
            (s8t :before s6t)""", """
            (s3h :same-entity s4p2)"""]

    for e in edge_cases:
        text = text.replace(e, "")

    edge_cases_replace = [("""(s3h3 / have-goal-91
    :ARG1 s3p 
    :ARG2 (s3h2 / human-settlement :wiki "Shoshoni,_Wyoming"
        :name (s3n2 / name :op1 "sosoni'")
        :mod (s3h4 / hinee)))
    :purpose (s3n / niistoo-00
        :actor (s3p / person
            :refer-person 3rd
            :refer-number Singular)
        :Aspect Activity
        :MODSTR PrtAff)
    :Aspect Activity
    :MODSTR FullAff""","""(s3h3 / have-goal-91
    :ARG1 s3p 
    :ARG2 (s3h2 / human-settlement :wiki "Shoshoni,_Wyoming"
        :name (s3n2 / name :op1 "sosoni'")
        :mod (s3h4 / hinee))
    :purpose (s3n / niistoo-00
        :actor (s3p / person
            :refer-person 3rd
            :refer-number Singular)
        :Aspect Activity
        :MODSTR PrtAff)
    :Aspect Activity
    :MODSTR FullAff)""")]
    for old, new in edge_cases_replace:
        text = text.replace(old, new)
    return text
def manual_fix_chinese(text):
    text = re.sub(r"(# :: snt\d+	)(Sentence: )", r"\1", text)  # make the sentence format consistent

    edge_cases = ["""(s23i4 :same-entity s24x4)

                    """]
    edge_cases_replace = [(""":temporal (s4x3 / 目前)
          :mod (s4x4 / 已经)
          :Aspect Aspect
          :MODSTR FullAff)""", """:temporal (s4x3 / 目前)
          :mod (s4x4 / 已经)
          :Aspect Performance
          :MODSTR FullAff)"""), (""":ARG1 (sa2 / and""", """:ARG1 (s14a2 / and"""), (""":op2 (sx3 / 评选-01""", """:op2 (s38x / 评选-01"""), ("""sx3: 20-20""", """s38x: 20-20"""), (""":ARG0 (sm / magazine""", """:ARG0 (s38m / magazine"""), ("""sm: 17-18""", """s38m: 17-18"""), (""":name (sn3 / name""", """:name (s38n4 / name"""), ("""sn3: -1--1""","""s38n4: -1--1"""), ("""(s1a / and
  :op1 (s1i5 / identity-91
         :ARG1 (s1i3 / individual-person
                 :name (s1n4 / name
                         :op1 "于海"))
         :ARG2 (s1x11 / 人
                 :place (s1c2 / city
                          :name (s1n3 / name
                                  :op1 "日照")
                          :place (s1p / province
                                   :name (s1n2 / name
                                           :op1 "山东"))))
         :Aspect State
         :MODSTR FullAff""", """(s1a / and
  :op1 (s1i5 / identity-91
         :ARG1 (s1i3 / individual-person
                 :name (s1n4 / name
                         :op1 "于海"))
         :ARG2 (s1x11 / 人
                 :place (s1c2 / city
                          :name (s1n3 / name
                                  :op1 "日照")
                          :place (s1p / province
                                   :name (s1n2 / name
                                           :op1 "山东"))))
         :Aspect State
         :MODSTR FullAff)"""), ("""(S10x13 :before s10x8)""", """(s10x13 :before s10x8)""")]
    for e in edge_cases:
        text = text.replace(e, "")
    for old, new in edge_cases_replace:
        text = text.replace(old, new)
    return text
def manual_fix_kukama(text):
    edge_cases = ["""
                    (s18t :after "MISSING-VALUE")""", """
                    (s13p :PrtAff "MISSING-VALUE")""", """
                    (s47p :PrtAff "MISSING-VALUE")
""", """
                    (s32e :before "MISSING-VALUE")""", """
                    (s41k :before "MISSING-VALUE")""", """
                    (s52e :before "MISSING-VALUE")""", """
                    (s53e :before "MISSING-VALUE")""", """
                    (s60e :before "MISSING-VALUE")""", """
                    (s63u :same-event s)""", """
                    (s :FullAff s55p3)""", """(s32e :overlap :32e2)""", """

                    (s55 :FullAff s55p3)
""", """
                    (s13p :PrtAff "MISSING-VALUE")""","""
                    (s47p :PrtAff "MISSING-VALUE")""","""
                    (s18t :after "MISSING-VALUE")""", """
                    (s32e :before "MISSING-VALUE")""", """
                    (s41k :before "MISSING-VALUE")""", """
                    (s52e :before "MISSING-VALUE")""", """
                    (s53e :before "MISSING-VALUE")""", """
                    (s60e :before "MISSING-VALUE")""", """
# :: snt59
Words                     era  ipirawira       ipu         peka
Morphemes                 era  ipirawira       ipu       pe -ka
Morpheme Gloss(English)  well    dolphin  to.sound    port -LOC
Morpheme Gloss(Spanish)  bien     delfín     sonar  puerto -LOC
English Sent Gloss: the dolphin sounds hard in the port
Spanish Sent Glossel bufeo suena fuerte en el puerto

# sentence level graph:



# alignment:

# document level annotation:
"""
]

    for e in edge_cases:
        text = text.replace(e, "")

    edge_case2 = """  :theme (s9m / mamaaa,-mamaaa)
"""
    edge_case2_replace = """  :theme (s9m / mamaaa-mamaaa))
"""

    edge_case12 = """(s56s0 / sentence

  :temporal ((s56e :before s56m)

  :coref ((s55e :same-event s56e)

                    (s55e2 :same-event s56m)))"""
    edge_case12_replace = """(s56s0 / sentence

  :temporal ((s56e :before s56m))

  :coref ((s55e :same-event s56e)

                    (s55e2 :same-event s56m)))
"""

    edge_case16 = """(s2s0 / sentence

  :temporal ((Past_ref / Past_ref :Contained s2m))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullNeg s2m))

  :coref ((s1p :same-entity s2p2))"""

    edge_case16_replace = """(s2s0 / sentence

  :temporal ((Past_ref / Past_ref :Contained s2m))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullNeg s2m))

  :coref ((s1p :same-entity s2p2)))"""
    edge_case17 = """(s16s0 / sentence

  :temporal ((s15t :overlap s16t)

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s16t))

  :coref ((s15p :same-entity s16p)))"""
    edge_case17_replace = """(s16s0 / sentence

  :temporal ((s15t :overlap s16t))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s16t))

  :coref ((s15p :same-entity s16p)))"""
    edge_case18 = """(s8s0 / sentence

  :temporal ((s7u :after s8t)

                    (s8t :before s8x))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s8x)

                    (AUTH :FullAff s8t))

  :coref (s8p :subset-of s2p)"""
    edge_case18_replace = """(s8s0 / sentence

  :temporal ((s7u :after s8t)

                    (s8t :before s8x))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s8x)

                    (AUTH :FullAff s8t))

  :coref ((s8p :subset-of s2p)))"""
    edge_case19 = """(s12s0 / sentence

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s12h))

  :coref (s4p :same-entity s12p)))"""
    edge_case19_replace = """(s12s0 / sentence

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s12h))

  :coref ((s4p :same-entity s12p)))"""
    edge_case20 = """(s13s0 / sentence

  :temporal ((s12h :overlap s13u)

                    (s13u :after s13t))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s13u))

                    (AUTH :FullAff s13p)

                    (s13p :PrtAff purpose)

                    (purpose :FullAff s13t))

  :coref ((s12p :same-entity s13p))

                    (s12k :same-entity s13y2)))"""
    edge_case20_replace = """(s13s0 / sentence

  :temporal ((s12h :overlap s13u)

                    (s13u :after s13t))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s13u)

                    (AUTH :FullAff s13p)

                    (s13p :PrtAff purpose)

                    (purpose :FullAff s13t))

  :coref ((s12p :same-entity s13p)

                    (s12k :same-entity s13y2)))"""
    edge_case21 = """(s14s0 / sentence

  :temporal ((s11t :overlap s14t)

                    (s14k3 :overlap s14t3))

  :modal ((ROOT :modal AUTH)

                    (AUTH :FullAff s14t)

                    (AUTH :FullAff s14p)

                    (AUTH :FullAff s14k3)

                    (s14p :FullAff s14t3))

  :coref ((s14t :subset-of s14k3))

                    (s10p :same-entity s14p)

                    (s11p :same-entity s14p2)

		    (s6p :same-entity s14k)))"""
    edge_case21_replace = """(s14s0 / sentence

  :temporal ((s11t :overlap s14t)

                    (s14k3 :overlap s14t3))

  :modal ((ROOT :modal AUTH)

                    (AUTH :FullAff s14t)

                    (AUTH :FullAff s14p)

                    (AUTH :FullAff s14k3)

                    (s14p :FullAff s14t3))

  :coref ((s14t :subset-of s14k3)

                    (s10p :same-entity s14p)

                    (s11p :same-entity s14p2)

		    (s6p :same-entity s14k)))"""
    edge_case22 = """(s23s0 / sentence

  :temporal ((s22u :overlap s24u))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s24u))

  :coref ((s22p :same-entity s23p

                    (s13p :same-entity s23p)))"""
    edge_case22_replace = """(s23s0 / sentence

  :temporal ((s22u :overlap s24u))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s24u))

  :coref ((s22p :same-entity s23p)

                    (s13p :same-entity s23p)))"""
    edge_case23 = """(s34s0 / sentence

  :temporal ((s33u :after s34u)

                    (s34u :overlap s34i2))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s34p)

                    (s34p :FullAff s34u)

                    (s34u :Unsp s34i2))

  :coref ((s33p :same-entity s34p)

                    (s32p3 :same-entity s34p2))"""
    edge_case23_replace = """(s34s0 / sentence

  :temporal ((s33u :after s34u)

                    (s34u :overlap s34i2))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s34p)

                    (s34p :FullAff s34u)

                    (s34u :Unsp s34i2))

  :coref ((s33p :same-entity s34p)

                    (s32p3 :same-entity s34p2)))
"""
    edge_case24 = """(s35s0 / sentence

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s35i2))

  :coref ((s34i2 :same-event s35i2)

                    (s34i3 :same-entity s35i3)

                    (s34p2 :same-entity s35p))"""
    edge_case24_replace = """(s35s0 / sentence

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s35i2))

  :coref ((s34i2 :same-event s35i2)

                    (s34i3 :same-entity s35i3)

                    (s34p2 :same-entity s35p)))"""
    edge_case25 = """(s42s0 / sentence

  :temporal ((s42e :overlap s42h))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s42e)

                    (AUTH :FullAff s42p)

                    (s42p :FullAff s42h))

  :coref ((s41k :same-event s42e)

                    (s41p :same-entity s42p)

                    (s41p2 :same-entity s42p4)

                    (s40p2 :same-entity s42p3))"""
    edge_case25_replace = """(s42s0 / sentence

  :temporal ((s42e :overlap s42h))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s42e)

                    (AUTH :FullAff s42p)

                    (s42p :FullAff s42h))

  :coref ((s41k :same-event s42e)

                    (s41p :same-entity s42p)

                    (s41p2 :same-entity s42p4)

                    (s40p2 :same-entity s42p3)))
"""
    text = text.replace(edge_case2, edge_case2_replace)
    text = text.replace(edge_case12, edge_case12_replace)
    text = text.replace(edge_case16, edge_case16_replace)
    text = text.replace(edge_case17, edge_case17_replace)
    text = text.replace(edge_case18, edge_case18_replace)
    text = text.replace(edge_case19, edge_case19_replace)
    text = text.replace(edge_case20, edge_case20_replace)
    text = text.replace(edge_case21, edge_case21_replace)
    text = text.replace(edge_case22, edge_case22_replace)
    text = text.replace(edge_case23, edge_case23_replace)
    text = text.replace(edge_case24, edge_case24_replace)
    text = text.replace(edge_case25, edge_case25_replace)

    return text
def manual_fix_navajo(text):
    edge_cases_replace = [('x95x','s95x'), ('"s159p"', 's159p'), ("(103x2", "(s103x2"), ("(108n", "(s108n"), (":before 101h", ":before s101h"), ("""s1k :0-0""", """s1k :1-1"""), (""":QUOT (s77s / s78n)""", """:QUOT s77s"""), (""":QUOT (s98s / s99s)""", """:QUOT s98s""") ]
    for old, new in edge_cases_replace:
        text = text.replace(old, new)



    edge_cases = ["""empty umr
""", """
  :temporal ((s7n :before s6x))""",
                  """(s21s :before s20c)
                                      """,
                  """
                    :temporal ((s34x :before s34n))""",
                  """
                    :temporal ((s54h :Contained s53x))""",
                  """(s21s :before s20c)
                    """,
                  """
  :temporal ((s34x :before s34n))""",
                  """
  :temporal ((s54h :Contained s53x))""",
                  """
                    (s74n :Contained s74d)
                    (s74x :Contained s74d)""",
                  """
                    (s74x :Contained s74d)""",
                  """
  :coref ((s74p2 :same-entity s71p))""",
                  """(s75p :same-entity s74p2)
                    """,
                  """
                    (s93n :Contained s92e)""",
                  """
                    (s99p :same-entity s100p)""",
                  """(s100n :before s199d)
                    """,
                  """
  :temporal ((s100n :overlap s100x))""",
                  """
  :temporal ((s177x :Contained DCT))""",
                  """
                    (s122h3 :overlap s122n2)""",
                  """
                    (s133n3 :Contained s133n)""",
                  """
  :temporal ((s149x :Contained s150))""", """
  :Aspect nahaz’ą́ą́""", """
  :Aspect T’óó""", """
Ch’ínílį́į́dę́ę́’ :undefined
Chinle,-Arizona :undefined"""
                  ]

    for e in edge_cases:
        text = text.replace(e, "")





    return text
def manual_fix_sanapana(text):
    edge_cases_replace = [("s2'", "s2x"), ("""(s6e / exist-91
  :ARG1 (s6t/ thing
          :Theme-of (s6e2 / enyanmoama-00
                  :recipient (s6p / person))
  :Aspect State
  :MODSTR FullNeg)""", """(s6e / exist-91
  :ARG1 (s6t/ thing
          :Theme-of (s6e2 / enyanmoama-00
                  :recipient (s6p / person)))
  :Aspect State
  :MODSTR FullNeg)"""), ('“', '"'), ('”', '"'), ("""(s62e / empengkanma-00
  :actor (s62p / person
           :refer-person 1st
           :refer-number Plural)
  :theme (s62a / ava’
           :part (s62k / kangken’)
           :refer-number Plural)
  :goal (s62h / hengka’e)
  :temporal (s62o / or
              :op1 (s62e2 / event)
              :op2 (s62e2 / event))
  :MODSTR FullAff
  :Aspect Habitual)""", """(s62e / empengkanma-00
  :actor (s62p / person
           :refer-person 1st
           :refer-number Plural)
  :theme (s62a / ava’
           :part (s62k / kangken’)
           :refer-number Plural)
  :goal (s62h / hengka’e)
  :temporal (s62o / or
              :op1 (s62e2 / event)
              :op2 (s62e3 / event))
  :MODSTR FullAff
  :Aspect Habitual)"""), ("""(s48e / exist-91
  :ARG0 (s48p / place)
  :ARG1 (s48f / festival
          :name (s48n / name
                  :op1 "maleng")
          :mod (s48m / ma'a)
  :MODSTR FullAff
  :Aspect State)""", """(s48e / exist-91
  :ARG0 (s48p / place)
  :ARG1 (s48f / festival
          :name (s48n / name
                  :op1 "maleng")
          :mod (s48m / ma'a))
  :MODSTR FullAff
  :Aspect State)"""), ("""(s39e / engvetay’a-00
  :experiencer (s39p / person
                 :refer-person 1st
                 :refer-number Singular)
  :stimulus (s39m / m’a
              :Theme-of (s39e2 / ehltennaskama-00
                          :actor s39p
                          :recipient (s39p2 / person)
                          :topic (s39e3 / emmohetma-00
                                   :name (s39n / name
                                           :op1 "anyamenana")
                                   :MODSTR FullAff
                                   :QUOT s39e2
                                   :Modpred s39e
                                   :Aspect Process))
                          :MODSTR FullAff
                          :Aspect Performance))
  :extent (s39k / kessoye
              :mod (s39t / tkok))
  :MODSTR FullAff
  :Aspect State)""", """(s39e / engvetay’a-00
  :experiencer (s39p / person
                 :refer-person 1st
                 :refer-number Singular)
  :stimulus (s39m / m’a
              :Theme-of (s39e2 / ehltennaskama-00
                          :actor s39p
                          :recipient (s39p2 / person)
                          :topic (s39e3 / emmohetma-00
                                   :name (s39n / name
                                           :op1 "anyamenana")
                                   :MODSTR FullAff
                                   :QUOT s39e2
                                   :Modpred s39e
                                   :Aspect Process))
                          :MODSTR FullAff
                          :Aspect Performance)
  :extent (s39k / kessoye
              :mod (s39t / tkok))
  :MODSTR FullAff
  :Aspect State)"""), ("""(s5i2 / identity-91
  :ARG0 (s5e / event)
  :ARG1 (s5e2 / eleyvoma-00
          :actor (s5p / person
                   :ARG0-of (s5h / have-rel-role-91
                              :ARG1 (s5p2 / person
                                      :refer-number Plural
                                      :refer-person 1st)
                              :ARG2 (s5e2 / enyatav'a))
                   :refer-number Plural)
          :Aspect Process
          :MODSTR FullAff)
  :Aspect State
  :MODSTR FullAff)""", """(s5i2 / identity-91
  :ARG0 (s5e / event)
  :ARG1 (s5e2 / eleyvoma-00
          :actor (s5p / person
                   :ARG0-of (s5h / have-rel-role-91
                              :ARG1 (s5p2 / person
                                      :refer-number Plural
                                      :refer-person 1st)
                              :ARG2 (s5e3 / enyatav'a))
                   :refer-number Plural)
          :Aspect Process
          :MODSTR FullAff)
  :Aspect State
  :MODSTR FullAff)
"""), ("""(s8e / entoma-00
  :actor (s8p / person
           :refer-person 3rd
           :refer-number Plural)
  :undergoer (s8t / thing
               :Undergoer-of (s8e2 / entoma-00
                         :actor (s8p4 / person
                                :ref-person 3rd
                                :ref-number Plural))
  :concession (s8e3 / ele'hlevay'a-00
                :actor s8p4
                :recipient s8p
                :theme (s8a / and
                         :op1 (s8p3 / pava)
                         :op2 s8t)
                :MODSTR FullAff
                :Aspect Habitual)
  :reason (s8e4 / event)
  :MODSTR FullNeg
  :Aspect Habitual)""", """(s8e / entoma-00
  :actor (s8p / person
           :refer-person 3rd
           :refer-number Plural)
  :undergoer (s8t / thing
               :Undergoer-of (s8e2 / entoma-00
                         :actor (s8p4 / person
                                :ref-person 3rd
                                :ref-number Plural)))
  :concession (s8e3 / ele'hlevay'a-00
                :actor s8p4
                :recipient s8p
                :theme (s8a / and
                         :op1 (s8p3 / pava)
                         :op2 s8t)
                :MODSTR FullAff
                :Aspect Habitual)
  :reason (s8e4 / event)
  :MODSTR FullNeg
  :Aspect Habitual)"""), ("""(s22e / elaykamok-00
  :actor (s22p / person
           :refer-number Plural
           :refer-person 3rd)
  :recipient (s22p2 / person
               :mod (s22e2 / ethnic-group
                      :name (s22n / name
                              :op1 "nenhlet")
                      :wiki "Sanapaná")
               :refer-number Plural)
  :theme (s22e3 / enma'mekama-00
           :actor s22p2
           :Aspect Process
           :MODSTR FullAff)
  :Aspect Habitual
  :MODSTR FullAff
  :manner (s22e4 / event)""", """(s22e / elaykamok-00
  :actor (s22p / person
           :refer-number Plural
           :refer-person 3rd)
  :recipient (s22p2 / person
               :mod (s22e2 / ethnic-group
                      :name (s22n / name
                              :op1 "nenhlet")
                      :wiki "Sanapaná")
               :refer-number Plural)
  :theme (s22e3 / enma'mekama-00
           :actor s22p2
           :Aspect Process
           :MODSTR FullAff)
  :Aspect Habitual
  :MODSTR FullAff
  :manner (s22e4 / event))"""), ("""(s98o / or
  :op1 (s98e / event)
  :op2 (s98e2 / ensavkeskama-00
         :actor (s98p / person
                  :refer-person 3rd
                  :refer-number Plural)
         :theme (s98o / or
                  :op1 (s98p2 / provista)
                  :op2 (s98t / thing
                       :ARG1-of (s98r / resemble-91
                            :ARG2 s98p2)))
         :Aspect Habitual
         :affectee (s98p3 / person)
         :MODSTR FullAff))""", """(s98o / or
  :op1 (s98e / event)
  :op2 (s98e2 / ensavkeskama-00
         :actor (s98p / person
                  :refer-person 3rd
                  :refer-number Plural)
         :theme (s98o2 / or
                  :op1 (s98p2 / provista)
                  :op2 (s98t / thing
                       :ARG1-of (s98r / resemble-91
                            :ARG2 s98p2)))
         :Aspect Habitual
         :affectee (s98p3 / person)
         :MODSTR FullAff))"""), ("""(s76e / entema-00
  :actor (s76p / person
           :mod (s76e2 / ethnic-group
                  :name (s76n / name
                          :op1 "nenhlet")
                  :wiki "Sanapaná")
           :refer-number Singular)
  :recipient (s76p2 / person)
  :theme (s76a / and
           :op1 (s76a2 / and
                  :op1 (s76h / have-location-91
                         :ARG0 (s76p3 / place)
                         :ARG1 (s76a3 / anteyepe')
                         :Aspect State
                         :QUOT s76e
                         :MODSTR FullAff)
                  :op2 (s76e3 / empo'temama-00
                         :actor (s76p4 / person
                                  :refer-person 1st
                                  :refer-number Plural)
                         :Aspect Performance
                         :MODSTR FullAff
                         :QUOT s76e))
           :op2 s76e3
  :Aspect Performance
  :MODSTR FullAff)""", """(s76e / entema-00
  :actor (s76p / person
           :mod (s76e2 / ethnic-group
                  :name (s76n / name
                          :op1 "nenhlet")
                  :wiki "Sanapaná")
           :refer-number Singular)
  :recipient (s76p2 / person)
  :theme (s76a / and
           :op1 (s76a2 / and
                  :op1 (s76h / have-location-91
                         :ARG0 (s76p3 / place)
                         :ARG1 (s76a3 / anteyepe')
                         :Aspect State
                         :QUOT s76e
                         :MODSTR FullAff)
                  :op2 (s76e3 / empo'temama-00
                         :actor (s76p4 / person
                                  :refer-person 1st
                                  :refer-number Plural)
                         :Aspect Performance
                         :MODSTR FullAff
                         :QUOT s76e)))
           :op2 s76e3
  :Aspect Performance
  :MODSTR FullAff)"""), ("""(s37i2 / identity-91
  :ARG0 (s37t / thing
          :Place-of (s37e / eleyvoma-00
                      :actor (s37p / person
                               :refer-number Plural
                               :refer-person 3rd)
                      :MODSTR FullAff
                      :Aspect Endeavor))
  :ARG1 (s37p2 / place
          :start (s37h / hengka'e)
          :goal (s37a / and
                  :op1 (s37r / river
                         :name (s37n / name
                                 :op1 "rio"
                                 :op2 "verde")
                         :wiki "Río_Verde_(Paraguay))
                  :op2 (s37r2 / river
                         :name (s37n2 / name
                                 :op1 "rio"
                                 :op2 "paraguay")
                         :wiki "Paraguay_River")))
  :Aspect State
  :MODSTR FullAff)""", """(s37i2 / identity-91
  :ARG0 (s37t / thing
          :Place-of (s37e / eleyvoma-00
                      :actor (s37p / person
                               :refer-number Plural
                               :refer-person 3rd)
                      :MODSTR FullAff
                      :Aspect Endeavor))
  :ARG1 (s37p2 / place
          :start (s37h / hengka'e)
          :goal (s37a / and
                  :op1 (s37r / river
                         :name (s37n / name
                                 :op1 "rio"
                                 :op2 "verde")
                         :wiki "Río_Verde_Paraguay)
                  :op2 (s37r2 / river
                         :name (s37n2 / name
                                 :op1 "rio"
                                 :op2 "paraguay")
                         :wiki "Paraguay_River")))
  :Aspect State
  :MODSTR FullAff)"""), ("""(s13a / ahlannenhan))""", """(s13a / ahlannenhan)"""),
                          ("""(s17y / yavhananhan))""", """(s17y / yavhananhan)"""), ("""(s55i2 / identity-91
  :ARG0 (s55e / event)
  :ARG1 (s55e2 / eleyvoma-00
          :actor (s55p / person
                   :refer-number Plural
                   :mod (s55e2 / ethnic-group
                          :name (s55n / name
                                  :op1 "nenhlet")
                          :wiki "Sanapaná"))
          :Aspect Process
          :MODSTR FullAff)
  :temporal (s55h / hlemmea)
  :Aspect State
  :MODSTR FullAff)""", """(s55i2 / identity-91
  :ARG0 (s55e / event)
  :ARG1 (s55e2 / eleyvoma-00
          :actor (s55p / person
                   :refer-number Plural
                   :mod (s55e3 / ethnic-group
                          :name (s55n / name
                                  :op1 "nenhlet")
                          :wiki "Sanapaná"))
          :Aspect Process
          :MODSTR FullAff)
  :temporal (s55h / hlemmea)
  :Aspect State
  :MODSTR FullAff)"""), ("""(s57e / engvay'a-00
  :actor (s57a2 / anya'a
           :refer-number Singular)
  :other (s57m / mokham)
  :Aspect Performance
  :topic (s57e / event)
  :goal (s57p / place)
  :MODSTR FullAff)""", """(s57e2 / engvay'a-00
  :actor (s57a2 / anya'a
           :refer-number Singular)
  :other (s57m / mokham)
  :Aspect Performance
  :topic (s57e / event)
  :goal (s57p / place)
  :MODSTR FullAff)"""), ("""(s13a / ala'mopay'a))""", """(s13a / ala'mopay'a)"""), ("""(s27h / have-mod-91
         :ARG1 (s27a / ava'
                 :part (s27t / thing)
                 :refer-number Plural)
         :ARG2 (s27a2 / alvana'tema)
         :Aspect State
         :MODSTR FullAff))""", """(s27h / have-mod-91
         :ARG1 (s27a / ava'
                 :part (s27t / thing)
                 :refer-number Plural)
         :ARG2 (s27a2 / alvana'tema)
         :Aspect State
         :MODSTR FullAff)"""), ("""(have-condition-91 :Unsp 61e2)""", """(have-condition-91 :Unsp s61e2)"""),
                          ("""(Null_Permitter :FullAff s64)""", """(Null_Permitter :FullAff s64p)"""),
                          ("""(s23e :same-event 25e2)""", """(s23e :same-event s25e2)"""), ("""(s65s0 / sentence

  :temporal ((s65e :after s65e2))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s65e2))""", """(s65s0 / sentence

  :temporal ((s65e :after s65e2))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s65e2)))"""), ("""(s15s0 / sentence

  :temporal ((s15e :after s15e2)

                    (s15e2 :overlap s15e3)))

  :coref ((s14e :same-event s15e)

                    (s14e2 :same-event s15e2)

                    (s11p :same-entity s15p)

                    (s14t :same-entity s15t)))""", """(s15s0 / sentence

  :temporal ((s15e :after s15e2)

                    (s15e2 :overlap s15e3))

  :coref ((s14e :same-event s15e)

                    (s14e2 :same-event s15e2)

                    (s11p :same-entity s15p)

                    (s14t :same-entity s15t)))"""), ("""(s21s0 / sentence

  :temporal ((s20h2 :overlap s21e)

                    (s21e :overlap s21e2))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :NeutAff have-condition-91)

                    (have-condition-91 :FullAff s21e)

                    (have-condition-91 :FullAff s21e2))

  :coref (s20p2 :same-entity s21p)))""", """(s21s0 / sentence

  :temporal ((s20h2 :overlap s21e)

                    (s21e :overlap s21e2))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :NeutAff have-condition-91)

                    (have-condition-91 :FullAff s21e)

                    (have-condition-91 :FullAff s21e2))

  :coref ((s20p2 :same-entity s21p)))"""), ("""(s51s0 / sentence

  :temporal ((past-reference :contained s51e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullNeg s51e)

  :coref ((s50p :subset-of s51p2)

                    (s50p :subset-of s51p3)))""", """(s51s0 / sentence

  :temporal ((past-reference :contained s51e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullNeg s51e))

  :coref ((s50p :subset-of s51p2)

                    (s50p :subset-of s51p3)))"""), ("""(s57s0 / sentence

  :temporal ((s32e :after s57e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s57e))

  :coref (s32p2 :same-entity s57p)))""", """(s57s0 / sentence

  :temporal ((s32e :after s57e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s57e))

  :coref ((s32p2 :same-entity s57p)))"""), ("""(s63s0 / sentence

  :temporal ((s58e2 :overlap s63e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s63e))

  :coref ((s62p2 :same-entity s63n)

                    (s62p :same-entity s63h))""", """(s63s0 / sentence

  :temporal ((s58e2 :overlap s63e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s63e))

  :coref ((s62p2 :same-entity s63n)

                    (s62p :same-entity s63h)))"""), ("""(s65s0 / sentence

  :temporal ((s64e :before s65e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s65e))

  :coref ((s64p :same-entity s65p)

                    (s64p2 :same-entity s65p2))""", """(s65s0 / sentence

  :temporal ((s64e :before s65e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s65e))

  :coref ((s64p :same-entity s65p)

                    (s64p2 :same-entity s65p2)))"""), ("""(s67s0 / sentence

  :temporal ((s65e :before s67e)

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s67e))

  :coref ((s65p :same-entity s67p)))""", """(s67s0 / sentence

  :temporal ((s65e :before s67e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s67e))

  :coref ((s65p :same-entity s67p)))"""), ("""(s92s0 / sentence

  :temporal ((s92e4 :overlap s92e)

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullNeg s92e)

                    (AUTH :FullAff s92e4))

  :coref ((s81e :same-event s92e4)

                    (s81p :same-entity s92p2)))""", """(s92s0 / sentence

  :temporal ((s92e4 :overlap s92e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullNeg s92e)

                    (AUTH :FullAff s92e4))

  :coref ((s81e :same-event s92e4)

                    (s81p :same-entity s92p2)))"""), ("""(s108s0 / sentence

  :temporal ((s106e :after s108e)""", """(s108s0 / sentence

  :temporal ((s106e :after s108e))"""), ("""(s82e0 / sentence""", """(s82s0 / sentence"""),
                          ("""(AUTH :FullNeg 115h)""", """(AUTH :FullNeg s115h)"""),
                          ("""(s60h :same-event ss115h2)""", """(s60h :same-event s115h2)"""),
                          (""":temporal (( :Contained s46i2))""", """:temporal ((Past_ref :Contained s46i2))"""), ("""(s63s0 / sentence

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s63i2))

  :coref ((s59i2 :same-event s63i2)

                    (s59t :same-event s63t)

                    (s59t2 :same-event s63t2)))""", """(s63s0 / sentence

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s63i2))

  :coref ((s59i2 :same-event s63i2)

                    (s59e :same-event s63t)

                    (s59t :same-event s63t2)))"""), ("""(s73s0 / sentence

  :temporal ((s69e :overlap s73h))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s73h))

  :coref ((s64p2 :same-entity s73p2)

                    (s70p2 :same-entity s73p)))""", """(s73s0 / sentence

  :temporal ((s69e :overlap s73h))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s73h))

  :coref ((s64p2 :same-entity s73p2)

                    (s71p2 :same-entity s73p)))"""), (""":coref ((s78i2 :same-event s80i2)

                    (s78e :same-event s80e)

                    (s78e2 :same-event s80t2)))""", """:coref ((s78i2 :same-event s80i2)

                    (s78e :same-event s80e)

                    (s78e2 :same-event s80t)))"""), ("""(s83s0 / sentence

  :temporal ((s82e :overlap s83h)

                    (s82h :overlap s83e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s83e)

                    (AUTH :FullAff s83h))

  :coref ((s82a :same-entity s83p)))""", """(s83s0 / sentence

  :temporal ((s82e :overlap s83h)

                    (s83h :overlap s83e))

  :modal ((ROOT :MODAL AUTH)

                    (AUTH :FullAff s83e)

                    (AUTH :FullAff s83h))

  :coref ((s82a :same-entity s83p)))"""), (""":coref ((s104a :same-event s107e)

              (s104e :same-event s107h)

              (s105p :same-entity s107p)))""", """:coref ((s104a :same-event s107a)

              (s104e :same-event s107h)

              (s105p :same-entity s107p)))"""),
                          (""":coref ((s39e2 :same-event s52a)""", """:coref ((s39e2 :same-event s52e)""")]

    for old, new in edge_cases_replace:
        text = text.replace(old, new)

    edge_cases = ["""s80t2: 0-0
""", """
s59t2: 0-0""", """s84h: undefined
"""]
    for e in edge_cases:
        text = text.replace(e, "")
    return text
