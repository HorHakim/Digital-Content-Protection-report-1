#include:utf-8
"""
Author : Horairy Hakim
Email : hakim.horairy@telecom-sudparis.eu
Tel : 07 69 22 52 55
"""
from Image import *

lena = Image(pathImage="images/Baboon.png")
lena.afficherImage(nameWindow="lena")

caesarCipherOnLena = lena.caesarCipherOnImage(key=70)
caesarCipherOnLena.afficherImage(nameWindow="Caesar cipher on Lena")


caesarCipherOnLena = lena.caesarCipherOnImage(key=158)
caesarCipherOnLena.afficherImage(nameWindow="Caesar cipher on Lena")

caesarCipherOnLena = lena.caesarCipherOnImage(key=220)
caesarCipherOnLena.afficherImage(nameWindow="Caesar cipher on Lena")


inverseCaesarCipherOnLena = caesarCipherOnLena.inverseCaesarCipherOnImage(key=150)
inverseCaesarCipherOnLena.afficherImage(nameWindow="Inverse Caesar cipher on Lena")

codageBySubstitutionOnLena = lena.codageBySubstitution()
codageBySubstitutionOnLena.afficherImage(nameWindow="Codage by substitution on Lena")


inverseCodageBySubstitutionOnLena = codageBySubstitutionOnLena.inverseCodageBySubstitution(tableOfSubstitution = codageBySubstitutionOnLena.tableOfSubstitution)
inverseCodageBySubstitutionOnLena.afficherImage(nameWindow="Inverse codage by substitution on Lena")


codageLBS1OnLena = lena.codageLSB(numberOfbits=1)
codageLBS1OnLena.afficherImage(nameWindow="Codage LSB 1 on Lena")

hiddenImage = Image.hiddenImageLSB(codageLBS1OnLena, numberOfbits=1)
hiddenImage.afficherImage(nameWindow="Hidden image LSB 1")


codageLBS2OnLena = lena.codageLSB(numberOfbits=2)
codageLBS2OnLena.afficherImage(nameWindow="Codage LSB 2 on Lena")

hiddenImage = Image.hiddenImageLSB(codageLBS2OnLena, numberOfbits=2)
hiddenImage.afficherImage(nameWindow="Hidden image LSB 2")

hiddenMessageOnImage = lena.insertHiddenMessageInImage("Albert Einstein né le 14 mars 1879 à Ulm, dans le Wurtemberg, et mort le 18 avril 1955 à Princeton, dans le New Jersey, est un physicien théoricien.") # on insert du texte dans une image
hiddenMessageOnImage.afficherImage(nameWindow="hide Message in Image") # on affiche l'image sur laquelle le message est caché
print(Image.getMessageFromImage(hiddenMessageOnImage)) # on affiche le message caché