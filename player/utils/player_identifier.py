import os
import requests
import json


class PlayerIdentifier:
    BASE_URI = os.getenv('FACE_BASE_URI')
    SUBSCRIPTION_KEY = os.getenv('FACE_SUBSCRIPTION_KEY')

    PERSON_GROUP_ID = 'yb-players'

    @classmethod
    def __delete_person_group(cls):
        url = cls.BASE_URI + '/persongroups/' + cls.PERSON_GROUP_ID
        headers = {
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }
        r = requests.delete(url, data=None, headers=headers)
        if r.text:
            print(r.json())

    @classmethod
    def __create_person_group(cls):
        url = cls.BASE_URI + '/persongroups/' + cls.PERSON_GROUP_ID
        payload = {
            'name': cls.PERSON_GROUP_ID
        }
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }

        r = requests.put(url, data=json.dumps(payload), headers=headers)
        if r.text:
            res = r.json()
            if res['error']['code'] != 'PersonGroupExists':
                return r.json()

    @classmethod
    def __create_person_in_person_group(cls, person_name):
        url = cls.BASE_URI + '/persongroups/' + cls.PERSON_GROUP_ID + '/persons'
        payload = {
            'name': person_name
        }
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }

        r = requests.post(url, data=json.dumps(payload), headers=headers)

        return r.json()

    @classmethod
    def __add_face_to_person_in_person_group(cls, person_id, image_url):
        url = cls.BASE_URI + '/persongroups/' + cls.PERSON_GROUP_ID + '/persons/' + person_id + '/persistedFaces'
        payload = {
            'url': image_url
        }
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }

        r = requests.post(url, data=json.dumps(payload), headers=headers)

        return r.json()

    @classmethod
    def __train_person_group(cls):
        url = cls.BASE_URI + '/persongroups/' + cls.PERSON_GROUP_ID + '/train'
        headers = {
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }

        r = requests.post(url, data=None, headers=headers)

        if r.text:
            return r.json()

    @classmethod
    def __detect_faces(cls, image):
            image_string = image.read()

            url = cls.BASE_URI + '/detect'
            payload = image_string
            headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
            }

            r = requests.post(url, data=payload, headers=headers)

            return r.json()

    @classmethod
    def __identify_faces_in_image(cls, image):
        faces = cls.__detect_faces(image)
        face_ids = []
        print(faces)
        for face in faces:
            face_ids.append(face['faceId'])

        url = cls.BASE_URI + '/identify'
        payload = {
            'faceIds': face_ids,
            'personGroupId': cls.PERSON_GROUP_ID
        }
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }

        r = requests.post(url, data=json.dumps(payload), headers=headers)

        return r.json()

    @classmethod
    def __get_person_with_person_id(cls, persisted_person_id):
        url = cls.BASE_URI + '/persongroups/' + cls.PERSON_GROUP_ID + '/persons/' + persisted_person_id
        headers = {
            'Ocp-Apim-Subscription-Key': cls.SUBSCRIPTION_KEY
        }

        r = requests.get(url, data=None, headers=headers)

        return r.json()

    @classmethod
    def create_and_train_person_group(cls, people):
        # Create PersonGroup
        cls.__delete_person_group()
        err = cls.__create_person_group()
        if err:
            raise Exception(err)
        else:
            print('PersonGroup with id "' + cls.PERSON_GROUP_ID + '" created')

        # Create People in PersonGroup
        for person in people:
            created_person = cls.__create_person_in_person_group(person['name'])
            if created_person.get('error', None):
                print(created_person['error'])
                raise Exception(created_person['error'])
            else:
                print('*****')
                print('Person "' + person['name'] + '" with id "' + created_person['personId'] + '" created')
            faces_count = 0

            # Add Faces to Person
            for face in person['faces']:
                created_face = cls.__add_face_to_person_in_person_group(created_person['personId'], face['url'])
                if created_face.get('error', None):
                    if person['name'] == 'Nicolas Moumi Ngamaleu' \
                            or person['name'] == 'Roger Assalé' \
                            or person['name'] == 'Jean-Pierre Nsame'\
                            or person['name'] == 'Thorsten Schick'\
                            or person['name'] == 'Ulisses Garcia'\
                            or person['name'] == 'Sékou Sanogo':
                        print('Is Azure racist? Hmmmmm...')
                    else:
                        print(created_face['error'])
                        raise Exception(created_face['error'])
                else:
                    face['persistedFaceId'] = created_face['persistedFaceId']
                    faces_count += 1

            if faces_count > 0:
                if faces_count == 1:
                    print(str(faces_count) + ' face added')
                else:
                    print(str(faces_count) + ' faces added')

        print('*****')
        err = cls.__train_person_group()
        if err:
            print(err)
            raise Exception(err)
        else:
            print('PersonGroup with id ' + cls.PERSON_GROUP_ID + ' successfully trained')
            return people

    @classmethod
    def get_person_from_image(cls, image):
        names = []
        faces = cls.__identify_faces_in_image(image)
        for face in faces:
            candidates = face['candidates']
            for candidate in candidates:
                person_id = candidate['personId']
                person = cls.__get_person_with_person_id(person_id)
                names.append(person['name'])
        return names
