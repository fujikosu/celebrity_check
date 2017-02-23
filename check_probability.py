import http.client, urllib.request, urllib.parse, urllib.error, base64, json

SUBSCRIPTION_KEY = "Your key"

# Query the face and get analized data
def detect_face(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '%s' % SUBSCRIPTION_KEY
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        # 'returnFaceAttributes': '{string}',
    })

    body = """{'url': '%s'}""" % (url)

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Register a face to Face API
def add_face(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '%s' % SUBSCRIPTION_KEY,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'userData': url,
        # 'targetFace': '{string}',
    })

    body = """{'url': '%s'}""" % (url)

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/facelists/celebrity_list/persistedFaces?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Query the face 
def get_similar_faces(face_id):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '%s' % SUBSCRIPTION_KEY
    }

    params = urllib.parse.urlencode({
    })

    body = """{'faceId': '%s', 
                "faceListId":"your list name", 
                "maxNumOfCandidatesReturned":10,
                "mode": "matchFace"}""" % (face_id)

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Get similarity percentages with face ids
def list_similar_face(url):
    data = detect_face(url)
    face_id = json.loads(data.decode('utf-8'))[0]["faceId"]
    print(get_similar_faces(face_id))


def main():
    data = detect_face("")
    # print(data.decode('utf-8'))
    json_data = json.loads(data.decode('utf-8'))[0]
    face_id = json_data["faceId"]
    face_rec = json_data["faceRectangle"]

    add_face_data = add_face("")
    print(add_face_data)
    added_face_id = json.loads(add_face_data.decode('utf-8'))["persistedFaceId"]

    list_similar_face("")

if __name__ == '__main__':
    main()