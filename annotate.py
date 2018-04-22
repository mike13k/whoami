import httplib
import json
import urllib

subscription_key = '3ae27aba10974d98a0546726c5ff9a55'
assert subscription_key

def annotate_image(image):
    headers = {'Ocp-Apim-Subscription-Key': "3ae27aba10974d98a0546726c5ff9a55",
               'Content-type': 'application/octet-stream'}

    params = urllib.urlencode({
        'returnFaceAttributes': 'smile'
    })

    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, image, headers)

    response = conn.getresponse()
    data = response.read().decode('utf-8')
    jsonData = json.loads(data)
    # data = data[1:-1]
    print(jsonData)
    if jsonData != []:
        if 'error' not in jsonData:
            face = jsonData[0]
            if 'error' not in face:
                attributes = face["faceAttributes"]
                conn.close()
                print attributes["smile"]
                if attributes["smile"] > 0.6:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # response = requests.post(face_api_url, params=params, headers=headers, data=image_url)
    # faces = response.json()
    #
    # image_file = BytesIO(requests.get(image_url).content)
    # image = Image.open(image_file)
    #
    # plt.figure(figsize=(8,8))
    # ax = plt.imshow(image, alpha=0.6)
    # for face in faces:
    #     fr = face["faceRectangle"]
    #     fa = face["faceAttributes"]
    #     return fa["smile"]
    # #     origin = (fr["left"], fr["top"])
    # #     p = patches.Rectangle(origin, fr["width"], \
    # #                           fr["height"], fill=False, linewidth=2, color='b')
    # #     ax.axes.add_patch(p)
    # #     plt.text(origin[0], origin[1], "%d, %d"%(fa["smile"], fa["smile"]), \
    # #              fontsize=20, weight="bold", va="bottom")
    # # plt.axis("off")