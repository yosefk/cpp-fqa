name2alt = {
    "systemc": "[System C: putting the 'hard' in hardware design]",
    "fqa": "[C++ FQA Lite]",
    "defective": "[Defective C++]",
    "not-crippled": "[This site is not crippled by C++]",
    "not-entirely": "[This site is not entirely crippled by C++]",
    "overload": "[C::operator++(int): invalid overload]",
    "static": "[C++ gives me static]",
    "operator": "[operator<< is not my friend]",
}
name2alt = {
    "cat": "[Cat++, a superset of cat]",
}

for k, v in list(name2alt.items()):
    s = """<a href="http://yosefk.com/c++fqa">
<img src="http://yosefk.com/c++fqa/images/%s.png"
     alt="%s" border=0>
</a>""" % (
        k,
        v,
    )

    print("`%s`" % s)
    print("@\n%s\n@" % s.replace("/", "\\/"))
    print()


# <a href="http://yosefk.com/c++fqa">
# <img src="http://yosefk.com/c++fqa/images/systemc.png"
#     alt="[System C: putting the 'hard' in hardware design]" border=0>
# </a>
