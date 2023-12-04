from .models import *

def getFollowerAndFollowing(id):
    following = Follow.objects.filter(follower_id=id)
    following_count = len(following)
    followings = []
    for f in following:
        following_user = User.objects.get(id = f.following_id)
        followings.append({
            'id' : following_user.id,
            'name' : following_user.getFullName(),
            'handle' : following_user.handle
        })
        
    follower = Follow.objects.filter(following_id=id)
    follower_count = len(follower)
    followers = []
    for f in follower:
        follower_user = User.objects.get(id = f.follower_id)
        # print(user)
        followers.append({
            'id' : follower_user.id,
            'name' : follower_user.getFullName(),
            'handle' : follower_user.handle
        })

    context = {
        'followings': followings,
        'followers' : followers,
        'follower_count': follower_count,
        'following_count': following_count
    }
    
    return context