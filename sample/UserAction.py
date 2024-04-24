from bioseq import BioSeq

class UserAction:

    def __init__(self, dbcursor):
        self.dbcursor = dbcursor

    def _create_new_entry(self):
        errors = False

        while errors:
            print("""
            Please provide the attributes of the sequence record to create
            """)

            seq_type = input("Sequence type => ")
            seq = input("Sequence => ")
            creator = input("Creator => ")
            bioseq = BioSeq(seq, seq_type, creator)
            try:
                bioseq.validate()
                insert_sql = f"INSERT INTO BIOSEQ (SEQ_TYPE, SEQ, CREATOR) VALUES ({bioseq.seq_type}, {bioseq.seq}, {bioseq.creator})"
                self.dbcursor.execute(insert_sql)
            except ValueError as exc:
                print(exc)
                errors = True
                exit = input("Please hit enter to try again or type 'exit' to leave. ")
                if (exit.lower() == "exit"):
                    break

    def _delete_existing_entry(self):
        pass

    def _print_existing_entry(self):
        pass

    def _validate_input(self, user_input):
        if user_input not in [1, 2, 3, 4]:
            raise ValueError(f"The input {user_input} does not correspond to any valid menu entries")

    def determine_action(self, user_input):
        self._validate_input(user_input)
        if input == 1:
            self._create_new_entry()
        elif input == 2:
            self._delete_existing_entry()
        elif input == 3:
            self._print_existing_entry()
