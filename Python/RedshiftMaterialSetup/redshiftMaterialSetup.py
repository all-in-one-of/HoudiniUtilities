import hou

filePath = hou.parm('/mat/Texture_Import/mat_path').unexpandedString()
materialName = filePath.split("/")[-2]
print materialName
matPath = '/mat/' + materialName

# Check if vopnet exists
if (hou.item(matPath) == None):
    print "Material Does Not Exist!"
    hou.node('/mat/').createNode('redshift_vopnet',materialName)
else:
    for child in hou.node(matPath).children():
#        print child 
        child.destroy()
    hou.node(matPath).createNode('redshift_material','redshift_material1')
    

# Get texture suffixes
if (hou.parm('/mat/Texture_Import/diffuse').eval()==1):
    diffuseSuffix = hou.parm('/mat/Texture_Import/diffuse_name').eval()
    diffuseTEX = filePath + materialName + diffuseSuffix
else:
    diffuseTEX = ""
    
if (hou.parm('/mat/Texture_Import/roughness').eval()==1):
    roughSuffix = hou.parm('/mat/Texture_Import/rough_name').eval()
    roughTEX = filePath + materialName + roughSuffix
else:
    roughTEX = ""

if (hou.parm('/mat/Texture_Import/metalness').eval()==1):
    metalSuffix = hou.parm('/mat/Texture_Import/metal_name').eval()
    metalTEX = filePath + materialName + metalSuffix
else:
    metalTEX = ""
    
if (hou.parm('/mat/Texture_Import/normal').eval()==1):
    normalSuffix = hou.parm('/mat/Texture_Import/normal_name').eval()
    normalTEX = filePath + materialName + normalSuffix
else:
    normalTEX = ""
    
if (hou.parm('/mat/Texture_Import/ao').eval()==1):
    aoSuffix = hou.parm('/mat/Texture_Import/ao_name').eval()
    aoTEX = filePath + materialName + aoSuffix
else:
    aoTEX = ""

if (hou.parm('/mat/Texture_Import/bump').eval()==1):
    bumpSuffix = hou.parm('/mat/Texture_Import/bump_name').eval()
    bumpTEX = filePath + materialName + bumpSuffix
else:
    bumpTEX = ""

if (hou.parm('/mat/Texture_Import/displacement').eval()==1):
    displacementSuffix = hou.parm('/mat/Texture_Import/displacement_name').eval()
    displacementTEX = filePath + materialName + displacementSuffix
else:
    displacementTEX = ""

# Check if using glossiness
roughness_invert = hou.parm('/mat/Texture_Import/roughness_invert').eval()

# Check if using triplanar
triplanar_check = hou.parm('/mat/Texture_Import/triplanar_check').eval()

# Create texture transform parameters
hou.node(matPath).createNode('parameter','scale')
hou.node(matPath +'/scale').parm('parmname').set('scale')
hou.node(matPath +'/scale').parm('parmtype').set(5)
hou.node(matPath +'/scale').parmTuple('float2def')[0].set(1)
hou.node(matPath +'/scale').parmTuple('float2def')[1].set(1)

hou.node(matPath).createNode('parameter','offset')
hou.node(matPath +'/offset').parm('parmname').set('offset')
hou.node(matPath +'/offset').parm('parmtype').set(5)

hou.node(matPath).createNode('parameter','rotation')
hou.node(matPath +'/rotation').parm('parmname').set('rotation')
hou.node(matPath +'/rotation').parm('rangeflt2').set(360)

# Create triplanar transform parameters
hou.node(matPath).createNode('parameter','tri_scale')
hou.node(matPath +'/tri_scale').parm('parmname').set('tri_scale')
hou.node(matPath +'/tri_scale').parm('parmlabel').set('Tri Planar Scale')
hou.node(matPath +'/tri_scale').parm('parmtype').set(6)
hou.node(matPath +'/tri_scale').parm('float3def1').set(1)
hou.node(matPath +'/tri_scale').parm('float3def2').set(1)
hou.node(matPath +'/tri_scale').parm('float3def3').set(1)

hou.node(matPath).createNode('parameter','tri_offset')
hou.node(matPath +'/tri_offset').parm('parmname').set('tri_offset')
hou.node(matPath +'/tri_offset').parm('parmlabel').set('Tri Planar Offset')
hou.node(matPath +'/tri_offset').parm('parmtype').set(6)

hou.node(matPath).createNode('parameter','tri_rotation')
hou.node(matPath +'/tri_rotation').parm('parmname').set('tri_rotation')
hou.node(matPath +'/tri_rotation').parm('parmlabel').set('Tri Planar Rotation')
hou.node(matPath +'/tri_rotation').parm('parmtype').set(6)

# Create triplanar switch
if hou.node(matPath).parm('triPlanar') == None:
	parm_group = hou.node(matPath).parmTemplateGroup()
	parm_folder = hou.FolderParmTemplate('folder', 'Tri Planar')
	parm_folder.addParmTemplate(hou.ToggleParmTemplate('triPlanar', 'Tri Planar', 0))
	parm_group.append(parm_folder)
	hou.node(matPath).setParmTemplateGroup(parm_group)

# Create material node
hou.node(matPath).createNode('redshift::Material','RS_Material')
#Set brdf to GGX
hou.node(matPath +'/RS_Material').parm('refl_brdf').set('1')
#Set fresnel type to metalness
hou.node(matPath +'/RS_Material').parm('refl_fresnel_mode').set('2')


#Create texture nodes
textureNodes = (
	'diffuse',
	'ao',
	'roughness',
	'metalness',
	'normal',
	'bump',
	'displacement_tex'
)

for node in textureNodes:
	hou.node(matPath).createNode('redshift::TextureSampler',node)

# hou.node(matPath).createNode('redshift::TextureSampler','diffuse')
# hou.node(matPath).createNode('redshift::TextureSampler','ao')
# hou.node(matPath).createNode('redshift::TextureSampler','roughness')
# hou.node(matPath).createNode('redshift::TextureSampler','metalness')

# hou.node(matPath).createNode('redshift::TextureSampler','normal')
# hou.node(matPath).createNode('redshift::TextureSampler','bump')
# hou.node(matPath).createNode('redshift::TextureSampler','displacement_tex')

#Create bump and displacement nodes
hou.node(matPath).createNode('redshift::BumpMap','BumpMap_Normal')
hou.node(matPath +'/BumpMap_Normal').parm('inputType').set('1')

hou.node(matPath).createNode('redshift::BumpMap','BumpMap_Bump')
hou.node(matPath).createNode('redshift::BumpBlender','BumpBlender')
hou.node(matPath).createNode('redshift::Displacement','Displacement')

# Create triplanar networks
for nodes in textureNodes:
	hou.node(matPath).createNode('redshift::TriPlanar','TriPlanar_' + nodes)
	hou.node(matPath).createNode('redshift::vopSwitch','vopSwitch_' + nodes)

	hou.node(matPath +'/vopSwitch_' + nodes).setInput(0,hou.node(matPath + '/' + nodes))
	hou.node(matPath +'/TriPlanar_' + nodes).setInput(0,hou.node(matPath + '/' + nodes))
	hou.node(matPath +'/vopSwitch_' + nodes).setInput(1,hou.node(matPath + '/TriPlanar_' + nodes))

	hou.node(matPath +'/vopSwitch_' + nodes).parm('RS_switch').setExpression('ch("' + matPath + '/' + 'triPlanar")')

# Connect material nodes
hou.node(matPath +'/redshift_material1').setInput(0,hou.node(matPath + '/RS_Material'))


# Connect texture nodes
hou.node(matPath +'/RS_Material').setInput(0,hou.node(matPath + '/vopSwitch_diffuse'))
hou.node(matPath +'/RS_Material').setInput(14,hou.node(matPath + '/vopSwitch_metalness'))

if roughness_invert:
	hou.node(matPath).createNode('redshift::RSMathInvColor','RSMathInvColor_roughness')
	hou.node(matPath +'/RSMathInvColor_roughness').setInput(0,hou.node(matPath + '/vopSwitch_roughness'))
	hou.node(matPath +'/RS_Material').setInput(7,hou.node(matPath + '/RSMathInvColor_roughness'))
else:
	hou.node(matPath +'/RS_Material').setInput(7,hou.node(matPath + '/vopSwitch_roughness'))


# Connect ao
hou.node(matPath +'/diffuse').setInput(3,hou.node(matPath + '/vopSwitch_ao'))


# Connect bump nodes
hou.node(matPath +'/BumpMap_Normal').setInput(0,hou.node(matPath + '/vopSwitch_normal'))
hou.node(matPath +'/BumpMap_Bump').setInput(0,hou.node(matPath + '/vopSwitch_bump'))
hou.node(matPath +'/BumpBlender').setInput(0,hou.node(matPath + '/BumpMap_Normal'))
hou.node(matPath +'/BumpBlender').setInput(1,hou.node(matPath + '/BumpMap_Bump'))
hou.node(matPath +'/RS_Material').setInput(49,hou.node(matPath + '/BumpBlender'))


# Connect displacement nodes
hou.node(matPath +'/redshift_material1').setInput(1,hou.node(matPath + '/Displacement'))
hou.node(matPath +'/Displacement').setInput(0,hou.node(matPath + '/vopSwitch_displacement_tex'))

# Connect parms
for node in textureNodes:
	hou.node(matPath + '/' + node).setInput(0,hou.node(matPath + '/scale'))
	hou.node(matPath + '/' + node).setInput(1,hou.node(matPath + '/offset'))
	hou.node(matPath + '/' + node).setInput(2,hou.node(matPath + '/rotation'))

# Connect tri planar parms
for node in textureNodes:
	hou.node(matPath + '/TriPlanar_' + node).setInput(4,hou.node(matPath + '/tri_scale'))
	hou.node(matPath + '/TriPlanar_' + node).setInput(5,hou.node(matPath + '/tri_offset'))
	hou.node(matPath + '/TriPlanar_' + node).setInput(6,hou.node(matPath + '/tri_rotation'))

# Assign textures and set gamma (can be done with loop)
hou.node(matPath +'/diffuse').parm('tex0').set(diffuseTEX)
hou.node(matPath +'/diffuse').parm('tex0_gammaoverride').set(1)
hou.node(matPath +'/diffuse').parm('tex0_srgb').set(1)

hou.node(matPath +'/metalness').parm('tex0').set(metalTEX)
hou.node(matPath +'/metalness').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/roughness').parm('tex0').set(roughTEX)
hou.node(matPath +'/roughness').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/normal').parm('tex0').set(normalTEX)
hou.node(matPath +'/normal').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/bump').parm('tex0').set(bumpTEX)
hou.node(matPath +'/bump').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/ao').parm('tex0').set(aoTEX)
hou.node(matPath +'/ao').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/displacement_tex').parm('tex0').set(displacementTEX)
hou.node(matPath +'/displacement_tex').parm('tex0_gammaoverride').set(1)

hou.node(matPath).layoutChildren()