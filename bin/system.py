'''
Data Flow
                               + <--- (response) -------------------- +
                               |                                      ^
                               |                                      |
[Script] --- (request) ---> [Cache] --- (request) ---> [Storage] ---> +
   ^                           |
   |                           |
   + <--- (response) --------- +

'''


class Request(str):
    def __init__(self, method):
        # method is GET, DELETE, POST, PUT
        self.method = method
        self.no = 0

class Response(str):
    def __init__(self, method):
        # method is GET, DELETE, POST, PUT
        self.method = method
        self.no = 0 # response no is same as the request.no
        self.data = {}

    def assign(self, request):
        self.method=request.method
        self.no = request.no

class App(list):
    def __init__(self, cache):
        print('App init')
        self.cache = cache
        self.request_idx = 0

    def add_request(self, request):
        # prepare a list requests to execute on run
        self.request_idx += 1
        request.no = self.request_idx
        self.append(request)
        return self

    def request_handler(self, request):
        #print('  app request handler')
        print('    * app request {}'.format(request.method))

        if request.method == 'GET':
            #print('    * app request {}'.format(request.method))
            response =  self.cache.get(request)

        elif request.method == 'DELETE':
            #print('    * app request {}'.format(request.method))
            response =  self.cache.delete(request)

        elif request.method == 'POST':
            #print('    * app request {}'.format(request.method))
            response =  self.cache.post(request)

        elif request.method == 'PUT':
            print('    * app request {}'.format(request.method))
            response =  self.cache.put(request)

        else:
            raise Exception('Unknown request method ()'.format(request.method))


        return self

    def response_handler(self, response):
        print('app response handler')
        pass

    def run(self):
        #print('app run')
        #request = Request('GET')
        #self.request_hander(request)
        print('run ', self)
        for request in self:
            response = self.request_handler(request)
            response = self.response_handler(response)

        return self

class Cache(dict):
    '''
    {
     1: {},
     2: {},
     3: {}
    }
    '''
    def __init__(self, storage):
        print('cache init')
        self.storage = storage
        self.request = None
        self.response = None

    def get(self, request): # aka get handler
        print('      * cache get')
        self.request = request

        self.response = self.response_hander(self.storage.get(request))
        return self.response

    def put(self, request): # aka put handler
        print('      * cache put')
        self.request = request
        self.response = self.response_hander(self.storage.put(request))
        return self.response

    def post(self, request): # aka post handler
        print('      * cache post')
        # is request.no in cache?

        self.request = request
        self.response = self.response_hander(self.storage.post(request))
        return self.response

    def delete(self, request): # aka delete handler
        print('      * cache delete')
        self.request = request
        self.response = self.response_hander(self.storage.delete(request))
        return self.response

    def response_hander(self, response):
        print('cache response handler')
        return response

class Storage(dict):
    # load everything
    def __init__(self):
        print('storage init')
        self.request=None
        self.response=None

    #def request_handler(self, request):
    #    # (request) ---> handler --> (response)
    #    response = Response()
    #    return response

    def get(self, request): # aka get handler
        print('storage get')
        return self.response

    def put(self, request): # aka put handler
        print('storage put')
        return self.response

    def post(self, request): # aka post handler
        print('storage post')
        return self.response

    def delete(self, request): # aka delete handler
        print('storage delete')
        return self.response

    def request_hander(self, request):
        print('storage request handler')

        if request.method == 'GET':
            response =  self.get(request)

        elif request.method == 'DELETE':
            response =  self.delete(request)

        elif request.method == 'POST':
            response =  self.post(request)

        elif request.methdon == 'PUT':
            response =  self.put(request)

        return self

def main():
    print('start storage')
    storage = Storage()
    cache = Cache(storage)
    app = App(cache).add_request(Request('POST'))
                    #.add_request(Request('GET'))\
                    #.add_request(Request('PUT'))\
                    #.add_request(Request('DELETE'))
    app.run()

if __name__ == "__main__":
    # execute as docker
    main()
