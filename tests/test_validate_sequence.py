import unittest
from sample.bioseq import BioSeq


class ValidateSequence(unittest.TestCase):

    def testNonValidSequenceThrowsError(self):
        bioseq = BioSeq("ACTGATTCA", "KNL", "creator")
        with self.assertRaisesRegex(ValueError, "The sequence type 'KNL' is not valid"):
            bioseq.validate()

    def testValidDNASequenceDoesNotThrowError(self):
        BioSeq("ACTGATTGA", "DNA", "creator")
        BioSeq("ACUGAUUA", "RNA", "creator")

    def testNonValidRNASequenceThrowsError(self):
        bioseq = BioSeq("ACTGATTGA", "RNA", "creator")
        with self.assertRaisesRegex(ValueError, "Thymine is not a valid base in an RNA-Sequence"):
            bioseq.validate()

    def testNonValidBioSeqThrowsError(self):
        bioseq = BioSeq("ACTGHJOGGCCCTAASDF", "RNA", "creator")
        with self.assertRaises(ValueError) as ve:
            bioseq.validate()
        self.assertEqual(
            "The sequence is not valid, because there are invalid bases included: ['H', 'J', 'O', 'S', 'D', 'F']",
            ve.exception.args[0])
