import unittest
from datetime import datetime, timedelta

from flask_tutorial import app, db
from flask_tutorial.models import User, Post



class TestUserModelCase(unittest.TestCase):
    def setUp(self):
        # use an im-memory sqlite for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hasing(self):
        """
        Test the set_password() and check_password() method of User model.
        """
        user = User(username='bob')
        user.set_password('qwerty')

        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('qwerty'))

    def test_avatar(self):
        """
        Test that the user's avatar is same from the gravatar service.
        """
        user = User(username='john', email='john@test.com')
        gravatar_url = 'https://www.gravatar.com/avatar/5634ff13f953ebcb374ac8c349bcfcfe?d=identicon&s=128'
        self.assertEqual(user.avatar(128), (gravatar_url))

    def test_follow(self):
        """
        Test if user2 can follow or unfollow user1.
        """
        user1 = User(username='bob', email='bob@test.com')
        user2 = User(username='john', email='john@test.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        # user1 is not following anyone and do not have followers
        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user1.followers.all(), [])

        # user1 is now following user2
        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, 'john')
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, 'bob')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    def test_follow_posts(self):
        """
        Test the followed posts of each user.
        Ex:
        user1 follows user2 and user3.
        user1 should see posts from user1 (include themselves), user2 and user3.
        user2 does not follow anyone. user2 should only see posts from themselves.
        """
        user1 = User(username='bob', email='bob@test.com')
        user2 = User(username='john', email='john@test.com')
        user3 = User(username='joe', email='joe@test.com')
        user4 = User(username='ann', email='ann@test.com')
        db.session.add_all([user1, user2, user3, user4])

        now = datetime.utcnow()
        post1 = Post(title='post a', body='post from bob', author=user1, timestamp=now + timedelta(seconds=1))
        post2 = Post(title='post b', body='post from john', author=user2, timestamp=now + timedelta(seconds=4))
        post3 = Post(title='post c', body='post from joe', author=user3, timestamp=now + timedelta(seconds=3))
        post4 = Post(title='post d', body='post from ann', author=user4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        # setup the followers:
        user1.follow(user2) # bob follows john
        user1.follow(user4) # bob follows ann
        user2.follow(user3) # john follows joe
        user3.follow(user4) # joe follows ann
        db.session.commit()

        # check the followed posts of each user
        fp1 = user1.followed_posts().all()
        fp2 = user2.followed_posts().all()
        fp3 = user3.followed_posts().all()
        fp4 = user4.followed_posts().all()
        self.assertEqual(fp1, [post2, post4, post1]) # bob's own post, john's post, ann's post
        self.assertEqual(fp2, [post2, post3]) # john's own post, joe's post
        self.assertEqual(fp3, [post3, post4]) # joe's own post, ann's post
        self.assertEqual(fp4, [post4]) # ann's own post. Ann is not following anyone

if __name__ == '__main__':
    unittest.main(verbosity=2)
