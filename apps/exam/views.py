from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Thought
import bcrypt

# Create your views here.

def root(request):
	request.session['user_id'] = None
	return render(request, 'exam/root.html')

def create(request):
	if request.method == 'POST':
		errors = User.objects.basic_validator(request.POST)
		existing_email = User.objects.filter(email = request.POST['email'])

		if len(existing_email) == 0:
			if len(errors) == 0:
				User.objects.create(
					first_name = request.POST['first_name'],
					last_name = request.POST['last_name'],
					email = request.POST['email'],
					password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
					)
				user = User.objects.last()
				request.session['user_id'] = user.id
				return redirect('/board')

			else:
				for key, value in errors.items():
					messages.error(request, value, extra_tags = 'register')
				return redirect('/')

		else:
			errors['duplicate'] = 'This email has already been registered'
			for key, value in errors.items():
				messages.error(request, value, extra_tags = 'register')
			return redirect('/')

	else:
		return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.basic_validator(request.POST)
		existing_email = User.objects.filter(email = request.POST['email'])


		if len(existing_email) != 0:
			if len(errors) == 0:
				user = User.objects.get(email = request.POST['email'])

				if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
					request.session['user_id'] = user.id
					return redirect('/board')

				else:
					errors['incorrect_pw'] = 'You have submitted the wrong password'
					for key, value in errors.items():
						messages.error(request, value, extra_tags = 'login')
					return redirect('/')

			else:
				for key, value in errors.items():
					messages.error(request, value, extra_tags = 'login')
				return redirect('/')

		else:
			errors['not_registered'] = 'This email has not been registered'
			for key, value in errors.items():
				messages.error(request, value, extra_tags = 'login')
			return redirect('/')

	else:
		return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def board(request):
	if request.session['user_id'] != None:
		user_info = User.objects.get(id  = request.session['user_id'])
		all_thoughts = Thought.objects.all().order_by('-number_likes')

		context = {
			'user' : user_info,
			'thoughts' : all_thoughts,
		}

		return render(request, 'exam/board.html', context)

	else:
		messages.error(request, 'Please log in', extra_tags = 'login')
		return redirect('/')

def post_thought(request):
	print('ENTERED POST_MESSAGE')
	if request.method == 'POST':
		if 'user_id' in request.session:
			if len(request.POST['thought']) >= 5:
				user = User.objects.get(id = request.session['user_id'])
				thought_content = request.POST['thought']
				print('MESSAGE CONTENT:', thought_content)
				print('BY USER:', user)
				Thought.objects.create(content = thought_content, user = user, number_likes = 0)
				return redirect('/board')
			else:
				messages.error(request, 'The thought must be at least 5 characters long', extra_tags = 'thought')
				return redirect('/board')
		else:
			messages.error(request, 'Please log in', extra_tags = 'login')
			return redirect('/')
	else:
		return redirect('/board')

def delete_thought(request, thought_id):
	print('ENTERED DELETE_MESSAGE')
	if request.method == 'POST':
		if 'user_id' in request.session:
			thought = Thought.objects.get(id = thought_id)
			thought.delete()
			return redirect('/board')
		else:
			messages.error(request, 'Please log in', extra_tags = 'login')
			return redirect('/')
	else:
		return redirect('/board')

def view_thought(request, thought_id):
	if 'user_id' in request.session:
		thought = Thought.objects.get(id = thought_id)
		user = User.objects.get(id = request.session['user_id'])
		poster = User.objects.get(id = thought.user.id)
		print("USER", user.__dict__)
		print("POSTER", poster.__dict__)
		print("WHO LIKES", thought.users_who_like.all().values())
		poster_in = False
		likers = thought.users_who_like.all()

		if poster in likers:

			poster_in = True

		print("LIKERS 2", likers.values())
		context = {
			'thought' : thought,
			'user' : user,
			'likers' : likers,
			'poster_in' : poster_in,
			'poster' : poster
		}
		return render(request, 'exam/thought.html', context)

	else:
		messages.error(request, 'Please log in', extra_tags = 'login')
		return redirect('/')

def like_thought(request, thought_id):
	if 'user_id' in request.session:
		user = User.objects.get(id = request.session['user_id'])
		thought = Thought.objects.get(id = thought_id)

		if user not in thought.users_who_like.all():
			thought.users_who_like.add(user)
			thought.number_likes = len(thought.users_who_like.all())
			thought.save()
			return redirect('/board/' + str(thought_id) + '/details')
		
		else:
			messages.error(request, 'You have already liked this thought', extra_tags = 'thought')
			return redirect('/board/' + str(thought_id) + '/details')


	else:
		messages.error(request, 'Please log in', extra_tags = 'login')
		return redirect('/')


def unlike_thought(request, thought_id):
	if 'user_id' in request.session:
		user = User.objects.get(id = request.session['user_id'])
		thought = Thought.objects.get(id = thought_id)

		if user in thought.users_who_like.all():
			thought.users_who_like.remove(user)
			thought.number_likes = len(thought.users_who_like.all())
			thought.save()
			return redirect('/board/' + str(thought_id) + '/details')

		else:
			messages.error(request, 'You do not like this thought in the first place', extra_tags = 'thought')
			return redirect('/board/' + str(thought_id) + '/details')

	else:
		messages.error(request, 'Please log in', extra_tags = 'login')
		return redirect('/')
