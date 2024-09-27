class PageMethod:
    def __init__(self, page, method_name, *args, **kwargs):
        self.page = page
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

    async def call(self):
        method = getattr(self.page, self.method_name)
        return await method(*self.args, **self.kwargs)


# Example usage of calling any method on the page object (Playwright)
async def perform_page_operation(page, method_name, *args, **kwargs):
    """
    Dynamically performs an operation on the Playwright page.
    Example operations could be 'click', 'goto', 'evaluate', etc.
    """
    method = PageMethod(page, method_name, *args, **kwargs)
    return await method.call()

