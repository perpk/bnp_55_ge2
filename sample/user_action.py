from bioseq import BioSeq


def _validate_input(user_input):
    if not user_input.isnumeric():
        raise ValueError(f"Expected a numeric input, yet '{user_input}' is not numeric")

    sanitized_user_input = int(user_input)
    if sanitized_user_input not in [1, 2, 3, 4]:
        raise ValueError(f"The input '{user_input}' does not correspond to any valid menu entries")

    return sanitized_user_input


class UserAction:

    def __init__(self, dbcursor):
        self.dbcursor = dbcursor

    def _create_new_entry(self):
        errors = False

        while not errors:
            print("""
            Please provide the attributes of the sequence record to create
            """)

            seq_type = input("Sequence type => ")
            seq = input("Sequence => ")
            creator = input("Creator => ")
            bioseq = BioSeq(seq, seq_type, creator)
            try:
                bioseq.validate()
                insert_sql = "INSERT INTO BIOSEQ (SEQ_TYPE, SEQ, CREATOR) VALUES (%s, %s, %s)"
                values = (bioseq.seq_type, bioseq.seq, bioseq.creator)
                self.dbcursor.execute(insert_sql, values)
                entry_row_id = self.dbcursor.lastrowid

                select_last_sql = "SELECT ID, SEQ_TYPE, SEQ, CREATOR FROM BIOSEQ WHERE ID=%s"
                self.dbcursor.execute(select_last_sql, (entry_row_id,))
                result = self.dbcursor.fetchone()

                print(f"Record successfully created with id={result[0]}, seq={result[1]} and seq_type={result[2]} by {result[3]}.")

                user_input = input("Hit <Enter> if you want to create another entry or type Exit to leave to the main menu...")
                if user_input.lower() == "exit":
                    break

            except ValueError as exc:
                print(exc)
                errors = True
                exit = input("Please hit enter to try again or type 'exit' to leave... ")
                if (exit.lower() == "exit"):
                    break

    def _delete_existing_entry(self):
        pass

    def _print_existing_entry(self):
        pass

    def execute_action(self, user_input):
        sanitized_user_input = _validate_input(user_input)
        if sanitized_user_input == 1:
            self._create_new_entry()
        elif sanitized_user_input == 2:
            self._delete_existing_entry()
        elif sanitized_user_input == 3:
            self._print_existing_entry()
