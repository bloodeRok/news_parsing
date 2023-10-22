class StatusCodeException(Exception):
    def __init__(self, response):
        self.message = f"Something went wrong! Response status code now {response.status_code}."
        super().__init__(self.message)
