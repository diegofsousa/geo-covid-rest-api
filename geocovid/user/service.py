from geocovid.authorize.models import TemporalyDataUser
from .models import User

def temp_user_to_persist_user(temporaly_user, password):
	user = User(name=temporaly_user.name,
				email=temporaly_user.email)

	user.set_password(password)

	user.save()
	return user