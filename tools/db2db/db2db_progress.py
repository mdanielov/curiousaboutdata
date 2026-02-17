import json

class DB2DBProgress:
    progress = { 'export': {}, 'import': {}}
    file_name = None

    def __init__( self, a_file_name):
        self.file_name = a_file_name
        self.progress = DB2DBProgress.load(self.file_name)

    @classmethod
    def set_filename(cls, a_file_name):
        cls.file_name = a_file_name

    def load_progress(self):
        self.progress = DB2DBProgress.load( self.file_name)
    
    def has_seen_export_table(self, table_name):
        return False if self.progress.get('export').get(table_name) is None else True

    def has_seen_import_table(self, table_name):
        return False if self.progress.get('import').get(table_name) is None else True

    def has_seen_export_file(self, table_name, file_name):
        return self.has_seen_file( 'export', table_name, file_name)
    
    def has_seen_import_file(self, table_name, file_name):
        return self.has_seen_file( 'import', table_name, file_name)
    
    def has_seen_file(self, direction, table_name, file_name):
        direction_dict = self.progress.get(direction)
        if direction_dict is not None:
            files = direction_dict.get(table_name)
            if files is not None:
                return True if file_name in files else False
        return False

    def mark_export( self, table_name, file_name):
        if table_name not in self.progress['export']:
            self.progress['export'][table_name] = []
        self.progress['export'][table_name].append(file_name)

    def mark_import(self, table_name, file_name):
        if table_name not in self.progress['import']:
            self.progress['import'][table_name] = []
        self.progress['import'][table_name].append(file_name)

    def store(self):
        with open(self.file_name, 'w') as fout:
            json.dump(self.progress, fout)

    @staticmethod
    def save(obj, a_file_name):
        with open(a_file_name, 'w') as fout:
            json.dump(obj, fout)

    @staticmethod
    def load(a_file_name):
        try:
            with open(a_file_name, 'r') as fin:
                obj = json.load(fin)
            return obj
        except Exception as ex:
            return  DB2DBProgress.progress


