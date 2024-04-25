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
        while True:
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

                print(
                    f"Record successfully created with id={result[0]}, seq={result[1]} and seq_type={result[2]} by {result[3]}.")

                user_input = input(
                    "Hit <Enter> if you want to create another entry or type Exit to leave to the main menu...")
                if user_input.lower() == "exit":
                    break

            except ValueError as exc:
                print(exc)
                exitCmd = input("Please hit enter to try again or type 'exit' to leave... ")
                if exitCmd.lower() == "exit":
                    break

    def _delete_existing_entry(self):
        while True:
            print("""
            These are the entries currently available in the Database
            """)
            select_all_sql = "SELECT ID, SEQ_TYPE, SEQ, CREATOR FROM BIOSEQ"
            self.dbcursor.execute(select_all_sql)
            results = self.dbcursor.fetchall()
            available_ids = []
            for result in results:
                print(f"id='{result[0]}'.....'{result[2]}'")
                available_ids.append(result[0])

            user_entry_to_delete = input("Please provide the ID of the entry you want to delete... ")
            while not user_entry_to_delete.isnumeric() or int(user_entry_to_delete) not in available_ids:
                user_entry_to_delete = input(
                    f"The provided input {user_entry_to_delete} is not valid because its either not numeric or not "
                    f"available, please provide a numeric one or type 'Exit' to leave...")
                if user_entry_to_delete.lower() == "exit":
                    return
            delete_entry_sql = "DELETE FROM BIOSEQ WHERE ID=%s"
            self.dbcursor.execute(delete_entry_sql, (user_entry_to_delete,))
            print(f"Entry with ID={user_entry_to_delete} is now deleted")
            user_input = input(
                "Hit <Enter> if you want to delete another entry or type Exit to leave to the main menu...")
            if user_input.lower() == "exit":
                break

    def _print_existing_entry(self):
        while True:
            select_all_sql = "SELECT SEQ, SEQ_TYPE, CREATOR, ID FROM BIOSEQ"
            self.dbcursor.execute(select_all_sql)
            results = self.dbcursor.fetchall()
            bio_seq_list = []
            for result in results:
                bio_seq_cur = BioSeq(result[0], result[1], result[2], result[3])
                bio_seq_list.append(bio_seq_cur)
            available_ids = [s.ident for s in bio_seq_list]
            print(f"""
            Currently the following entries are available in the database:
            {[e for e in available_ids]}
            """)
            user_entry_to_print = input("Please provide the ID of the entry you want to print... ")
            while not user_entry_to_print.isnumeric() or int(user_entry_to_print) not in available_ids:
                user_entry_to_delete = input(
                    f"The provided input {user_entry_to_print} is not valid because its either not numeric or not "
                    f"available, please provide a numeric one or type 'Exit' to leave...")
                if user_entry_to_delete.lower() == "exit":
                    return
            bio_seq_to_print_f = filter(lambda b: b.ident == int(user_entry_to_print), bio_seq_list)
            bio_seq_to_print = list(bio_seq_to_print_f)[0]
            bio_seq_to_print.print_info()
            user_input = input(
                "Hit <Enter> if you want to print another entry or type Exit to leave to the main menu...")
            if user_input.lower() == "exit":
                break

    def execute_action(self, user_input):
        sanitized_user_input = _validate_input(user_input)
        if sanitized_user_input == 1:
            self._create_new_entry()
        elif sanitized_user_input == 2:
            self._delete_existing_entry()
        elif sanitized_user_input == 3:
            self._print_existing_entry()
