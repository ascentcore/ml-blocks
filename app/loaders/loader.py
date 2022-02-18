class Loader:

    def load_files(self, files):
        raise Exception('not implemented')

    def store(self):
        raise Exception('not implemented')

    def count(self):
        pass

    def clean(self):
        pass

    def load_page(self, page, count):
        pass

    def load_from_store(self):
        pass

    def export_content_types(self):
        pass

    async def load_request(self, request):
        pass