import pytest

from apps.user.models import ExecutiveUser, TechnicalUser, User


class TestUserManager:
    """Test UserManager"""
    @pytest.mark.django_db
    def test_create_user(self):
        user = User.objects.create_user('user@test.com')
        assert not user.is_staff
        assert not user.is_superuser

        # cannot have null email
        with pytest.raises(ValueError):
            User.objects.create_user(None)

    @pytest.mark.django_db
    def test_create_superuser(self):
        user = User.objects.create_superuser('superuser@test.com', None)
        assert user.is_staff
        assert user.is_superuser

        # cannot have is_staff=False
        with pytest.raises(ValueError):
            User.objects.create_superuser('superuser@test.com', None, is_staff=False)

        # cannot have is_superuser=False
        with pytest.raises(ValueError):
            User.objects.create_superuser('superuser@test.com', None, is_superuser=False)


class TestExecutiveUserManager:
    """Test ExecutiveUserManager"""
    @pytest.mark.django_db
    def test_create_user(self):
        user = ExecutiveUser.objects.create_user('executive@test.com')
        assert user.is_executive


class TestTechnicalUserManager:
    """Test TechnicalUserManager"""
    @pytest.mark.django_db
    def test_create_user(self):
        user = TechnicalUser.objects.create_user('technical@test.com')
        assert user.is_technical
