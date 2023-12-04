from importlib.resources import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('setting', views.setting, name="setting"),
    path('writing-article', views.write_article, name="writing-article"),
    path('publish-article', views.publish_article, name="publish-article"),
    path('save-draft', views.save_draft, name="save-draft"),
    path('read_article/<str:id>', views.read_article, name="read_article"),
    path('library', views.acccess_library, name="library"),
    path('read_book/<str:id>', views.read_book, name="read_book"),
    path('make-note', views.make_note, name="make-note"),
    path('update_note', views.update_note, name="update_note"),
    path('post-comment', views.post_comment, name="post-comment"),
    path('profile/<str:pk>', views.view_profile, name="profile"),
    path('follow', views.follow, name="follow"),
    path('follow-from-article', views.follow_from_article, name="follow-from-article"),
    path('draft-list/<str:pk>', views.draft_list, name="draft-list"),
    path('edit-article/<str:pk>', views.edit_article, name="edit-article"),
    path('publish-draft', views.publish_draft, name="publish-draft"),
    path('update-draft', views.update_draft, name="update-draft"),
    path('remove-article/<str:pk>', views.remove_article, name="remove-article"),
    path('my-setting/<str:pk>', views.my_setting, name="my-setting"),
    path('edit-setting/<str:pk>', views.edit_setting, name="edit-setting"),
    path('update-setting', views.update_setting, name="update-setting"),
    path('verify-email', views.verify_email, name="verify-email"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('like-article', views.like_article, name="like-article"),
    path('search', views.search, name="search")
]