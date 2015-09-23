from asyncon.handlers import AsyncRequestHandler

if __name__ == '__main__':
    handler = AsyncRequestHandler()
    handler.load_from_csv('alexa.csv', 400)
    handler.run()
