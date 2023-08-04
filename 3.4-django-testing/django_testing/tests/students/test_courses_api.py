import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/1/')

    assert 200 == response.status_code
    assert response.data['name'] == courses[0].name


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert 200 == response.status_code
    for index, course in enumerate(courses):
        assert response.data[index]['name'] == course.name


@pytest.mark.django_db
def test_id_courses_filter(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?id={courses[2].pk}')

    assert 200 == response.status_code
    assert response.data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_name_courses_filter(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?name={courses[2].name}')

    assert 200 == response.status_code
    assert response.data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_course_post(client):

    response = client.post('/api/v1/courses/', data={
        "id": 1,
        "name": "test_name"
    })

    assert 201 == response.status_code
    assert response.data['name'] == 'test_name'


@pytest.mark.django_db
def test_course_patch(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.patch(f'/api/v1/courses/{courses[4].pk}/', data={"name": "test_name"}, format='json')

    assert 200 == response.status_code
    assert response.data['id'] == courses[4].id
    assert response.data['name'] == 'test_name'


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.delete(f'/api/v1/courses/{courses[4].pk}/')

    assert 204 == response.status_code
    assert response.data is None


@pytest.mark.parametrize(
    ['data', 'status_code'],
    [
        ({'name': 'test_course', 'students': 1}, 400),
        ({'name': 'test_course',}, 201)
    ]
)
@pytest.mark.django_db
def test_count_students_in_curse(client, settings, data, status_code):
    settings.MAX_STUDENTS_PER_COURSE = 0

    response = client.post(
        path='/api/v1/courses/',
        data=data,
        # format='json'
    )

    assert response.status_code == status_code
