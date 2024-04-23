import re


def has_thymine_content(seq):
    return re.search('T', seq) != None

def has_uracil_content(seq):
    return re.search('U', seq) != None

def validate_only_valid_bases(seq):
    seq_list = [char for char in seq]
    valid_bases = {'A', 'G', 'C', 'T', 'U'}
    not_valid_bases = []
    for base in seq_list:
        if base not in valid_bases:
            not_valid_bases.append(base)
    if not_valid_bases:
        raise ValueError(f"The sequence is not valid, because there are invalid bases included: {not_valid_bases}")


class BioSeq:
    """
    B. A Class to represent an RNA or DNA Sequence
    """

    ## i. The Constructor
    def __init__(self, seq, seq_type, creator):
        self.seq = seq
        self.seq_type = seq_type
        self.creator = creator

    ## ii. A print Method to display all fields with their respective values when called
    def print_info(self):
        print(f"""
        sequence = {self.seq}
        sequence type = {self.seq_type}
        creator = {self.creator}
        """)

    ## iii. A validation Method which
    ### a) Checks whether a given sequence contains only the base-alphabet A,T,C,G,U
    ### b) If the type is either RNA or DNA
    ### c) In case of RNA thymine doesn't exist
    ### d) In case of DNA uracil doesn't exist
    def validate(self):
        validate_only_valid_bases(self.seq)
        if self.seq_type != "RNA" and self.seq_type != "DNA":
            raise ValueError(f"The sequence type '{self.seq_type}' is not valid")
        if self.seq_type == "RNA" and has_thymine_content(self.seq):
            raise ValueError("Thymine is not a valid base in an RNA-Sequence")
        if self.seq_type == "DNA" and has_uracil_content(self.seq):
            raise ValueError("Uracil is not a valid base in a DNA-Sequence")



