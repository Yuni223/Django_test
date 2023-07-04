from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.contrib.auth.models import User
# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

        self.user_obama.is_staff = True
        self.user_obama.save()

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_python_kor = Tag.objects.create(name="파이썬 공부", slug="파이썬-공부")
        self.tag_python = Tag.objects.create(name="python", slug="python")
        self.tag_hello = Tag.objects.create(name="hello", slug="hello")

        # post 생성
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content='1등이 전부인 드러운 세상',
            category=self.category_programming,
            author=self.user_trump
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트 입니다.',
            content='category가 없는 경우',
            author=self.user_obama
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

        self.post_004 = Post.objects.create(
            title="Post Form 만들기",
            content="Post Form 페이지를 만듭시다.",
            category=self.category_music,
            author=self.user_obama
        )


    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        response = self.client.get(update_post_url)
        self.assertNotEquals(response.status_code, 200) # 로그인하지 않은 상태

        # 로그인이 되어있으나 작성자가 아닌 경우
        self.assertNotEquals(self.post_003.author, self.user_trump)
        # post_003은 obama가 작성함
        self.client.login(
            username=self.user_trump.username,
            password='somepassword',
        )
        response = self.client.get(update_post_url)
        self.assertEquals(response.status_code, 403)

        # 작성자가 접속하는 경우
        self.client.login(
            username=self.post_003.author.username,
            password='somepassword',
        )
        response = self.client.get(update_post_url)
        self.assertEquals(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 정상적 접속됬다면 내용 확인
        self.assertIn('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        # 포스트 수정
        response = self.client.post(
            update_post_url,
            {
                'title':'세번째 포스트를 수정했습니다.',
                'content':'안녕하세요 포스트가 수정되었습니다.',
                'category':self.category_music.pk
            },
            follow = True
        )

        # 수정이 됐는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main=area')
        self.assertIn('세번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕하세요 포스트가 수정되었습니다.', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)


    def test_create_post(self):
        response = self.client.get('/blog/create_post/')
        self.assertNotEquals(response.status_code, 200)

        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post/') # obama만 허용해줬기 때문에 접속이 되면 안됨
        self.assertNotEquals(response.status_code, 200)

        self.client.login(username='obama', password='somepassword')
        response = self.client.get('/blog/create_post/') # obama는 허용했으니 정상적이라면 접속되야함
        self.assertEquals(response.status_code, 200)

        response = self.client.get('/blog/create_post/')
        self.assertEquals(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertIn('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        self.assertEquals(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEquals(last_post.title, 'Post Form 만들기')
        self.assertEquals(last_post.author.username, 'obama')


    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        # self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)


    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        # self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)


    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)


    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Django')
        self.assertEquals(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEquals(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEquals(blog_btn.attrs['href'], '/blog')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEquals(about_me_btn.attrs['href'], '/about_me')


    def test_post_list(self):
        self.assertEquals(Post.objects.count(), 4)
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog')

        # 1.2 정상적인 페이지가 로드된다.
        self.assertEquals(response.status_code, 200)

        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1.4 네이게이션 바가 있다.
        # navbar = soup.nav

        # 1.5 Blog, About Me라는 문구가 네비게이션 바에 있다.
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 2.2 '아직 게시물이 없습니다'라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog')
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')
        # 3.4 '아직 게시물이 없습니다'라는 문구는 더 이상 보이지 않는다.
        self.assertIn('아직 게시물이 없습니다.', main_area.text)


    def test_post_detail(self):
        # # 1.1 Post가 하나 있다.
        # self.post_000 = Post.objects.create(
        #     title='첫번째 포스트 입니다.',
        #     content='Hello World. We are the world.',
        #     author=self.user_trump,
        # )

        # 1.2 그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 post의 detail 페이지 테스트
        # 2.1 첫 번째 post url로 접근하면 정상적으로 작동한다. (status code: 200))
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 post_list 페이지와 똑같은 네비게이션 바가 있다.all()
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역(post-area)에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역(post-area)에 있다.
        self.assertIn(self.post_001.title, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)