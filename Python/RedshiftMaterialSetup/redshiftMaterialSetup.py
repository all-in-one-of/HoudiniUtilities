import hou

materialName = 'Iron';
matPath = '/mat/' + materialName;

hou.node('/mat/').createNode('redshift_vopnet',materialName);

# Create material node
hou.node(matPath).createNode('redshift::Material','RS_Material');

#Create texture nodes
hou.node(matPath).createNode('redshift::TextureSampler','diffuse');
hou.node(matPath).createNode('redshift::TextureSampler','ao');
hou.node(matPath).createNode('redshift::TextureSampler','roughness');
hou.node(matPath).createNode('redshift::TextureSampler','specular');

hou.node(matPath).createNode('redshift::TextureSampler','normal');
hou.node(matPath).createNode('redshift::TextureSampler','bump');
hou.node(matPath).createNode('redshift::TextureSampler','displacement_tex');

#Create bump and displacement nodes
hou.node(matPath).createNode('redshift::BumpMap','BumpMap_Normal');
hou.node(matPath).createNode('redshift::BumpMap','BumpMap_Bump');
hou.node(matPath).createNode('redshift::BumpBlender','BumpBlender');
hou.node(matPath).createNode('redshift::Displacement','Displacement');

# Connect material nodes
hou.node(matPath +'/redshift_material1').setInput(0,hou.node(matPath + '/RS_Material'));

# Connect texture nodes
hou.node(matPath +'/RS_Material').setInput(0,hou.node(matPath + '/diffuse'));
hou.node(matPath +'/RS_Material').setInput(7,hou.node(matPath + '/roughness'));
hou.node(matPath +'/RS_Material').setInput(6,hou.node(matPath + '/specular'));

# Connect ao
hou.node(matPath +'/diffuse').setInput(3,hou.node(matPath + '/ao'));

# Connect bump nodes
hou.node(matPath +'/BumpMap_Normal').setInput(0,hou.node(matPath + '/normal'));
hou.node(matPath +'/BumpMap_Bump').setInput(0,hou.node(matPath + '/bump'));
hou.node(matPath +'/BumpBlender').setInput(0,hou.node(matPath + '/BumpMap_Normal'));
hou.node(matPath +'/BumpBlender').setInput(1,hou.node(matPath + '/BumpMap_Bump'));
hou.node(matPath +'/RS_Material').setInput(49,hou.node(matPath + '/BumpBlender'));

# Connect displacement nodes
hou.node(matPath +'/redshift_material1').setInput(1,hou.node(matPath + '/Displacement'));
hou.node(matPath +'/Displacement').setInput(0,hou.node(matPath + '/displacement_tex'));


hou.node(matPath).layoutChildren()