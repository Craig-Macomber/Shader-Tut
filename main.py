"""
Craig's CG Tutorial for Panda3D
This is for use with Panda3D: www.panda3d.org
It is for using CG: http://en.wikipedia.org/wiki/Cg_(programming_language)

Knowledge of Panda3D is assumed, and we will work from Python,
though the majority should apply to C++ as well.

Knowledge of linear algrebra is assumed: http://en.wikipedia.org/wiki/Linear_algebra
If you come across an equation in a shader you don't understand,
its prabably something from linear algrebra.
The CG functions we will be using are all in this list: http://http.developer.nvidia.com/CgTutorial/cg_tutorial_appendix_e.html

Knowlege of basic C syntax is assumed. The C in in CG means the C language.
If you get confused by syntax, its likley the same as in C which is easy to look up.
Differences from C will be noted when relevent.

This tutorial is mostly examples which you could be able to learn about by reading and modifying.
It consists of a set of shaders applied to some Pandas, and the needed python code to set them up.

"""

import direct.directbase.DirectStart
from direct.actor.Actor import Actor
base.disableMouse()
base.camera.setPos(0,-5000,0)

def getPanda():
    panda=Actor("models/panda-model",{"walk": "models/panda-walk4"})
    panda.loop("walk")
    return panda
panda=getPanda()

# this just makes us as many pandas as we need, and puts then ina grid
# ordered left to right, bottom to top
count=[0]
def getNode(copy=False):
    node = (getPanda() if copy else panda).instanceUnderNode(render,"")
    node.setX(-1200+(count[0]%5)*600)
    node.setZ(-1000+(count[0]/5)*500)
    count[0]+=1
    return node

# these three don't use shaders, just examples of out setup here
plane=getNode()
red=getNode()
red.setColor(1,0,0,0)
blue=getNode()
blue.setColor(0,0,1,0)

# now for some shaders

# autoshader looks the same as plane, nothing special
auto=getNode()
auto.setShaderAuto() 

# gets a panda, applies the shader from the passed filename, and return the shader
def shade(filename):
    shader=loader.loadShader(filename+'.sha')
    node=getNode()
    node.setShader(shader)
    return node

# minimal custom shader
# read minimal.sha for info!
shade("minimal")

# read simple.sha for info!
# makes a plad panda or sorts.
shade("simple")

# more comming soon

# demo for my shader geneator comming soon! for now,
# see shadergeneator/test.py

run()