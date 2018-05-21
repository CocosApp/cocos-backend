from requests import request, HTTPError
from django.core.files.base import ContentFile
from django.utils.text import slugify


def save_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs):
    if is_new and backend.name == "facebook":
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = user
            profile.picture.save(u'{0}_social.jpg'.format(slugify(user.email)), ContentFile(response.content))
            profile.save()
