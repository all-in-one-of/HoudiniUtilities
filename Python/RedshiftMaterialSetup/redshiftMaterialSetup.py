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

normalTEX = ""
    
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
    

# Create material node
hou.node(matPath).createNode('redshift::Material','RS_Material')
#Set brdf to GGX
hou.node(matPath +'/RS_Material').parm('refl_brdf').set('1')
#Set fresnel type to metalness
hou.node(matPath +'/RS_Material').parm('refl_fresnel_mode').set('2')

#Create texture nodes
hou.node(matPath).createNode('redshift::TextureSampler','diffuse')
hou.node(matPath).createNode('redshift::TextureSampler','ao')
hou.node(matPath).createNode('redshift::TextureSampler','roughness')
hou.node(matPath).createNode('redshift::TextureSampler','metalness')

hou.node(matPath).createNode('redshift::TextureSampler','normal')
hou.node(matPath).createNode('redshift::TextureSampler','bump')
hou.node(matPath).createNode('redshift::TextureSampler','displacement_tex')

#Create bump and displacement nodes
hou.node(matPath).createNode('redshift::BumpMap','BumpMap_Normal')
hou.node(matPath +'/BumpMap_Normal').parm('inputType').set('1')

hou.node(matPath).createNode('redshift::BumpMap','BumpMap_Bump')
hou.node(matPath).createNode('redshift::BumpBlender','BumpBlender')
hou.node(matPath).createNode('redshift::Displacement','Displacement')

# Connect material nodes
hou.node(matPath +'/redshift_material1').setInput(0,hou.node(matPath + '/RS_Material'))

# Connect texture nodes
hou.node(matPath +'/RS_Material').setInput(0,hou.node(matPath + '/diffuse'))
hou.node(matPath +'/RS_Material').setInput(7,hou.node(matPath + '/roughness'))
hou.node(matPath +'/RS_Material').setInput(14,hou.node(matPath + '/metalness'))

# Connect ao
hou.node(matPath +'/diffuse').setInput(3,hou.node(matPath + '/ao'))

# Connect bump nodes
hou.node(matPath +'/BumpMap_Normal').setInput(0,hou.node(matPath + '/normal'))
hou.node(matPath +'/BumpMap_Bump').setInput(0,hou.node(matPath + '/bump'))
hou.node(matPath +'/BumpBlender').setInput(0,hou.node(matPath + '/BumpMap_Normal'))
hou.node(matPath +'/BumpBlender').setInput(1,hou.node(matPath + '/BumpMap_Bump'))
hou.node(matPath +'/RS_Material').setInput(49,hou.node(matPath + '/BumpBlender'))

# Connect displacement nodes
hou.node(matPath +'/redshift_material1').setInput(1,hou.node(matPath + '/Displacement'))
hou.node(matPath +'/Displacement').setInput(0,hou.node(matPath + '/displacement_tex'))


# Assign textures and set gamma
hou.node(matPath +'/diffuse').parm('tex0').set(diffuseTEX)
hou.node(matPath +'/diffuse').parm('tex0_gammaoverride').set(1)
hou.node(matPath +'/diffuse').parm('tex0_srgb').set(1)

hou.node(matPath +'/metalness').parm('tex0').set(metalTEX)
hou.node(matPath +'/metalness').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/roughness').parm('tex0').set(roughTEX)
hou.node(matPath +'/roughness').parm('tex0_gammaoverride').set(1)

hou.node(matPath +'/normal').parm('tex0').set(normalTEX)
hou.node(matPath +'/normal').parm('tex0_gammaoverride').set(1)

hou.node(matPath).layoutChildren()