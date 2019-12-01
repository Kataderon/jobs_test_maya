def setAttribute(pbr_attr, file_attr, value):
	file = setAttribute(pbr_attr, value)
	cmd.connectAttr(file + "." + file_attr, "R_UberMat." + pbr_attr, force=True)
	cmd.setAttr(file + ".fileTextureName", value, type="string")

	return file


def resetAttribute():
	cmd.setAttr('R_UberMat.diffuse', 1)
	cmd.setAttr('R_UberMat.diffuseColor', 0.05285, 0.298014, 0.303, type='double3')
	cmd.setAttr('R_UberMat.diffuseWeight', 1)
	cmd.setAttr('R_UberMat.diffuseRoughness', 1)
	cmd.setAttr('R_UberMat.useShaderNormal', 1)
	cmd.setAttr('R_UberMat.diffuseNormal', 1, 1, 1, type='double3')
	cmd.setAttr('R_UberMat.backscatteringWeight', 0)
	cmd.setAttr('R_UberMat.separateBackscatterColor', 0)
	cmd.setAttr('R_UberMat.backscatteringColor', 0.5, 0.5, 0.5, type='double3')

	cmd.setAttr('R_UberMat.reflections', 1)
	cmd.setAttr('R_UberMat.reflectColor', 1, 1, 1, type='double3')
	cmd.setAttr('R_UberMat.reflectWeight', 1)
	cmd.setAttr('R_UberMat.reflectRoughness', 0.119)
	cmd.setAttr('R_UberMat.reflectAnisotropy', 0)
	cmd.setAttr('R_UberMat.reflectAnisotropyRotation', 0)
	cmd.setAttr('R_UberMat.reflectUseShaderNormal', 1)
	cmd.setAttr('R_UberMat.reflectNormal', 1, 1, 1, type='double3')

	cmd.setAttr('R_UberMat.reflectMetalMaterial', 0)
	cmd.setAttr('R_UberMat.reflectIOR', 1.5)
	cmd.setAttr('R_UberMat.reflectMetalness', 0)

	cmd.setAttr('R_UberMat.refraction', 1)
	cmd.setAttr('R_UberMat.refractColor', 0.22, 0.957, 0.794, type='double3')
	cmd.setAttr('R_UberMat.refractWeight', 1)
	cmd.setAttr('R_UberMat.refractRoughness', 0)
	cmd.setAttr('R_UberMat.refractLinkToReflect', 0)
	cmd.setAttr('R_UberMat.refractIor', 1.5)
	cmd.setAttr('R_UberMat.refractThinSurface', 0)
	cmd.setAttr('R_UberMat.refractAbsorptionDistance', 0)
	cmd.setAttr('R_UberMat.refractAbsorbColor', 0, 0, 0, type='double3')
	cmd.setAttr('R_UberMat.refractAllowCaustics', 1)

	cmd.setAttr('R_UberMat.clearCoat', 0)
	cmd.setAttr('R_UberMat.coatColor', 1, 1, 1, type='double3')
	cmd.setAttr('R_UberMat.coatWeight', 1)
	cmd.setAttr('R_UberMat.coatRoughness', 0.5)
	cmd.setAttr('R_UberMat.coatIor', 1.5)
	cmd.setAttr('R_UberMat.coatUseShaderNormal', 0)
	cmd.setAttr('R_UberMat.coatNormal', 1, 1, 1, type='double3')
	cmd.setAttr('R_UberMat.coatThickness', 1)
	cmd.setAttr('R_UberMat.coatTransmissionColor', 1, 1, 1, type='double3')

	cmd.setAttr('R_UberMat.emissive', 0)
	cmd.setAttr('R_UberMat.emissiveWeight', 1)
	cmd.setAttr('R_UberMat.emissiveColor', 1, 1, 1, type='double3')
	cmd.setAttr('R_UberMat.emissiveIntensity', 1)
	cmd.setAttr('R_UberMat.emissiveDoubleSided', 0)

	cmd.setAttr('R_UberMat.sssEnable', 0)
	cmd.setAttr('R_UberMat.sssWeight')
	cmd.setAttr('R_UberMat.sssUseDiffuseColor', 0)
	cmd.setAttr('R_UberMat.volumeScatter', 0.436, 0.227, 0.131, type='double3')
	cmd.setAttr('R_UberMat.subsurfaceRadius0', 3.67)
	cmd.setAttr('R_UberMat.subsurfaceRadius1', 1.37)
	cmd.setAttr('R_UberMat.subsurfaceRadius2', 0.68)
	cmd.setAttr('R_UberMat.scatteringDirection', 0)
	cmd.setAttr('R_UberMat.multipleScattering', 1)

	cmd.setAttr('R_UberMat.transparencyEnable', 0)
	cmd.setAttr('R_UberMat.transparencyLevel', 1)
	cmd.setAttr('R_UberMat.normalMapEnable', 1)

	try:
		cmd.connectAttr('RPRNormal3.out', 'R_UberMat.normalMap', force=True)
	except:
		pass

	cmd.setAttr('file13.fileTextureName', 'sourceimages/normal_normalmap.png', type='string')
	cmd.setAttr('R_UberMat.displacementEnable', 0)
	cmd.setAttr('R_UberMat.displacementMap', 0, 0, 0, type='double3')
	cmd.setAttr('R_UberMat.displacementMin', 13.986)
	cmd.setAttr('R_UberMat.displacementMax', 23.776)
	cmd.setAttr('R_UberMat.displacementSubdiv', 4)
	cmd.setAttr('R_UberMat.displacementCreaseWeight', 0)
	cmd.setAttr('R_UberMat.displacementBoundary', 1)