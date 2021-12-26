from News_Portal.models import *


u1 = User.objects.get(username='ChtoNibut')

u2 = User.objects.get(username='User_4')


Author.objects.create(user=u1)

Author.objects.create(user=u2)



Category.objects.create(name='enotiki')

Category.objects.create(name='kotiki')

Category.objects.create(name='sovushki')

Category.objects.create(name='raznoe')


author1 = Author.objects.get(id=1)

author2 = Author.objects.get(id=2)


Post.objects.create(author=author1, post_type='AR', heading='Котики vs совушки', text='Весна пришла. Коты дерутся. А совы - нет!')

Post.objects.create(author=author2, post_type='AR', heading='Как нет винишка?', text='Всё выпили. 10 лайфхаков, как жить дальше')

Post.objects.create(author=author1, post_type='NW', heading='А у нас - Новый год!', text='Но это неточно...')


Post.objects.get(id=1).categories.add(Category.objects.get(id=2))

Post.objects.get(id=1).categories.add(Category.objects.get(id=3))

Post.objects.get(id=2).categories.add(Category.objects.get(id=1))

Post.objects.get(id=3).categories.add(Category.objects.get(id=4))


Comment.objects.create(post=Post.objects.get(id=1), user=Author.objects.get(id=2).user, text='МИМИМИ')

Comment.objects.create(post=Post.objects.get(id=2), user=Author.objects.get(id=1).user, text='многабукафф')

Comment.objects.create(post=Post.objects.get(id=3), user=Author.objects.get(id=1).user, text='...или точно...')

Comment.objects.create(post=Post.objects.get(id=2), user=Author.objects.get(id=2).user, text='ниасилел?')


Post.objects.get(id=1).like()

Post.objects.get(id=1).like()

Post.objects.get(id=2).like()

Post.objects.get(id=2).like()

Post.objects.get(id=2).like()

Post.objects.get(id=3).like()


Post.objects.get(id=1).dislike()

Post.objects.get(id=2).dislike()

Post.objects.get(id=3).dislike()

Post.objects.get(id=3).dislike()


Post.objects.get(id=1).rating

Post.objects.get(id=2).rating

Post.objects.get(id=3).rating


Comment.objects.get(id=1).like()

Comment.objects.get(id=1).like()

Comment.objects.get(id=3).like()

Comment.objects.get(id=3).like()

Comment.objects.get(id=3).like()

Comment.objects.get(id=4).like()


Comment.objects.get(id=1).dislike()

Comment.objects.get(id=2).dislike()


Comment.objects.get(id=1).rating

Comment.objects.get(id=2).rating

Comment.objects.get(id=3).rating

Comment.objects.get(id=4).rating


author1.update_rating()
author1.rating

author2.update_rating()
author2.rating

a = Author.objects.order_by('-rating')[:1]
a[0].username
a[0].rating

best_post = Post.objects.order_by('-rating').first()

result = {
	'publication_time': best_post.publication_time,
	'author_username': best_post.user.username,
	'rating': best_post.rating,
	'heading': best_post.heading,
	'preview': best_post.preview(),
}

Comment.objects.filter(post=best_post).values('time', 'user__username', 'rating', 'text')