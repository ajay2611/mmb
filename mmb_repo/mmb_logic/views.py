import json

from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from mmb_repo.mmb_logic.utils import check_for_session
from mmb_repo.users.models import *
from mmb_repo.mmb_data.models import *
from mmb_repo.bands.models import *
from mmb_repo.bands.utils import send_multiple_mails


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        result = json.dumps({'not_authenticated': True})
        return HttpResponse(result, 'application/json')

    return wrapper


def category_search(request):
    data = None
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=q)[:20]
        print "query result "
        print users
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username

            results.append(user_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_location(request):
    data = None
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=q)[:20]
        print "query result "
        print users
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username

            results.append(user_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@ajax_login_required
def inc_likes(request):
    success = False
    mimetype = 'application/json'

    # checking for band/user
    is_band, band_id = check_for_session(request)

    if request.is_ajax():
        song_id = request.GET.get('song_id')
        try:
            song_obj = Song.objects.get(id=song_id)

            # if band then creating Songlike object for band
            if is_band and band_id:
                band = Band.objects.get(id=band_id)
                SongLike.objects.create(band=band, song=song_obj)
            else:
                SongLike.objects.create(user=request.user, song=song_obj)

            song_obj.likes += 1
            song_obj.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success, 'like_count': song_obj.likes}), mimetype)

@ajax_login_required
def dec_likes(request):
    success = False
    mimetype = 'application/json'

    # checking for band/user
    is_band, band_id = check_for_session(request)

    if request.is_ajax():
        song_id = request.GET.get('song_id')
        try:
            song_obj = Song.objects.get(id=song_id)

            if is_band and band_id:
                band = Band.objects.get(id=band_id)
                # for now getting all objects and deleting it
                SongLike.objects.filter(band=band, song=song_obj).delete()
            else:
                # for now getting all objects and deleting it
                SongLike.objects.filter(user=request.user, song=song_obj).delete()
            song_obj.likes -= 1
            song_obj.save()
            success = True
        except:
            pass

        return HttpResponse(json.dumps({'success': success, 'like_count': song_obj.likes}), mimetype)

@ajax_login_required
def change_profile(request, id, type=None):
    if request.method == 'GET':
        if type == 'band':
            request.session['id'] = id
            request.session['is_band'] = True
            return HttpResponseRedirect(reverse('bands:view_band', args=[str(id), ]))
        else:
            username = request.user.username
            request.session['is_band'] = False
            request.session['id'] = None
            return HttpResponseRedirect(reverse('users:view_profile', args=[str(username), ]))


@ajax_login_required
def follow(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        followed_user_id = int(request.GET.get('user_id'))
        followed_user = get_user_model().objects.get(id =followed_user_id)
        user_followed_profile = Profile.objects.get(user=followed_user)
        user_profile = Profile.objects.get(user=user)
        try:
            UserFollowers.objects.create(follower=user, following=followed_user)
            user_followed_profile.followed_by_count += 1
            user_profile.following_count += 1
            user_profile.save()
            user_followed_profile.save()
            success = True
        except:
            pass

        return HttpResponse(json.dumps({'success': success,
                                        'followed_by_count': user_followed_profile.followed_by_count,
                                        'following_count': user_followed_profile.following_count}),
                            mimetype)


@ajax_login_required
def unfollow(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        followed_user_id = request.GET.get('user_id')
        followed_user = get_user_model().objects.get(id =followed_user_id)
        user_followed_profile = Profile.objects.get(user=followed_user)
        user_profile = Profile.objects.get(user=user)
        try:
            UserFollowers.objects.filter(follower=user, following=followed_user).delete()
            user_followed_profile.followed_by_count -= 1
            user_profile.following_count -= 1
            user_profile.save()
            user_followed_profile.save()
            success = True
        except:
            pass

        return HttpResponse(json.dumps({'success': success,
                                        'followed_by_count': user_followed_profile.followed_by_count,
                                        'following_count': user_followed_profile.following_count}),
                            mimetype)

@ajax_login_required
def unfollow_band(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        band_id = request.GET.get('band_id')
        band_obj = Band.objects.get(id=band_id)
        user_profile = Profile.objects.get(user=user)
        try:
            BandFollowers.objects.filter(follower=user, following_band=band_obj).delete()
            band_obj.follower_count -= 1
            user_profile.band_follow_count -= 1
            user_profile.save()
            band_obj.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success, 'band_follow_count': band_obj.follower_count}), mimetype)

@ajax_login_required
def follow_band(request):
    mimetype = 'application/json'
    user = request.user
    success = False
    if request.is_ajax():
        band_id = int(request.GET.get('band_id'))
        band_obj = Band.objects.get(id=band_id)
        user_profile = Profile.objects.get(user=user)
        try:
            BandFollowers.objects.create(follower=user, following_band=band_obj)
            band_obj.follower_count += 1
            user_profile.band_follow_count += 1
            user_profile.save()
            band_obj.save()
            success = True
        except:
            pass

    return HttpResponse(json.dumps({'success': success,'band_follow_count': band_obj.follower_count}), mimetype)

@ajax_login_required
def apply_vacancy(request):
    mimetype = 'application/json'
    success = False
    if request.is_ajax():
        band_id = int(request.GET.get('band_id'))
        inst = request.GET.get('inst')
        type = request.GET.get('type')
        inst_obj = Instrument.objects.get(instrument=inst)
        bv_obj = BandVacancy.objects.get(band=band_id, instrument=inst_obj, type=type)
        BandVacancyApplication.objects.create(band_vacancy=bv_obj, user=request.user)
        bandmember_objs = BandMember.objects.filter(band=band_id)
        sub = 'Vacancy Applied - {}'.format(inst)
        msg = '{} is interested in joining your band to play {}. Check your account at mmb.'.format(
            request.user.username, inst)
        member_list = []
        for bm_obj in bandmember_objs:
            member_list.append(bm_obj.member.email)

        send_multiple_mails(sub, msg, '', member_list)

    return HttpResponse(json.dumps({'success': success}), mimetype)


#
# @ajax_login_required
# def band_inc_likes(request):
#     success = False
#     mimetype = 'application/json'
#     if request.is_ajax():
#         band_song_id = request.GET.get('band_song_id')
#         band_song_obj = BandSong.objects.get(id=band_song_id)
#         band_song_obj.likes += 1
#         band_song_obj.save()
#         BandSongLike.objects.create(user=request.user, song=band_song_obj)
#         success = True
#
#     return HttpResponse(json.dumps({'success': success, 'like_count': band_song_obj.likes}), mimetype)
#
# @ajax_login_required
# def band_dec_likes(request):
#     success = False
#     mimetype = 'application/json'
#     if request.is_ajax():
#         band_song_id = request.GET.get('band_song_id')
#         try:
#             band_song_obj = Song.objects.get(id=band_song_id)
#             BandSongLike.objects.filter(user=request.user, song=band_song_obj).delete()
#             band_song_obj.likes -= 1
#             band_song_obj.save()
#             success = True
#         except:
#             pass
#
#     return HttpResponse(json.dumps({'success': success, 'like_count': band_song_obj.likes}), mimetype)
