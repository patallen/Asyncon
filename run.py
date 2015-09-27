from asyncon.handlers import AsyncRequestHandler

if __name__ == '__main__':
    handler = AsyncRequestHandler()
    handler.load_from_csv('alexa.csv', 2000)
    handler.run()
    handler.get_results()
