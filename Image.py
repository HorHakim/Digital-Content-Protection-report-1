#include:utf-8
"""
Author : Horairy Hakim
email : hakim.horairy@telecom-sudparis.eu
Tel : 07 69 22 52 55
"""
import re
import numpy
import random
import cv2

class Image:
	def __init__(self, pathImage=None, image=None, tableOfSubstitution=None):
		
		self.pathImage = pathImage
		
		if type(image) == numpy.ndarray:
			self.image=image
		else:
			self.image = cv2.imread(pathImage, cv2.IMREAD_GRAYSCALE)

		self.tableOfSubstitution = tableOfSubstitution

##########################################################################################################################################################
####################################################      --- Chiffre de César ---     ###################################################################
##########################################################################################################################################################


	def caesarCipherOnImage(self, key, pathImageEncrypted=None):
		# Ajout de la clef  
		imageEncrypted = self.image + numpy.ones(shape=self.image.shape, dtype=numpy.uint8) * key
		
		# remise des pixels dans l'interval [0, 255]
		for line in range(imageEncrypted.shape[0]):
			for column in range(imageEncrypted.shape[1]):

				if imageEncrypted[line][column] > 255 : 
					imageEncrypted[line][column] %= 256
				if imageEncrypted[line][column] < 0:
					imageEncrypted[line][column] %= 256

		# retour de l'objet + (enregistrement de l'image si un chemin est donné en entrée de la fonction)
		if pathImageEncrypted:
			cv2.imwrite(pathImageEncrypted, imageEncrypted)
			return Image(pathImage=pathImageEncrypted)
		else:
			return Image(pathImage=pathImageEncrypted, image=imageEncrypted)



	def inverseCaesarCipherOnImage(self, key, pathImageEncrypted=None): 
		""" La clef pour décrypté une image chiffrée par décallage est 256-key """
		return self.caesarCipherOnImage(key=256-key, pathImageEncrypted=None)


################################################################################################################################################
################################################      --- Codage par substitution ---     ######################################################
################################################################################################################################################
	

	def generateTableOfSubstitution(valueMin=0, valueMax=256):
		
		""" A chaque indice dans [valueMin, valueMax] on assigne 
					aléatoirement et de façon unique une valeur dans[valueMin, valueMax]"""

		initialValues = [k for k in range(valueMin,valueMax)]
		
		substituedValues = [k for k in range(valueMin,valueMax)]
		random.shuffle(substituedValues)

		tableOfSubstitution = dict(zip(initialValues, substituedValues))
		return tableOfSubstitution
	generateTableOfSubstitution = staticmethod(generateTableOfSubstitution)



	def codageBySubstitution(self, pathImageEncrypted=None):
		
		imageCodeBySubsitution = numpy.zeros(shape=self.image.shape, dtype=numpy.uint8)
		tableOfSubstitution = Image.generateTableOfSubstitution(valueMin=0, valueMax=256)

		for line in range(self.image.shape[0]):
			for column in range(self.image.shape[1]):
				imageCodeBySubsitution[line][column] = tableOfSubstitution[self.image[line][column]]

		if pathImageEncrypted:
			cv2.imwrite(pathImageEncrypted, imageCodeBySubsitution)
			return Image(pathImage=pathImageEncrypted, tableOfSubstitution=tableOfSubstitution)
		else:
			return Image(pathImage=pathImageEncrypted, image=imageCodeBySubsitution, tableOfSubstitution=tableOfSubstitution)



	def inverseCodageBySubstitution(self, tableOfSubstitution, pathImageEncrypted=None):
		inverseTableOfSubstitution = {substituedValues: initialValues for initialValues, substituedValues in tableOfSubstitution.items()}
		inverseImageCodedBySubstitution = numpy.zeros(shape=self.image.shape, dtype=numpy.uint8)

		for line in range(self.image.shape[0]):
			for column in range(self.image.shape[1]):
				inverseImageCodedBySubstitution[line][column] = inverseTableOfSubstitution[self.image[line][column]]

		if pathImageEncrypted:
			cv2.imwrite(pathImageEncrypted, inverseImageCodedBySubstitution)
			return Image(pathImage=pathImageEncrypted, tableOfSubstitution=None)
		else:
			return Image(pathImage=pathImageEncrypted, image=inverseImageCodedBySubstitution, tableOfSubstitution=None)


################################################################################################################################################
####################################      --- Stéganographie : Codage bit de poids faible ---     ##############################################
################################################################################################################################################

	def codageLSB(self, pathImageEncrypted=None, numberOfbits=1):

		imageCodedFollowingLSB1 = numpy.zeros(shape=self.image.shape, dtype=numpy.uint8)
		nbLines, nbColumns = self.image.shape


		# # #	Ce boût de code est déprecié, il est remplacé par un algorithme avec moins d'opérations à effectuer				# # #
		# # #	La mise à jour consiste à hard coder le codage LSB.																# # #
		# # #	Cette version déprecié (commentée) code une image en nuance de gris 512X512 en 7.6 sec.							# # #
		# # #	La version hard codée de la boucle for du codage LSB code une image en nuance de gris 512X512 en 6.2 sec.		# # #
		# # #	Ce gain est scalable avec la résolution de l'image à coder 														# # #
		# # #	La version dépreciée ne gère pas le LSB 2, celui ci est disponible dans la version hard codée					# # #
	
		# for line in range(nbLines):
		# 	for column in range(nbColumns):
		# 		if(line < nbLines / 2 and column < nbColumns / 2) or (line >= nbLines / 2 and column >= nbColumns / 2):
		# 			imageCodedFollowingLSB1[line][column] = self.image[line][column] - self.image[line][column]%2
		# 		else : 
		# 			imageCodedFollowingLSB1[line][column] = self.image[line][column] - self.image[line][column]%2 + 1

		if numberOfbits == 1 :
			parameters = (2**numberOfbits, [0, 1, 1, 0])

		elif numberOfbits == 2:
			parameters = (2**numberOfbits, [0, 1, 2, 3])


		middleOfTheImageFollowingX = nbColumns // 2
		middleOfTheImageFollowingY = nbLines // 2

		
		for line in range(0, middleOfTheImageFollowingY):
		 	for column in range(0, middleOfTheImageFollowingX):
		 		imageCodedFollowingLSB1[line][column] = self.image[line][column] - self.image[line][column]%parameters[0] + parameters[1][0]

		for line in range(0, middleOfTheImageFollowingY):
		 	for column in range(middleOfTheImageFollowingX, nbColumns):
		 		imageCodedFollowingLSB1[line][column] = self.image[line][column] - self.image[line][column]%parameters[0] + parameters[1][1]

		for line in range(middleOfTheImageFollowingY, nbLines):
			for column in range(0, middleOfTheImageFollowingX):
				imageCodedFollowingLSB1[line][column] = self.image[line][column] - self.image[line][column]%parameters[0] + parameters[1][2]
		
		for line in range(middleOfTheImageFollowingY, nbLines):
			for column in range(middleOfTheImageFollowingX, nbColumns):
				imageCodedFollowingLSB1[line][column] = self.image[line][column] - self.image[line][column]%parameters[0] + parameters[1][3]

		if pathImageEncrypted:
			cv2.imwrite(pathImageEncrypted, imageCodedFollowingLSB1)
			return Image(pathImage=pathImageEncrypted)
		else:
			return Image(pathImage=pathImageEncrypted, image=imageCodedFollowingLSB1)

	
	def hiddenImageLSB(codedImageByLSB, numberOfbits=1):
		
		"""Cette fonction renvoie l'image cachée par codage LSB1"""

		if numberOfbits==1:
			return Image(image=(codedImageByLSB.image.copy())%2 *255)
		elif numberOfbits==2:
			return Image(image=(codedImageByLSB.image.copy())%4 *64)

	hiddenImageLSB = staticmethod(hiddenImageLSB)


	def insertHiddenMessageInImage(self, messageString, pathImageEncrypted=None):

		numberOfPixelContainingMessage = Image.stringToBinary(str(len(messageString)*8))
		binaryStopMessage = Image.stringToBinary("stop")
		binaryMessage = Image.stringToBinary(messageString)

		# on charge une image avec que des pixels à valeur paire
		imageWithHiddenMessage = Image(image=self.image-self.image%2)
		
		nbLines, nbColumns = self.image.shape
		
		# on insert la taille du message en binaire dans l'image dans la ligne 0 de l'image
		for index, bit in enumerate(numberOfPixelContainingMessage + binaryStopMessage):
			imageWithHiddenMessage.image[index//nbColumns][index%nbColumns] += int(bit)

		# on insert le message en binaire dans l'image
		for index, bit in enumerate(binaryMessage):
			imageWithHiddenMessage.image[index//nbColumns+1][index%nbColumns] += int(bit)

		if pathImageEncrypted:
			cv2.imwrite(pathImageEncrypted, imageWithHiddenMessage)
			return imageWithHiddenMessage
		else:
			return imageWithHiddenMessage

	def getMessageFromImage(hiddenMessageOnImage):
		
		imageOfBinaryMessage = Image(image=(hiddenMessageOnImage.image.copy())%2)		

		metaDataLineZero = Image.binaryToString("".join([str(bit) for bit in imageOfBinaryMessage.image[0]]))

		numberOfPixelContainingMessage = int(metaDataLineZero[:metaDataLineZero.find("stop")])
		

		nbLines, nbColumns = hiddenMessageOnImage.image.shape

		binaryMessage = ""
		for indexPixel in range(numberOfPixelContainingMessage):
				binaryMessage += str(hiddenMessageOnImage.image[indexPixel//nbColumns + 1][indexPixel%nbColumns]%2)

		Message = Image.binaryToString(binaryMessage)
		return Message

	getMessageFromImage = staticmethod(getMessageFromImage)

########################################################################################################################################
####################################      --- Fonctions utiles ---     #################################################################
########################################################################################################################################

	def afficherImage(self, nameWindow="nameWindow"):
		cv2.imshow(nameWindow, self.image)
		cv2.waitKey(0)
		return None


	def stringToBinary(messageString, encoding='utf-8', errors='surrogatepass'):
		bits = bin(int.from_bytes(messageString.encode(encoding, errors), 'big'))[2:]
		return bits.zfill(8 * ((len(bits) + 7) // 8))
	stringToBinary = staticmethod(stringToBinary)


	def binaryToString(messageBits, encoding='utf-8', errors='surrogatepass'):
		n = int(messageBits, 2)
		return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
	binaryToString = staticmethod(binaryToString)

	def __sub__(self, otherImage):
		return Image(image=self.image - otherImage.image)
