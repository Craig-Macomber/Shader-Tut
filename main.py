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

pandas=[] # we need to keep a referance so the Actors don't get garbage collected and stop animating
def getPanda():
    panda=Actor("models/panda-model",{"walk": "models/panda-walk4"})
    panda.loop("walk")
    pandas.append(panda)
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
plain=getNode()
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

# read inputs.sha for info!
# makes a panda change color over time
# by using a shader input
inputExample=shade("inputs")
time=[0]
def setInput(task):
    time[0]+= globalClock.getDt()
    t=time[0]
    # set the input to some time variable color to show it varying over time
    inputExample.setShaderInput("inputExample",t%1,t/2.3%1,t/3.7%1,1)
    return task.cont
taskMgr.add(setInput,"inputUpdate")



#### demo for my shader geneator ####
## 1 - A Red Panda via getManager 
# see shadergenerator/test.py
import shadergenerator.manager
# setup a shaderManager, see shadergenerator/manager.py
# this is just a simple wrapper around the more complex inner workings
# the paramaters are a list of library directories, and a script the defines the shader generator
# and an optional path for any output debug files
shaderManager=shadergenerator.manager.getManager(["shadergenerator/library"],"shadergenerator/graph/basic.gen",debugPath="shadergenerator/ShadersOut/")
# and use the manager to generate a shader
# first paramater is the node to process, and second is an optional debug file to dump the shader soure to.
shaderManager.genShaders(getNode(True),"debug")


## 2 - A Red Panda without getManager
# now, the same thing without using the getManager
import shadergenerator.shaderBuilder
# load the library
library=shadergenerator.shaderBuilder.Library(["shadergenerator/library"])
# use the library with the script to get a ShaderBuilder
builder=library.loadScript("shadergenerator/graph/basic.gen")
# make a manager thats the same as the one getManager returned
shaderManager2=shadergenerator.manager.Manager(builder)
# shader source is the same as last time, so I'm omitting the debug path
shaderManager2.genShaders(getNode(True))

## 3 - A Red Panda without using Manager.genShaders
# Manager.genShaders walks the scene graph under the passed node, and generates shaders for every geom
# often thats what you want, but not alwayse. To generate a single shader, we can use Manager.makeShader
# look at the source of Manager.makeShader for details and addational paramaters
node=getNode()
shader=shaderManager2.makeShader(node)
node.setShader(shader)



## 4 - A Red Panda without using Manager - an intro shaderGenerator renderStates
# This is not important to using the shaderGenerator in most cases, but
# its important for extending and understanding it.
# Panda has a renderState class, which describes the state of a node in the scene graph.
# The shader generator uses a very similar RenderState class.
# The shader generator takes this state, feeds it to the ShaderBuilder, which then generates
# a custom shader just for that renderState.
# The reason the panda RenderState class is not used is tweo fold:
#       - It contains lots of unneeded data (hurts caching)
#       _ It is missing some needed data (tags, geomVertexFormat)
# To get the exact minimum needed data stored in our RenderStates for the ShaderBuilder,
# the graph of nodes (created by the script) that describes the configuration of
# the particular builder is used to setup a RenderStateFactory the produces ideal minimal RenderStates
# See shadergenerator/renderState.py for more info, and see Manager for some more example usage.

node=getNode()
# init a renderStateFactory that produces minimal renderStates as needed for builder
renderStateFactory=builder.setupRenderStateFactory()
# use the factory to produce a renderState from our node
renderState=renderStateFactory.getRenderState(node)
# and finally submit the renderState to get a shader
shader=builder.getShader(renderState)
node.setShader(shader)

## 5 - A Textured Panda, demo of a more compelex shader generator
# this time using the tex.gen script, read the script for info
shaderManager=shadergenerator.manager.getManager(["shadergenerator/library"],"shadergenerator/graph/tex.gen")
shaderManager.genShaders(getNode(True))

## 6 - A Lit Panda, demo of a more compelex shader generator
# this time using the lit.gen script, read the script for info
shaderManager=shadergenerator.manager.getManager(["shadergenerator/library"],"shadergenerator/graph/lit.gen")

node=getNode(True)
# this script requires a dlight input, so add one:
from panda3d.core import DirectionalLight,Vec4,Point3,AmbientLight
dlight = DirectionalLight('dlight')
dlight.setColor(Vec4(4.9, 0.9, 0.8, 1))
dlnp = render.attachNewNode(dlight)
node.setShaderInput('dlight',dlnp)
dayCycle=dlnp.hprInterval(10.0,Point3(0,360,0))
dayCycle.loop()
node.setShaderInput('fogDensity',.0001)
shaderManager.genShaders(node)

run()